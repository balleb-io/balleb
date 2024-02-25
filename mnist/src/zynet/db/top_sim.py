import cocotb
from cocotb.utils import get_sim_time
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from cocotb.binary import BinaryValue

FRACBITS = 32 - 7
DATAWIDTH = 32

def fixedToFloat(bin_str, fracBits, totalBits) -> float:
    # There's probably a faster way of doing this
    # Honestly I just don't want to mess with Python's 
    # Sign extension logic here, I just want to make
    # Inference work, so,
    # TODO do this with bitwise manipulation <3
    if bin_str[0] == '1':
        inverted_bin_str = ''
        for x in bin_str:
            if x == '0': inverted_bin_str+= '1'
            if x == '1': inverted_bin_str+= '0'

        x = int(inverted_bin_str, 2) + 1

        sign = 1 if bin_str[0] == '0' else -1

        return sign * x / 2**fracBits
    else:
        return int(bin_str, 2) / 2**fracBits

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
            filename = f"../../weights/b_{k}_{j}.mif"
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
            filename = f"../../weights/w_{k}_{j}.mif"
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
    await Timer(95, units="ns")
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
        print(binstr, "->", fixedToFloat(binstr, FRACBITS, DATAWIDTH))
    print(" ")
    # TODO Maybe the padding is wrong when extending the bias' data width
    binstr = dut.l1.n_0.bias.value.binstr
    print(binstr)
    print()
    # TODO finish this as a test (i.e. compare with files using assert)
    with open("../../weights/w_1_0.mif", "r") as f:
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


# LOCALPARAMS FOR ZYNET
@cocotb.test()
async def test_inference(dut):
    TEST_SAMPLES = 10
    cocotb.start_soon(Clock(dut.s_axi_aclk, 5, units="ns").start())
    cocotb.start_soon(axi_always(dut))
#    await test_load_weights(dut)    
    cocotb.start_soon(axi_always(dut))

    dut.s_axi_aresetn.value = 0
    dut.s_axi_awvalid.value = 0
    dut.s_axi_bready.value = 0
    dut.s_axi_wvalid.value = 0
    dut.s_axi_arvalid.value = 0
    dut.axis_in_data_valid.value = 0
    await Timer(95, units="ns")
    dut.s_axi_aresetn.value = 1
    await Timer(100, units="ns")
    right = 0
    for test in range(TEST_SAMPLES):
        filename = f"../../testData/test_data_{test:04}.txt"
        print(f"---- TEST {test} ----")
        with open(filename, "r") as f:
            in_mem = f.read().split("\n")
            await RisingEdge(dut.s_axi_aclk)
            await RisingEdge(dut.s_axi_aclk)
            await RisingEdge(dut.s_axi_aclk)
            await RisingEdge(dut.s_axi_aclk)
            await RisingEdge(dut.s_axi_aclk)
            prev_prod = 0
            prev_w = 0
            prev_inp = 0
            for t in range(784):
                val = BinaryValue()
                val.binstr = in_mem[t]
                await RisingEdge(dut.s_axi_aclk)
                # Tests neuron 0 layer 1 weight product with input
                if 'z' not in dut.l1.n_0.myinputd.value.binstr and 'x' not in dut.l1.n_0.mul.value.binstr:
                        inputd = dut.l1.n_0.myinputd.value.binstr
                        wout = dut.l1.n_0.w_out.value.binstr
                        prev_result = dut.l1.n_0.sum.value.binstr
                        mul = dut.l1.n_0.mul.value.binstr
                        #print(f"{t:03}: ({mul}) {inputd} * {wout} + {prev_result}")
                        inputd = fixedToFloat(dut.l1.n_0.myinputd.value.binstr, FRACBITS, DATAWIDTH)
                        wout = fixedToFloat(dut.l1.n_0.w_out.value.binstr, FRACBITS, DATAWIDTH)
                        prev_result = fixedToFloat(dut.l1.n_0.sum.value.binstr, FRACBITS, DATAWIDTH)
                        mul = fixedToFloat(dut.l1.n_0.mul.value.binstr, FRACBITS, DATAWIDTH)
                        #print(f"{t:03}: ({mul}) {inputd} * {wout} + {prev_result}")
                        assert abs(mul - prev_prod) < 0.1, f"{mul} != {prev_w} * {prev_inp}"
                        prev_w = wout
                        prev_inp = inputd
                        prev_prod = inputd * wout

                dut.axis_in_data.value = val
                dut.axis_in_data_valid.value = 1
            await RisingEdge(dut.s_axi_aclk)
            dut.axis_in_data_valid.value = 0
            expected = in_mem[784]

            await RisingEdge(dut.l1.all_valid)
            await print_activations(1, 30, dut)

            await RisingEdge(dut.l2.all_valid)
            await print_activations(2, 30, dut)

            await RisingEdge(dut.l3.all_valid)
            await print_activations(3, 10, dut)

            await RisingEdge(dut.l4.all_valid)
            await print_activations(4, 10, dut)

            await RisingEdge(dut.intr)
            val = await read_axi(8, dut)
            print("Inference:", int(val.binstr, 2), "Expected:", int(fixedToFloat(expected, FRACBITS, DATAWIDTH)))
            if int(val.binstr, 2) == int(fixedToFloat(expected, FRACBITS, DATAWIDTH)): right += 1
    print(f"{right}/{TEST_SAMPLES} inferences correct")
    assert right != 0, "Failed inference test, got none right."

async def print_activations(layer, neurons, dut):
    if layer == 4: acts = []
    print(f"LAYER {layer}")
    for idx, x in enumerate(range(0, DATAWIDTH * neurons, DATAWIDTH)):
        binstr = getattr(dut, f"l{layer}").x_out.value.binstr[x:x+DATAWIDTH]
        if layer == 4: acts.append((fixedToFloat(binstr, FRACBITS, DATAWIDTH), 9 - idx))
        if layer != 4:
            print(f"{idx:04}:", binstr , "->", fixedToFloat(binstr, FRACBITS, DATAWIDTH))
        else:
            print(f"{idx:04} = {9 - idx:04}:", binstr , "->", fixedToFloat(binstr, FRACBITS, DATAWIDTH))
    if layer == 4: print(f"max activation {max(acts)}")
    print()
