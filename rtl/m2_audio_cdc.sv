// Held-bus mailbox: one request per 256 MCLK cycles (48 kHz).
// Source sample stays stable from request acceptance through next request.
module m2_audio_cdc(input clk_sys,clk_audio,input signed [15:0] pcm,
 output reg signed [15:0] sample=0);
 reg [7:0] count=0;reg request=0;
 reg [1:0] request_s=0,ack_s=0;reg ack=0,received=0;
 reg signed [15:0] held=0;
 always @(posedge clk_audio)begin
  count<=count+1'b1; if(count==0)request<=~request;
  ack_s<={ack_s[0],ack};
  if(ack_s[1]!=received)begin sample<=held;received<=ack_s[1];end
 end
 always @(posedge clk_sys)begin
  request_s<={request_s[0],request};
  if(request_s[1]!=ack)begin held<=pcm;ack<=request_s[1];end
 end
endmodule
