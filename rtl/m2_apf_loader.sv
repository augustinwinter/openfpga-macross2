// M2-08: APF bridge words cross once and write both SDRAM lanes together.
// Cold boot only: slot reload is disabled in data.json. No game ROM is embedded.
module m2_apf_loader(
 input clk_74a,clk_ram,bridge_wr,little,allcomplete,ready,reset,
 input [31:0] bridge_addr,bridge_data,
 output wire [31:0] diag_words,
 output reg active=1, output wire error,
 output reg [24:1] addr=0,output reg [15:0] word_data=0,
 output reg req=0,input ack
);
 wire full,empty;wire [55:0] q;
 reg prev_wr=0;reg over=0;reg [55:0] fifo_data;
 reg push=0; reg pop=0;
 (* preserve, dont_merge, altera_attribute="-name SYNCHRONIZER_IDENTIFICATION FORCED_IF_ASYNCHRONOUS" *) reg [2:0] reset_74=3'b111;
 // Synchronize memory initialization into the APF domain; FIFO release is
 // additionally synchronized internally in both FIFO clock domains.
 always @(posedge clk_74a) reset_74<={reset_74[1:0],reset};
 wire [31:0] stream=little ? bridge_data : {bridge_data[7:0],bridge_data[15:8],bridge_data[23:16],bridge_data[31:24]};
 always @(posedge clk_74a) begin
  if(reset_74[2])begin prev_wr<=0;push<=0;over<=0;fifo_data<=0;end
  else begin
  prev_wr<=bridge_wr;push<=0;
  if (bridge_wr && !prev_wr && bridge_addr[31:28]==4'h1) begin
   if (full || bridge_addr[27:24]!=0 || bridge_addr[23:0]>=24'h9c0000 || bridge_addr[1:0]!=0) over<=1;
   else begin fifo_data<={bridge_addr[23:0],stream};push<=1;end
  end
  end
 end
 dcfifo #(.intended_device_family("Cyclone V"),.lpm_numwords(64),.lpm_width(56),.lpm_widthu(6),
   .lpm_showahead("OFF"),.overflow_checking("ON"),.underflow_checking("ON"),
   .rdsync_delaypipe(5),.wrsync_delaypipe(5),.read_aclr_synch("ON"),
   .write_aclr_synch("ON"),.use_eab("ON")) queue(
   .data(fifo_data),.wrclk(clk_74a),.wrreq(push),.wrfull(full),
   .rdclk(clk_ram),.rdreq(pop),.q(q),.rdempty(empty),.aclr(reset_74[2]));
 reg [2:0] state=0;reg [15:0] upper;
 reg completed=0;
 (* preserve, dont_merge, altera_attribute="-name SYNCHRONIZER_IDENTIFICATION FORCED_IF_ASYNCHRONOUS" *) reg [1:0] all_s=0,over_s=0;
 reg [5:0] drain=0;
 reg [21:0] words=0;
 reg count_error=0;
 assign diag_words={10'd0,words};
 assign error=over_s[1]|count_error;
 always @(posedge clk_ram) begin
  // A real reset path retains the cold-boot loader in synthesized hardware.
  // SDRAM initialization asserts reset before any host transfer is accepted.
  if(reset)begin
   active<=1;state<=0;req<=0;addr<=0;word_data<=0;upper<=0;pop<=0;
   completed<=0;all_s<=0;over_s<=0;drain<=0;words<=0;count_error<=0;
  end else begin
  all_s<={all_s[0],allcomplete};over_s<={over_s[0],over};pop<=0;
  if(all_s[1])completed<=1;
  case(state)
   0: if(ready && !empty && active)begin pop<=1;state<=1;drain<=0;end
      else if(completed && ready && empty && active)begin
       if(drain==63)begin
        // 0x9c0000 bytes = 0x270000 APF words; fail closed on a missing tail.
        if(words==22'h270000 && !error) active<=0;
        else count_error<=1;
       end else drain<=drain+1'b1;
      end
   1: state<=2; // synchronous FIFO read
   2: begin addr<=q[55:33];word_data<=q[15:0];upper<=q[31:16];req<=~req;state<=3;end
   3: if(ack==req)begin addr<=addr+1'b1;word_data<=upper;req<=~req;state<=4;end
   4: if(ack==req)begin words<=words+1'b1;state<=0;end
   default:state<=0;
  endcase
  end
 end
endmodule
