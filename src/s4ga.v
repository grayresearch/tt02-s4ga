// Copyright (C) 2022, Gray Research LLC.
// Licensed under the Apache License, Version 2.0.

`default_nettype none

`define V(N)        [(N)-1:0]
`define SEG(N,M)    (((N) + ((M)-1)) / (M))

// Receive a stream of LUTs' LUT config segments of SI_W bits per clock.
// When an entire LUT config is recevied, compute the next value of that LUT.
// Output the most recent 8 LUT outputs.
//
// LUT config:
// packed struct LUT_n_k {  // N K-LUTs
//  bit[$clog2(N)] input[K];    // indices of those LUT outputs which are this LUT's K inputs.
//  bit[2**K] mask;             // LUT mask
// };
// Each input[] and mask field rounded up to next multiple of SI_W bits.
//
// For N=16, K=4, SI_W=4, this is 32 bits:
// packed struct LUT_n16_k4 {   // N=16 K=4-LUTs
//  bit[4] input[4];            // 4 4b indices
//  bit[16] mask;               // LUT mask
// };
//
// For N=64, K=6, SI_W=4, this is 112 bits:
// struct LUT_n64_k6 {          // N=64 K=4-LUTs
//  bit[8] input[6];            // 6 6b indices padded to 6 8b indices
//  bit[64] mask;               // LUT mask
// };
module s4ga #(
    parameter int N     = 32,   // # LUTs
    parameter int K     = 4,    // # LUT inputs
    parameter int SI_W  = 4     // SI width
) (
    input  wire `V(8)   io_in,
    output reg  `V(8)   io_out
);
    localparam int N_W      = $clog2(N);
    localparam int K_W      = $clog2(K+1);  // k in [0,K]
    localparam int MASK_W   = 2**K;
    localparam int IDX_W    = $clog2(N);
    localparam int SR_W     = ((MASK_W >= IDX_W) ? MASK_W : IDX_W) - SI_W;
    localparam int SEG_W    = $clog2(`SEG(SR_W, SI_W));
    localparam int MASK_SEGS= `SEG(MASK_W, SI_W);
    localparam int IDX_SEGS = `SEG(IDX_W, SI_W);

    wire            clk;        // clock input
    wire            rst;        // sync reset input
    wire `V(SI_W)   si;         // LUTs' configuration segments input stream
    reg  `V(N)      luts;       // last N LUT outputs; shift register

    assign {si,rst,clk} = io_in;
    assign io_out = luts;

    reg  `V(SR_W)   sr;         // input shift reg of LUT input index (k<K) or LUT mask (k==K)
    wire `V(MASK_W) mask    = {sr,si};  // current LUT mask
    wire `V(IDX_W)  idx     = {sr,si};  // current input index
    reg  `V(K)      ins;        // last K LUT inputs; shift register

    // control FSM
    reg  `V(N_W)    n;          // LUT counter; n in [0,N)
    reg  `V(K_W)    k;          // LUT input index counter; k in [0,K]: k<K => loading index; k==K => loading mask
    reg  `V(SEG_W)  seg;        // input segment counter

    reg/*comb*/     in;         // a LUT input;  valid when k<K  && seg==IDX_SEGS-1
    reg/*comb*/     lut;        // LUT output; valid when k==K && seg==MASK_SEGS-1

    always @* begin
        in = luts[idx];         // select an input bit from the various LUT outputs
        lut = mask[ins];        // select a LUT output from the LUT mask indexed by the input bit vector
    end

    always @(posedge clk) begin
        sr <= {sr,si};          // always collect input segments

        if (rst) begin
            luts <= 0;
            n <= 0;
            k <= 0;
            seg <= 0;
        end else if (k != K) begin
            // input index segment
            if (seg == IDX_SEGS-1) begin
                ins <= {ins,in};
                k <= k + 1'b1;
                seg <= 0;
            end else begin
                seg <= seg + 1'b1;
            end
        end else begin
            // mask segment
            if (seg == MASK_SEGS-1) begin
                luts <= {luts,lut};
                n <= (n == N-1) ? 0 : (n + 1'b1);
                k <= 0;
                seg <= 0;
            end else begin
                seg <= seg + 1'b1;
            end
        end
    end
endmodule
