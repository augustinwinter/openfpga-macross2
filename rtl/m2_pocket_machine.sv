// M2-03C feasibility proxy: actual Family C core, caches, video and SDRAM.
// Pocket-specific PLL and physical SDRAM pins; synchronous virtual host/display.
// Not an installable Pocket core. No MiSTer sys/HPS/scaler wrapper.
module m2_pocket_machine(
 input load_active, input [24:1] load_addr, input [15:0] load_word,
 input load_toggle, output load_ack,
 output sys_clock, output ram_clock, output pixel_clock_90,
 output video_hs, output video_vs, output ready_o,
 input clk_74a, input reset_req,
 input download, input write_byte, input [24:0] download_addr,
 input [7:0] download_data, input [15:0] download_index,
 input [15:0] in0, input [15:0] in1,
 output ioctl_wait, output [23:0] video_rgb, output video_de,
 output video_hblank, output video_vblank, output video_clock,
 output signed [15:0] audio_l, output signed [15:0] audio_r,
 output [12:0] dram_a, output [1:0] dram_ba, output [1:0] dram_dqm,
 output dram_clk, output dram_cke, output dram_ras_n,
 output dram_cas_n, output dram_we_n, inout [15:0] dram_dq
);
 wire clk_sys, clk_ram, clk_sdram, clk_pixel, clk_capture, pll_locked;
 assign sys_clock=clk_sys; assign ram_clock=clk_ram; assign ready_o=sdram_ready;
 pocket_pll clocks(.refclk(clk_74a),.rst(1'b0),.clk_sys(clk_sys),
   .clk_ram(clk_ram),.clk_sdram(clk_sdram),
  .clk_capture(clk_capture),.clk_pixel(clk_pixel),.clk_pixel_90(pixel_clock_90),.locked(pll_locked));
 reg reset_q, download_q, write_q;
 reg [24:0] addr_q; reg [7:0] data_q; reg [15:0] index_q; reg [15:0] in0_q,in1_q;
 always @(posedge clk_sys) begin
  reset_q<=reset_req; download_q<=download; write_q<=write_byte;
  addr_q<=download_addr; data_q<=download_data; index_q<=download_index; in0_q<=in0;in1_q<=in1;
 end
 wire sdram_ready;
 // M2-03C: first synchronizer stages are the ONLY excluded CDC endpoints.
 // Two game clocks before release; the resulting reset is game-domain data.
 reg [1:0] ready_sys=0,lock_sys=0;
 reg [1:0] lock_ram=0;
 always @(posedge clk_ram) lock_ram <= {lock_ram[0],pll_locked};
 reg game_reset=1;
 always @(posedge clk_sys) begin
  ready_sys<={ready_sys[0],sdram_ready};lock_sys<={lock_sys[0],pll_locked};
  game_reset<=reset_q|download_q|~lock_sys[1]|~ready_sys[1];
 end
 wire dtack_n,cpu_read,rom_selected,zreset,zm1,zmreq,ziorq,zcen;wire [15:0] zaddr; wire [15:0] cpu_latch_word;
 wire cpu_latch_dbin,cpu_latch_irc;
 wire [1:0] rom_pair_verdict,sd0_dout_verdict;
 wire rom_pair_start,rom_pair_done; wire [24:1] rom_pair_addr; wire [31:0] rom_pair_data;
 wire [23:1] bus_addr;wire [15:0] bus_data;wire bus_as,bus_fc0,bus_fc1,bus_fc2;
 wire [9:0] hcount,vcount; wire ce_pix,hblank,vblank;
 // The renderer prefetches the next line during pre-line blanking.
 // Preserve modular coordinates there, as its x_look contract requires.
 wire [8:0] rd_x=hcount-10'd28;
 wire [7:0] rd_y=vcount-10'd16;
 wire [23:0] rgb_sys; wire signed [15:0] audio_l_sys,audio_r_sys;
 reg [23:0] rgb_pixel; reg de_pixel,hb_pixel,vb_pixel; reg hs_pixel,vs_pixel;
 assign video_hs=hs_pixel; assign video_vs=vs_pixel;
 always @(posedge clk_pixel) begin
  rgb_pixel<=rgb_sys; de_pixel<=~hblank & ~vblank;
  hb_pixel<=hblank; vb_pixel<=vblank;
  hs_pixel<=hcount==10'd8; vs_pixel<=(hcount==0 && vcount==0);
 end
 assign video_rgb=rgb_pixel; assign video_de=de_pixel;
 assign video_hblank=hb_pixel;assign video_vblank=vb_pixel;
 assign video_clock=clk_pixel;
 assign audio_l=audio_l_sys;assign audio_r=audio_r_sys;
 wire [24:1] sd0_addr; wire sd0_req,sd0_ack; wire [15:0] sd0_dout; wire [31:0] sd0_dout_pair;
 wire [24:1] sd1_addr; wire sd1_req,sd1_ack; wire [15:0] sd1_dout; wire [31:0] sd1_dout_pair;
 wire [24:1] sd2_addr; wire sd2_req,sd2_ack; wire [15:0] sd2_dout; wire [31:0] sd2_dout_pair;
 wire [24:1] sd3_addr; wire sd3_req,sd3_ack; wire [15:0] sd3_dout; wire [31:0] sd3_dout_pair;
 wire sd0_wrl,sd0_wrh; wire [15:0] sd0_din;
 wire sd0_ack_mem;
 assign load_ack=sd0_ack_mem;
 // Boot loader owns physical port0 until all queued writes complete.
 // Translate its final toggle parity into the independently preserved core epoch.
 assign sd0_ack=load_active ? sd0_req : (sd0_ack_mem ^ load_toggle);
 wire sd2_wrl,sd2_wrh; wire [15:0] sd2_din;
 tdragon2_core #(.HW_ROMS(1)) machine(
  .dbg_rom_pair_verdict(rom_pair_verdict),.sd0_dout_verdict(sd0_dout_verdict),
  .dbg_rom_pair_start(rom_pair_start),.dbg_rom_pair_done(rom_pair_done),
  .dbg_rom_pair_addr(rom_pair_addr),.dbg_rom_pair_data(rom_pair_data),
  .clk_sys(clk_sys),
  .dbg_dtack_n(dtack_n),.dbg_cpu_read(cpu_read),.dbg_rom_selected(rom_selected),
   .dbg_cpu_latch_word(cpu_latch_word),.dbg_cpu_latch_dbin(cpu_latch_dbin),.dbg_cpu_latch_irc(cpu_latch_irc),
  .dbg_z80_pc(zaddr),.dbg_z80_reset_n(zreset),.dbg_z80_m1_n(zm1),.dbg_z80_mreq_n(zmreq),.dbg_z80_iorq_n(ziorq),.dbg_z80_cen(zcen),
  .dbg_eab(bus_addr),.dbg_data(bus_data),.dbg_as_n(bus_as),
  .dbg_fc0(bus_fc0),.dbg_fc1(bus_fc1),.dbg_fc2(bus_fc2),
  .reset(game_reset),
  .pause('0),
  .hs_addr('0),
  .hs_din('0),
  .hs_write('0),
  .hs_access('0),
  .game_macross2(1'b1),
  .game_powerins('0),
  .game_tdragon3h('0),
  .game_pi_bootleg('0),
  .game_pi_nosnd('0),
  .game_pi_gfxlsb('0),
  .ioctl_download(download_q),
  .ioctl_wr(write_q),
  .ioctl_addr(addr_q),
  .ioctl_dout(data_q),
  .ioctl_index(index_q),
  .sd0_dout(sd0_dout),
  .sd0_dout_pair(sd0_dout_pair),
  .sd0_ack(sd0_ack),
  .sd1_dout(sd1_dout),
  .sd1_dout_pair(sd1_dout_pair),
  .sd1_ack(sd1_ack),
  .sd2_dout(sd2_dout),
  .sd2_dout_pair(sd2_dout_pair),
  .sd2_ack(sd2_ack),
  .sd3_dout(sd3_dout),
  .sd3_dout_pair(sd3_dout_pair),
  .sd3_ack(sd3_ack),
  .rd_x(rd_x),
  .rd_y(rd_y),
  .dbg_pal_addr('0),
  .dbg_bgvram_addr('0),
  .dbg_txvram_addr('0),
  .in0_i(in0_q),
  .in1_i(in1_q),
  .dsw1_i(16'h00f7),
  .dsw2_i(16'h00ff),
  .osd_flip('0),
  .extra_por_hold(~lock_sys[1]),
  .dbg_bucket_sel_i('0),
  .ss_freeze('0),
  .ss_resume('0),
  .ss_active('0),
  .ss_addr('0),
  .ss_wr('0),
  .ss_wdata('0),
  .ss_replay('0),
  .rd_rgb(rgb_sys),
  .audio_l(audio_l_sys),
  .audio_r(audio_r_sys),
  .hcount_o(hcount),
  .vcount_o(vcount),
  .ce_pix_o(ce_pix),
  .hblank_o(hblank),
  .vblank_o(vblank),
  .ioctl_wait(ioctl_wait),
  .sd0_addr(sd0_addr),
  .sd0_req(sd0_req),
  .sd1_addr(sd1_addr),
  .sd1_req(sd1_req),
  .sd2_addr(sd2_addr),
  .sd2_req(sd2_req),
  .sd3_addr(sd3_addr),
  .sd3_req(sd3_req),
  .sd0_wrl(sd0_wrl),
  .sd0_wrh(sd0_wrh),
  .sd0_din(sd0_din),
  .sd2_wrl(sd2_wrl),
  .sd2_wrh(sd2_wrh),
  .sd2_din(sd2_din)
 );
 sdram #(.REFRESH_CYCLES(720),.SEPARATE_SDRAM_CLK(1)) memory(
  .SDRAM_DQ(dram_dq),
  .SDRAM_A(dram_a),
  .SDRAM_BA(dram_ba),
  .SDRAM_DQML(dram_dqm[0]),
  .SDRAM_DQMH(dram_dqm[1]),
  .SDRAM_nCS(),
  .SDRAM_nWE(dram_we_n),
  .SDRAM_nRAS(dram_ras_n),
  .SDRAM_nCAS(dram_cas_n),
  .SDRAM_CLK(dram_clk),
  .SDRAM_CKE(dram_cke),
  .ready(sdram_ready),
  .init(~lock_ram[1]),
  .clk(clk_ram),
  .clk_sdram(clk_sdram),
  .clk_capture(clk_capture),
  .prio_mode(2'b00),
  .addr0(load_active ? load_addr : sd0_addr),
  .req0(load_active ? load_toggle : (sd0_req ^ load_toggle)),
  .ack0(sd0_ack_mem),
  .dout0(sd0_dout),
  .dout0_pair(sd0_dout_pair),.dout0_verdict(sd0_dout_verdict),
  .wrl0(load_active ? 1'b1 : sd0_wrl),
  .wrh0(load_active ? 1'b1 : sd0_wrh),
  .din0(load_active ? load_word : sd0_din),
  .addr1(sd1_addr),
  .req1(sd1_req),
  .ack1(sd1_ack),
  .dout1(sd1_dout),
  .dout1_pair(sd1_dout_pair),
  .wrl1('0),
  .wrh1('0),
  .din1('0),
  .addr2(sd2_addr),
  .req2(sd2_req),
  .ack2(sd2_ack),
  .dout2(sd2_dout),
  .dout2_pair(sd2_dout_pair),
  .wrl2(sd2_wrl),
  .wrh2(sd2_wrh),
  .din2(sd2_din),
  .addr3(sd3_addr),
  .req3(sd3_req),
  .ack3(sd3_ack),
  .dout3(sd3_dout),
  .dout3_pair(sd3_dout_pair),
  .wrl3('0),
  .wrh3('0),
  .din3('0)
 );
endmodule
