# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/include.v 
VERILOG_SOURCES += $(PWD)/Weight_Memory.v
VERILOG_SOURCES += $(PWD)/maxFinder.v
#VERILOG_SOURCES += $(PWD)/Sig_ROM.v
VERILOG_SOURCES += $(PWD)/relu.v
VERILOG_SOURCES += $(PWD)/neuron.v
VERILOG_SOURCES += $(PWD)/axi_lite_wrapper.v
VERILOG_SOURCES += $(PWD)/Layer_1.v
VERILOG_SOURCES += $(PWD)/Layer_2.v
VERILOG_SOURCES += $(PWD)/Layer_3.v
VERILOG_SOURCES += $(PWD)/Layer_4.v
VERILOG_SOURCES += $(PWD)/zynet.v

# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = zyNet

# MODULE is the basename of the Python test file
MODULE = top_sim

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
