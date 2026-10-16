// M2-03B main-RAM adapter. Hold requests to sdram_arb until completion.
// CPU reads AND writes wait for acknowledgement. Each AS cycle gets one
// transaction. Snapshot reuses both halves of aligned read pairs. CPU writes
// invalidate snapshot cache both at issue and completion; pending CPU work
// drains before a snapshot read starts. No reset clear: matches original RAM.
module m2_main_sdram #(parameter [23:0] BASE_WORD=24'h780000)(
 input clk,reset,input cpu_active,input [14:0] cpu_a,
 input cpu_we,cpu_wrl,cpu_wrh,input [15:0] cpu_d,
 output reg [15:0] cpu_q,output cpu_ready,
 input dma_active,input [14:0] dma_a,output [15:0] dma_q,output dma_ready,
 output reg [24:1] c_addr,output reg c_req,c_we,c_wrl,c_wrh,output reg [15:0] c_d,
 input c_valid,input [15:0] c_q,
 output reg [24:1] d_addr,output reg d_req,input d_valid,input [31:0] d_pair);
 reg c_done;
 reg [14:0] c_tag;
 reg pair_valid;
 reg [13:0] pair_tag,d_tag;
 reg [31:0] pair_q;
 wire cpu_unserved=cpu_active && !c_done;
 assign cpu_ready=c_done && c_tag==cpu_a;
 assign dma_ready=pair_valid && pair_tag==dma_a[14:1] && !c_req && !cpu_unserved;
 assign dma_q=dma_a[0] ? pair_q[31:16] : pair_q[15:0];
 always @(posedge clk) begin
  if (reset) begin
   c_req<=0;c_done<=0;d_req<=0;pair_valid<=0;
   c_we<=0;c_wrl<=0;c_wrh<=0;c_addr<=0;d_addr<=0;c_d<=0;cpu_q<=0;
  end else begin
   if (!cpu_active) c_done<=0;
   // AS precedes the 68000 write strobes. Latch a write only when a
   // byte lane is asserted; otherwise both masks would be frozen low.
   if (cpu_active && !c_done && !c_req && (!cpu_we || cpu_wrl || cpu_wrh)) begin
    c_addr<=BASE_WORD+cpu_a;c_tag<=cpu_a;c_we<=cpu_we;
    c_wrl<=cpu_wrl;c_wrh<=cpu_wrh;c_d<=cpu_d;c_req<=1;
    if(cpu_we)pair_valid<=0;
   end
   if(c_req && c_valid) begin
    c_req<=0;c_done<=1;cpu_q<=c_q;
    if(c_we)pair_valid<=0;
   end
   if(dma_active && !dma_ready && !d_req && !c_req && !cpu_unserved) begin
    d_addr<=BASE_WORD+{dma_a[14:1],1'b0};d_tag<=dma_a[14:1];d_req<=1;
   end
   if(d_req && d_valid) begin
    d_req<=0;pair_q<=d_pair;pair_tag<=d_tag;pair_valid<=1;
   end
  end
 end
endmodule
