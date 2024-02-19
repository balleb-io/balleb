import cocotb
from cocotb.utils import get_sim_time
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from cocotb.binary import BinaryValue

def fixedToFloat(bin_str, fracBits, totalBits) -> float:
    
    bit_list = list(bin_str)
    sign = 1
    if(bit_list[0] == "1"):
        sign = -1
        bit_list[0] = "0"

    bin_str = ''.join(bit_list)

    intRepresentation = int(bin_str, 2)

    return sign * (intRepresentation * 1.0)/(2 ** fracBits)


async def write_axi(addr, data, dut):
    await RisingEdge(dut.s_axi_aclk)
    dut.s_axi_awvalid.value = 1
    dut.s_axi_awaddr.value = addr
    dut.s_axi_wdata.value = data
    dut.s_axi_wvalid.value = 1
    await RisingEdge(dut.s_axi_wready)
    await RisingEdge(dut.s_axi_aclk)
    dut.s_axi_awvalid.value = 0
    dut.s_axi_wvalid.value = 0
    await RisingEdge(dut.s_axi_aclk)


num_layers = 4
num_neurons = [0, 30, 30, 10, 10]
num_weights = [0, 784, 30, 30, 10]

config_mem = [0 for _ in range(784)];


async def config_bias(dut):
    await RisingEdge(dut.s_axi_aclk)
    for k in range(1, num_layers+1):
        await(write_axi(12, k, dut))
        for j in range(num_neurons[k]):
            filename = f"../weights/b_{k}_{j}.mif"
            with open(filename, "r") as f:
                print("Opening file " + filename)
                elem = BinaryValue()
                elem.binstr = f.read().split("\n")[0]
                await write_axi(16, j, dut)
                await write_axi(4, elem, dut)

async def config_weights(dut):
    await RisingEdge(dut.s_axi_aclk)
    for k in range(1, num_layers+1):
        await(write_axi(12, k, dut))
        for j in range(num_neurons[k]):
            filename = f"../weights/w_{k}_{j}.mif"
            with open(filename, "r") as f:
                print("Opening file " + filename)
                config_mem = [BinaryValue() for _ in range(784)]
                for elem, weight in zip(config_mem, f.read().split("\n")):
                    elem.binstr = weight
                await(write_axi(16, j, dut))
                for t in range(num_weights[k]):
                    await write_axi(0, config_mem[t], dut)



async def axi_always(dut):
    while True:
        await RisingEdge(dut.s_axi_aclk)
        dut.s_axi_bready.value = dut.s_axi_bvalid.value
        dut.s_axi_rready.value = dut.s_axi_rvalid.value
    

@cocotb.test()
async def test_load_weights(dut):
    # Load weights through AXI interface

    cocotb.start_soon(Clock(dut.s_axi_aclk, 5, units="ns").start())
    cocotb.start_soon(axi_always(dut))

    dut.s_axi_aresetn.value = 0
    dut.s_axi_awvalid.value = 0
    dut.s_axi_bready.value = 0
    dut.s_axi_wvalid.value = 0
    dut.s_axi_arvalid.value = 0
    dut.axis_in_data_valid.value = 0
    await Timer(100, units="ns")
    dut.s_axi_aresetn.value = 1
    await Timer(100, units="ns")
    await write_axi(28, 0, dut)
    start = get_sim_time(units="ns")
    await config_weights(dut)
    await config_bias(dut)
    end = get_sim_time(units="ns")
    print(f"Configuration completed in {end-start}ns")
    for addr in range(784):
        binstr = dut.l1.n_0.WM.mem[addr].value.binstr
        print(binstr, "->", fixedToFloat(binstr, 27, 32))
    print(" ")
    # TODO Maybe the padding is wrong when extending the bias' data width
    binstr = dut.l1.n_0.bias.value.binstr
    print(binstr)
    print()
    # TODO finish this as a test (i.e. compare with files using assert)
    with open("../weights/w_1_0.mif", "r") as f:
        memory = f.read().split("\n")
        for addr in range(784):
            assert dut.l1.n_0.WM.mem[addr].value.binstr == memory[addr]

async def load_weights(dut):
    # Load weights through AXI interface
    dut.s_axi_aresetn.value = 0
    dut.s_axi_awvalid.value = 0
    dut.s_axi_bready.value = 0
    dut.s_axi_wvalid.value = 0
    dut.s_axi_arvalid.value = 0
    dut.axis_in_data_valid.value = 0
    await Timer(100, units="ns")
    dut.s_axi_aresetn.value = 1
    await Timer(100, units="ns")
    await write_axi(28, 0, dut)
    start = get_sim_time(units="ns")
    await config_weights(dut)
    await config_bias(dut)
    end = get_sim_time(units="ns")
    print(f"Loaded weights in {end - start}ns")

async def read_axi(addr, dut):
    await RisingEdge(dut.s_axi_aclk)
    dut.s_axi_arvalid.value = 1
    dut.s_axi_araddr.value = addr
    await RisingEdge(dut.s_axi_arready)
    await RisingEdge(dut.s_axi_aclk)
    dut.s_axi_arvalid.value = 0
    await RisingEdge(dut.s_axi_rvalid)
    await RisingEdge(dut.s_axi_aclk)
    val = dut.s_axi_rdata.value
    await RisingEdge(dut.s_axi_aclk)
    return val


@cocotb.test()
async def test_inference(dut):
    TEST_SAMPLES = 10
    cocotb.start_soon(Clock(dut.s_axi_aclk, 5, units="ns").start())
    cocotb.start_soon(axi_always(dut))
    await test_load_weights(dut)    
    right = 0
    for test in range(TEST_SAMPLES):
        filename = f"../testData/test_data_{test:04}.txt"
        print("Loading", filename, end = " ")
        with open(filename, "r") as f:
            in_mem = f.read().split("\n")
            await RisingEdge(dut.s_axi_aclk)
            await RisingEdge(dut.s_axi_aclk)
            await RisingEdge(dut.s_axi_aclk)
            for t in range(784):
                val = BinaryValue()
                val.binstr = in_mem[t]
                await RisingEdge(dut.s_axi_aclk)
                dut.axis_in_data.value = val
                dut.axis_in_data_valid.value = 1
            await RisingEdge(dut.s_axi_aclk)
            dut.axis_in_data_valid.value = 0
            expected = in_mem[784]
            await RisingEdge(dut.intr)
            val = await read_axi(8, dut)
            print("Inference:", val, "Expected:", expected)
            if val == expected: right += 1
    print(f"{right}/{TEST_SAMPLES} inferences correct")
    assert right != 0, "Failed inference test, got none right."