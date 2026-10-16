// Hold reset/download until every V-PROM byte has actually crossed APF FIFO.
module m2_prom_guard(input clk,input wr,input [15:0] index,input [24:0] addr,
 output reg ready=0,output reg error=0, output wire [8:0] diag_count);
 reg [8:0] count=0;
 assign diag_count=count;
 always @(posedge clk)begin
  if(wr && index==16'd1)begin
   if(count==256 || addr!={16'd0,count})error<=1;
   else begin count<=count+1'b1;if(count==255)ready<=1;end
  end
 end
endmodule
