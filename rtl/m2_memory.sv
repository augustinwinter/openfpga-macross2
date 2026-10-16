// M2-03B Macross II specialization. No game behavior removed for fit.
module m2_sprite_store #(parameter PIXELS=172032)(
 input clk, input we, input [17:0] wa, input [9:0] wd,
 input [17:0] ra, output [9:0] q);
 wire [8:0] qr;
 // Macross II uses five colour bits, hence nine stored bits. The tenth
 // input bit is constant zero in this specialized target.
 altsyncram #(.operation_mode("DUAL_PORT"),.intended_device_family("Cyclone V"),
  .ram_block_type("M10K"),.width_a(9),.widthad_a(18),.numwords_a(PIXELS),
  .width_b(9),.widthad_b(18),.numwords_b(PIXELS),.maximum_depth(1024),
  .address_reg_b("CLOCK0"),.outdata_reg_b("UNREGISTERED"),
  .read_during_write_mode_mixed_ports("OLD_DATA"),.power_up_uninitialized("TRUE")) ram(
  .clock0(clk),.address_a(wa),.data_a(wd[8:0]),.wren_a(we),
  .address_b(ra),.q_b(qr),.wren_b(1'b0),.rden_a(1'b1),.rden_b(1'b1),
  .byteena_a(1'b1),.byteena_b(1'b1),.clocken0(1'b1),.clocken1(1'b1),
  .clocken2(1'b1),.clocken3(1'b1),.aclr0(1'b0),.aclr1(1'b0),
  .addressstall_a(1'b0),.addressstall_b(1'b0),.data_b(9'd0));
 assign q={1'b0,qr};
endmodule

module m2_z80_lane(input clk,input [11:0] a,input we,input [7:0] d,output [7:0] q);
 altsyncram #(.operation_mode("SINGLE_PORT"),.intended_device_family("Cyclone V"),
  .ram_block_type("M10K"),.width_a(8),.widthad_a(12),.numwords_a(4096),
  .outdata_reg_a("UNREGISTERED"),.read_during_write_mode_port_a("NEW_DATA_NO_NBE_READ"),
  .power_up_uninitialized("TRUE")) ram(
  .clock0(clk),.address_a(a),.data_a(d),.wren_a(we),.q_a(q),
  .wren_b(1'b0),.rden_a(1'b1),.rden_b(1'b1),.byteena_a(1'b1),.byteena_b(1'b1),
  .clocken0(1'b1),.clocken1(1'b1),.clocken2(1'b1),.clocken3(1'b1),
  .aclr0(1'b0),.aclr1(1'b0),.addressstall_a(1'b0),.addressstall_b(1'b0));
endmodule
