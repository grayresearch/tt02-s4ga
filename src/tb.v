`default_nettype none
`timescale 1ns/1ps

module tb(
    input wire          clk,
    input wire          rst,
    input wire [3:0]    si,
    output wire [7:0]   luts
);
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    wire [7:0] io_in = {2'b0, si, rst, clk};
    wire [7:0] io_out;
    assign luts = io_out;

    s4ga s4ga(.io_in, .io_out);
endmodule
