![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

# tt02-s4ga

This is the TinyTapeout2 Super Slow Serial SRAM FPGA, S4GA, the best
FPGA I could implement in ~100x100um of the 130nm Skywater ASIC PDK.

This version of S4GA uses an external serial SRAM with SQI (QSPI) mode
such as the Microchip 23LC512 to continually stream in 4-bit segments
of the LUTs' config data into the device.

While the LUT configuration data is streamed in from external SRAM,
the current LUT output values are kept on-die.

As a circuit optimization, the LUT outputs circular shift register 'luts'
shifts every cycle, but LUT evaluation occurs every LL = K * ($clog2(N)+3)/4
+ 2^K/4 cycles. Thus LUT output values are not sequential and a given
LUT output index changes from cycle to cyclei. Therefore LUT output
references in LUT input indices in the configuration bitstream must
compensate for these shenanigans.

The project is currently configured to repeatedly evaluate N=89 K=5-LUTs with LL=14 cycles.
Each LUT configuration has this format:

    // LUT config:
    struct LUT_n89_k5 { // all fields big-endian, most signif. nybble first:
        bit[8] in4;     // relative index of LUT input 4, in [0,N)
        bit[8] in3;     // relative index of LUT input 3, in [0,N)
        bit[8] in2;     // relative index of LUT input 2, in [0,N)
        bit[8] in1;     // relative index of LUT input 1, in [0,N)
        bit[8] in0;     // relative index of LUT input 0, in [0,N)
        bit[32] mask;   // 5-LUT truth table
    };

## Ripple carry LUT optimization

While evaluating each K-LUT, S4GA also evaluates the LUT's lower half-LUT
mask using the K-1 inputs in[0],...,in[K-2], into the 'Q' register.
This enables efficient ripple carry adders, using the upper half-LUT
to evaluate sum[i] and the lower half-LUT to evaluate the carry[i],
fed into the next LUT (via Q).  This uses two special input indices:

    in[i] == 2^$clog2(N)-1 (i.e., 'b111...111) => input is constant 1;
    in[i] == 2^$clog2(N)-2 (i.e., 'b111...110) => input is Q;
    otherwise ith LUT input is LUTs[in[i]].

## ASIC implementation

[Explore the GDS 3D view](https://grayresearch.github.io/tt02-s4ga).

## See also

See also my prior [Zero-to-ASIC S4GA repo](https://github.com/grayresearch/s4ga).

## TODO

1. Test bench of a (hand techmapped) FPGA circuit.
2. Whether/how to do autonomous control of external SPI memory.
3. Redo IOs to enable expandable external input and output regs w/ 74HC595 & 74HC165.

_More soon_.
