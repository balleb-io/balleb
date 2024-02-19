# This is a fork of ZyNet, a framework for automatic generation of neural networks on FPGAs

The idea is to make it faster to go from model to synthesis.

## Installation and development

Currently, Vivado is the only way of synthesis (actually, we're not sure if synthesis actually works, we're still fixing the design in simulation). 

You need Python, cocotb and icarus verilog to compile your model to verilog files and to run tests

The workflow for generating verilog and test cases is:
```sh
cd src
python3 mnistZyNet.py && python3 genTestData.py
```

This will create a `src` folder with all of the compilation results.

In order to run the testbench you cd into `src/fpga/rtl/` and run `make`.

To run specific test cases, refer to cocotb's documentation, for example: `TESTCASE=test_load_weights make`.


## Original Readme

Framework for automatically generating fully connected neural networks on FPGAs. Detailed tutorial at
https://youtu.be/3z_Eh3PSXKk
