`default_nettype none
`timescale 1ns/1ps

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

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

    S4GA #(.N(16), .K(4), .SI_W(4)) s4ga(.io_in, .io_out);
endmodule
