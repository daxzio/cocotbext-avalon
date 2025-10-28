from random import randint
from cocotb import test

from interfaces.clkrst import ClkReset

from cocotbext.avalon import AvalonMaster
from cocotbext.avalon import AvalonBus


def returned_val(read_op):
    return int.from_bytes(read_op, byteorder="little")


class testbench:
    def __init__(self, dut, reset_sense=1, period=10):

        self.cr = ClkReset(dut, period, reset_sense=reset_sense, resetname="rst")
        self.dut = dut

        avalon_prefix = "avalon"
        self.bus = AvalonBus.from_prefix(dut, avalon_prefix)
        clk_name = "clk"
        self.intf = AvalonMaster(self.bus, getattr(dut, clk_name))


@test()
async def test_dut_proper_err(dut):
    """Test proper error handling for read-only and write-only registers"""
    tb = testbench(dut, reset_sense=1)

    await tb.cr.wait_clkn(200)

    # Read initial value from r_rw
    await tb.intf.read(0x0, 40)

    # Write and read back from r_rw
    await tb.intf.write(0x0, 61)
    await tb.intf.read(0x0, 61)

    # --------------------------------------------------------------------------
    # r_r - sw=r; hw=na; // Read-only register
    # --------------------------------------------------------------------------

    # Read constant value from r_r
    await tb.intf.read(0x4, 80)

    # Try to write to read-only register (should error)
    await tb.intf.write(0x4, 81, error_expected=True)

    # Verify value unchanged
    await tb.intf.read(0x4, 80)

    # --------------------------------------------------------------------------
    # r_w - sw=w; hw=r; // Write-only register
    # --------------------------------------------------------------------------

    # Try to read write-only register (should error, returns 0)
    await tb.intf.read(0x8, 0, error_expected=True)

    # Verify hardware sees initial value
    assert int(tb.dut.hwif_out_r_w_f.value) == 100, "Initial HW value mismatch"

    # Write new value
    await tb.intf.write(0x8, 101)

    # Try to read again (still errors)
    await tb.intf.read(0x8, 0, error_expected=True)

    # Verify hardware sees new value
    assert int(tb.dut.hwif_out_r_w_f.value) == 101, "Updated HW value mismatch"

    await tb.cr.end_test(200)


@test()
async def test_dut_incorrect_write_err(dut):
    """Test that unexpected write errors are detected"""
    tb = testbench(dut, reset_sense=1)

    await tb.cr.wait_clkn(200)

    # Read constant value
    await tb.intf.read(0x4, 80)

    tb.intf.exception_enabled = False
    assert (
        tb.intf.exception_occurred == False
    ), "Exception occurred when it should not have"
    # Try to write (should error)
    await tb.intf.write(0x4, 81, error_expected=False)
    assert (
        tb.intf.exception_occurred == True
    ), "Exception did not occur when it should have"

    await tb.cr.end_test(200)


@test()
async def test_dut_incorrect_read_err(dut):
    """Test that unexpected read errors are detected"""
    tb = testbench(dut, reset_sense=1)

    await tb.cr.wait_clkn(200)

    # Write to write-only register
    await tb.intf.write(0x8, 101)

    tb.intf.exception_enabled = False
    assert (
        tb.intf.exception_occurred == False
    ), "Exception occurred when it should not have"
    # Try to read (should error)
    await tb.intf.read(0x8, 0, error_expected=False)
    assert (
        tb.intf.exception_occurred == True
    ), "Exception did not occur when it should have"

    await tb.cr.end_test(200)

