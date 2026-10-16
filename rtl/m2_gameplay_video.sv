// TEST10: registered native arcade video only. No selector or pattern source.
// Keep TEST09 native RGB/DE/HS/VS register latency and passive CRC observation.
module m2_gameplay_video(input clk,
 input [23:0] native_rgb,input native_de,native_hs,native_vs,
 output reg [23:0] rgb=0,output reg de=0,hs=0,vs=0,
 output reg [31:0] frames=0,
 output reg [31:0] frame_crc=0,frame_pixels=0);
 reg [31:0] running_crc=32'hffffffff,running_pixels=0;
 function automatic [31:0] crc24(input [31:0] previous,input [23:0] pixel);
  reg [31:0] c;integer n;begin c=previous;for(n=23;n>=0;n=n-1)c=(c[31]^pixel[n])?((c<<1)^32'h04c11db7):(c<<1);crc24=c;end
 endfunction
 always @(posedge clk)begin
  if(vs)begin frame_crc<=running_crc;frame_pixels<=running_pixels;running_crc<=32'hffffffff;running_pixels<=0;end
  else if(de)begin running_crc<=crc24(running_crc,rgb);running_pixels<=running_pixels+1'b1;end
 end
 always @(posedge clk)begin
  if(native_vs)frames<=frames+1'b1;
  rgb<=native_de?native_rgb:24'd0;de<=native_de;hs<=native_hs;vs<=native_vs;
 end
endmodule
