SIM?=icarus
TOPLEVEL_LANG=verilog

TOPLEVEL = regblock
MODULE = test_dut

VERILOG_SOURCES = regblock.sv

COCOTB_TEST_MODULES = test_dut

include $(shell cocotb-config --makefiles)/Makefile.sim

etana:
	peakrdl etana regblock.rdl -o ./ --cpuif avalon-mm-flat --err-if-bad-addr --err-if-bad-rw --rename regblock

regblock:
	peakrdl regblock regblock.rdl -o ./ --cpuif avalon-mm-flat --err-if-bad-addr --err-if-bad-rw --rename regblock

clean::
	rm -rf sim_build/ __pycache__/ results.xml *.fst *.vcd

