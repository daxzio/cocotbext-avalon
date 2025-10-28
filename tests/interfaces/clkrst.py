"""Clock and Reset utilities for cocotb tests"""

from cocotb.triggers import RisingEdge, Timer


class ClkReset:
    """Clock and reset controller"""
    
    def __init__(self, dut, period=10, reset_sense=1, resetname="rst"):
        self.dut = dut
        self.period = period
        self.reset_sense = reset_sense
        self.resetname = resetname
        
        # Get clock and reset signals
        self.clk = getattr(dut, "clk")
        self.rst = getattr(dut, resetname)
        
        # Start clock
        import cocotb
        cocotb.start_soon(self._run_clock())
        
        # Initialize reset
        cocotb.start_soon(self._do_reset())
    
    async def _run_clock(self):
        """Run clock indefinitely"""
        while True:
            self.clk.value = 0
            await Timer(self.period // 2, units='ns')
            self.clk.value = 1
            await Timer(self.period // 2, units='ns')
    
    async def _do_reset(self):
        """Apply reset at start"""
        self.rst.value = self.reset_sense
        await Timer(self.period * 10, units='ns')
        self.rst.value = 1 - self.reset_sense
        await Timer(self.period, units='ns')
    
    async def wait_clkn(self, n):
        """Wait for n clock cycles"""
        for _ in range(n):
            await RisingEdge(self.clk)
    
    async def end_test(self, n):
        """Wait n cycles before ending test"""
        await self.wait_clkn(n)

