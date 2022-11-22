# Copyright (C) 2022, Gray Research LLC.
# Licensed under the Apache License, Version 2.0.

# Handbuilt test vectors for now.
# FPGA synthesis and bitgen tools to come.

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

N = 283             # no. LUTs
K = 5               # no. LUT inputs
I = 2               # no. FPGA inputs
W = 4               # LUT config data segment width
MASK_SEGS = (1<<K)//W   # LUT mask segments
IDX_SEGS = ((3+I+N).bit_length() + W-1) // W
LL = K*IDX_SEGS + MASK_SEGS    # LUT latency (no. cycles in a LUT config frame)

def nyb(n, i):
    return (n >> (i*W)) & ((1<<W)-1)

# special LUT input indices -- these are rotated into [0,4] below.
_ = N+0         # constant 0
H = N+1         # constant 1
Q = N+2         # Q (often carry-in)
I0 = N+3        # FPGA input 0
I1 = N+4        # FPGA input 1
SPECIALS = 5

# LUTs
_E = 0xFFFF0000 # pass E input
_0 = 0x00000000 # constant 0
_1 = 0xFFFFFFFF # constant 1
_A = 0x9696e8e8 # {sum,carry}
_X = 0x96696996 # xor5

zero = [_,_,_,_,_, _0, 0,0,  0,0,0,0,0, 0]

vectors=[
#    LUT-input      inps  expected ins,lut
#    4 3 2 1 0 mask 0 1   4 3 2 1 0  O
    [I0,_,_,_,_,_E, 0,1,  0,0,0,0,0, 0], # input 0 = 0
    [I1,_,_,_,_,_E, 0,1,  1,0,0,0,0, 1], # input 1 = 1
    [I0,_,_,_,_,_E, 1,0,  1,0,0,0,0, 1], # input 0 = 1
    [I1,_,_,_,_,_E, 1,0,  0,0,0,0,0, 0], # input 1 = 0

    [_,_,_,_,_, _E, 0,0,  0,0,0,0,0, 0], # _E(0,...) = 0
    [H,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # _E(1,...) = 1
    [0,0,0,0,0, _E, 0,0,  0,0,0,0,0, 0], # _E(0s) = 0
    [1,1,1,1,1, _E, 0,0,  1,1,1,1,1, 1], # _E(1s) = 1

    [_,_,_,_,_, _0, 0,0,  0,0,0,0,0, 0], # L,Q = 0,0
    [Q,_,_,_,_, _E, 0,0,  0,0,0,0,0, 0], # _E(Q,...) = 0
    [_,_,_,_,_, _1, 0,0,  0,0,0,0,0, 1], # L,Q = 1,1
    [Q,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # _E(Q,...) = 1

    zero, zero, zero, zero,

# 16: exercise adder LUT
    [H,_,0,0,0, _A, 0,0,  1,0,0,0,0, 0], # S(0,0,0) = 0
    [Q,_,_,_,_, _E, 0,0,  0,0,0,0,0, 0], # Q(0,0,0) = 0
    [H,_,0,0,1, _A, 0,0,  1,0,0,0,1, 1], # S(0,0,1) = 1
    [Q,_,_,_,_, _E, 0,0,  0,0,0,0,0, 0], # Q(0,0,1) = 0
    [H,_,0,1,1, _A, 0,0,  1,0,0,1,1, 0], # S(0,1,1) = 0
    [Q,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # Q(0,1,1) = 1
    [H,_,1,1,1, _A, 0,0,  1,0,1,1,1, 1], # S(1,1,1) = 1
    [Q,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # Q(1,1,1) = 1
    [H,_,1,1,0, _A, 0,0,  1,0,1,1,0, 0], # S(1,1,0) = 0
    [Q,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # Q(1,1,0) = 1
    [H,_,1,0,0, _A, 0,0,  1,0,1,0,0, 1], # S(1,0,0) = 1
    [Q,_,_,_,_, _E, 0,0,  0,0,0,0,0, 0], # Q(1,0,0) = 0

# 28: 8b adder 'b11101101 + 'b11100111 = '111010100
    [H,_,1,1,0, _A, 0,0,  1,0,1,1,0, 0],
    [H,_,1,0,Q, _A, 0,0,  1,0,1,0,1, 0],
    [H,_,1,1,Q, _A, 0,0,  1,0,1,1,1, 1],
    [H,_,0,1,Q, _A, 0,0,  1,0,0,1,1, 0],
    [H,_,0,0,Q, _A, 0,0,  1,0,0,0,1, 1],
    [H,_,1,1,Q, _A, 0,0,  1,0,1,1,0, 0],
    [H,_,1,1,Q, _A, 0,0,  1,0,1,1,1, 1],
    [H,_,1,1,Q, _A, 0,0,  1,0,1,1,1, 1],
    [Q,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1],

    zero, zero, zero,

# 40: xors
    [28,29,30,31,32, _X, 0,0, 0,0,1,0,1, 0],
    [40,33,34,35,36, _X, 0,0, 0,0,1,1,1, 1],
    [41,16,17,18,19, _X, 0,0, 1,0,0,1,0, 0],
    [42,20,21,22,23, _X, 0,0, 0,0,1,1,1, 1],
    [43,24,25,26,27, _X, 0,0, 1,0,1,1,0, 1],
    [40,41,42,43,44, _X, 0,0, 0,1,0,1,1, 1],
    zero, zero, zero, zero,

#50:
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,

#100:
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,

#200:
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,
    zero, zero, zero, zero, zero, zero, zero, zero, zero, zero,

#270: test O=7 output pins: output 'b1100101
    zero, zero, zero, zero, zero, zero,

    [H,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # _E(1,...) = 1
    [H,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # _E(1,...) = 1
    [_,_,_,_,_, _E, 0,0,  0,0,0,0,0, 0], # _E(0,...) = 0
    [_,_,_,_,_, _E, 0,0,  0,0,0,0,0, 0], # _E(0,...) = 0
    [H,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # _E(1,...) = 1
    [_,_,_,_,_, _E, 0,0,  0,0,0,0,0, 0], # _E(0,...) = 0
    [H,_,_,_,_, _E, 0,0,  1,0,0,0,0, 1], # _E(1,...) = 1

#283:
]

ExpectedFPGAOutput = 0x65

# wait one clock cycle, then check the signal matches the test vector expected value
async def delay_assert(dut, signal, expected, error):
    await ClockCycles(dut.clk, 1)
    assert signal.value == expected, error

@cocotb.test()
async def test_s4ga(dut):
    print("N=%d K=%d LL=%d" % (N, K, LL));
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.fork(clock.start())
    
    # reset FPGA for N+1 cycles (mandatory)
    dut._log.info("reset")
    dut.rst.value = 1
    dut.si.value = 0
    dut.inputs.value = 0
    await ClockCycles(dut.clk, N + 1);
    dut.rst.value = 0

    dut._log.info("go");
    for i in range(len(vectors)):
        vec = vectors[i]
        mask = vec[K]
        in0 = vec[K+1]
        in1 = vec[K+2]
        dut.inputs.value = 2*in1 + in0

        # send LUT input indices and check LUT input values
        for k in range(K):
            idx = vec[k]
            if idx < N:
                # adjust relative index to the specified LUT output
                # to account for 'luts' shuffling circulating shift
                # register, which shifts every cycle
                idx = ((i-1 - idx)*LL + IDX_SEGS*k+IDX_SEGS-1) % N

            # adjust index so that special indices and inputs precede relatively indexed LUT outputs
            idx = (idx + SPECIALS) % (N + SPECIALS);

            # send index big-endian
            for s in range(IDX_SEGS-1,-1,-1):
                dut.si.value = nyb(idx, s)
                await ClockCycles(dut.clk, 1)

            cocotb.fork(delay_assert(dut, dut.s4ga.debug, vec[K+3+k], "input error: i=%d k=%d" % (i, k)))

        # send mask and check LUT output
        for j in range(MASK_SEGS):
            dut.si.value = nyb(mask, MASK_SEGS-1-j)
            await ClockCycles(dut.clk, 1)

        cocotb.fork(delay_assert(dut, dut.s4ga.debug, vec[2*K+3], "output error: i=%d" % (i)))

    # check FPGA outputs updated with last O=7 LUT outputs
    await ClockCycles(dut.clk, 1)
    await ClockCycles(dut.clk, 1)
    assert dut.outputs.value == ExpectedFPGAOutput, "FPGA output error"
