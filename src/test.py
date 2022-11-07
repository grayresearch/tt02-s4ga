import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

@cocotb.test()
async def test_7seg(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.fork(clock.start())
    
    dut._log.info("reset")
    dut.rst.value = 1
    dut.si.value = 0
    await ClockCycles(dut.clk, 64 + 1);
    dut.rst.value = 0

    # TODO: verify FPGA operation. For now we just exercise things.

    dut._log.info("go");
    for i in range(1000):
        dut.si.value = i % 16
        await ClockCycles(dut.clk, 1)
