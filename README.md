![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

# tt02-s4ga

This is the TinyTapeout2 Super Slow Serial SRAM FPGA, S4GA, the best FPGA I could implement in ~100x100um of the 130nm Skywater ASIC PDK.

This version of S4GA uses an external serial SRAM with SQI (QSPI) mode such as the Microchip 23LC512
to continually stream in 4-bit segments of the LUTs' config data into the device.

While the LUT configuration data is streamed in from external SRAM, the current LUT output values are kept on-die.

The project is currently configured to repeatedly evaluate N=64 K=4-LUTs.
Each LUT configuration has this format:

    // LUT config:
    struct LUT_n64_k4 {	// all fields big-endian, most signif. nybble first:
        bit[8] in3;     // relative index of LUT input 3, in [0,63]
        bit[8] in2;     // relative index of LUT input 2, in [0,63]
        bit[8] in1;     // relative index of LUT input 1, in [0,63]
        bit[8] in0;     // relative index of LUT input 0, in [0,63]
        bit[16] mask;   // 4-LUT truth table
    };

_More soon_.

See also my prior [Zero-to-ASIC S4GA repo](https://github.com/grayresearch/s4ga).
