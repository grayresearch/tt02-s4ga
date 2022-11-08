![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

# tt02-s4ga

This is the TinyTapeout2 Super Slow Serial SRAM FPGA, S4GA, the best FPGA I could implement in ~100x100um of the 130nm Skywater ASIC PDK.

This version of S4GA uses an external serial SRAM with SQI (QSPI) mode such as the Microchip 23LC512
to continually stream in 4-bit segments of the LUTs' config data into the device.

While the LUT configuration data is streamed in from external SRAM, the current LUT output values are kept on-die.

The project is currently configured to repeatedly evaluate N=101 K=5-LUTs.
Each LUT configuration has this format:

    // LUT config:
    struct LUT_n101_k5 { // all fields big-endian, most signif. nybble first:
        bit[8] in4;     // relative index of LUT input 4, in [0,63]
        bit[8] in3;     // relative index of LUT input 3, in [0,63]
        bit[8] in2;     // relative index of LUT input 2, in [0,63]
        bit[8] in1;     // relative index of LUT input 1, in [0,63]
        bit[8] in0;     // relative index of LUT input 0, in [0,63]
        bit[32] mask;   // 5-LUT truth table
    };

## Ripple carry LUT optimization

While evaluating each K-LUT, S4GA also evaluates the LUT's lower half-LUT mask using the K-1 inputs in[0],...,in[K-2], into the 'Q' register.
This enables efficient ripple carry adders, using the upper half-LUT to evaluate sum[i] and the lower half-LUT to evaluate the carry[i], fed into the next LUT.
This uses two special input indices:

    in[i] == 2**$clog2(N)-1 (i.e., 'b111...111) => input is 1'b1;
    in[i] == 2**$clog2(N)-2 (i.e., 'b111...110) => input is Q;
    otherwise ith LUT input is LUTs[in[i]].

# ASIC implementation

[Explore the GDS 3D view](https://grayresearch.github.io/tt02-s4ga).

# See also

See also my prior [Zero-to-ASIC S4GA repo](https://github.com/grayresearch/s4ga).

_More soon_.
