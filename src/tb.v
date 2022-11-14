`default_nettype none
`timescale 1ns/1ps

module tb(
    input wire          clk,
    input wire          rst,
    input wire [3:0]    si,
    input wire [1:0]    inputs,
    output wire [6:0]   outputs,
    output wire         debug
);
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    wire [7:0] io_in = {inputs,si,rst,clk};
    wire [7:0] io_out;
    assign {debug,outputs} = io_out;

    s4ga s4ga(.io_in, .io_out);
endmodule
