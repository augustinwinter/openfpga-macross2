// M2-04A: exact rational nominal clocks from the Pocket 74.25MHz source.
// Game M/N=160/11, C=27/135 => 40/8MHz; memory M/N=128/11, C=9 => 96MHz.
// Memory phase step is 1/(8*864MHz)=144.676ps: -/+14 steps = -/+2025.463ps.
// Frequencies remain proportional to actual board oscillator tolerance.
module pocket_pll(input refclk, input rst, output clk_sys, output clk_ram, output clk_sdram,
                  output clk_pixel, output clk_pixel_90, output clk_capture, output locked);
  wire [4:0] a,b; wire game_locked,memory_locked;
  altpll #(.intended_device_family("Cyclone V"),.inclk0_input_frequency(13468),
    .operation_mode("NORMAL"),.pll_type("AUTO"),.compensate_clock("CLK0"),
    .clk0_multiply_by(160),.clk0_divide_by(297),.clk0_duty_cycle(50),.clk0_phase_shift("0"),
    .clk1_multiply_by(32),.clk1_divide_by(297),.clk1_duty_cycle(50),.clk1_phase_shift("0"),
    .clk2_multiply_by(32),.clk2_divide_by(297),.clk2_duty_cycle(50),.clk2_phase_shift("31250"),
    .width_clock(5)) game(.inclk({1'b0,refclk}),.areset(rst),.clk(a),.locked(game_locked),
      .clkena(6'b111111),.extclkena(4'b1111),.pllena(1'b1),.pfdena(1'b1));
  altpll #(.intended_device_family("Cyclone V"),.inclk0_input_frequency(13468),
    .operation_mode("NORMAL"),.pll_type("AUTO"),.compensate_clock("CLK0"),
    .clk0_multiply_by(128),.clk0_divide_by(99),.clk0_duty_cycle(50),.clk0_phase_shift("0"),
    .clk1_multiply_by(128),.clk1_divide_by(99),.clk1_duty_cycle(50),.clk1_phase_shift("-2025"),
    .clk2_multiply_by(128),.clk2_divide_by(99),.clk2_duty_cycle(50),.clk2_phase_shift("2604"),
    .width_clock(5)) memory(.inclk({1'b0,refclk}),.areset(rst),.clk(b),.locked(memory_locked),
      .clkena(6'b111111),.extclkena(4'b1111),.pllena(1'b1),.pfdena(1'b1));
  assign clk_sys=a[0]; assign clk_pixel=a[1]; assign clk_pixel_90=a[2];
  assign clk_ram=b[0]; assign clk_sdram=b[1]; assign clk_capture=b[2];
  assign locked=game_locked & memory_locked;
endmodule
