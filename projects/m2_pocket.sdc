# M2-03C: conservative single-cycle internal timing. No inherited MiSTer
# or Ver26 multicycles/false-path exceptions.
create_clock -name clk_74a -period 13.468013 [get_ports clk_74a]
create_clock -name clk_74b -period 13.468013 [get_ports clk_74b]
create_clock -name bridge_spiclk -period 13.468013 [get_ports bridge_spiclk]
derive_pll_clocks
derive_clock_uncertainty
set SYS [get_clocks {ic|machine|clocks|game|auto_generated|generic_pll1~PLL_OUTPUT_COUNTER|divclk}]
set PIX [get_clocks {ic|machine|clocks|game|auto_generated|generic_pll2~PLL_OUTPUT_COUNTER|divclk}]
if {[get_collection_size $SYS] != 1 || [get_collection_size $PIX] != 1} {
  error "M2-03C PLL clock collections did not match exactly"
}
create_generated_clock -name dram_clk -source \
  [get_pins {ic|machine|clocks|memory|auto_generated|generic_pll2~PLL_OUTPUT_COUNTER|divclk}] \
  [get_ports dram_clk]
# Same board-budget assumptions used by the preserved Pocket reference.
# This controller/phase still requires its own hardware validation.
set_input_delay -max -clock dram_clk 7.0 [get_ports {dram_dq[*]}]
set_input_delay -min -clock dram_clk 2.5 [get_ports {dram_dq[*]}]
set DRAM_OUT [get_ports {dram_a[*] dram_ba[*] dram_dqm[*] dram_cke dram_dq[*] dram_ras_n dram_cas_n dram_we_n}]
set_output_delay -max -clock dram_clk 1.5 $DRAM_OUT
set_output_delay -min -clock dram_clk -0.8 $DRAM_OUT
# Ready/PLL lock: synchronize into game domain; do not exclude downstream reset.
set FIRST_SYNC [get_registers {ic|machine|ready_sys[0] ic|machine|lock_sys[0] ic|machine|lock_ram[0]}]
if {[get_collection_size $FIRST_SYNC] != 3} { error "M2-03C first-stage synchronizer endpoints not found" }
set_false_path -to $FIRST_SYNC
# This virtual port forwards a PLL clock, not data. Physical display clock
# transport is outside this representative shell; all RGB/control data remains timed.


# DQ capture deliberately uses the following capture-clock edge, rather
# than the early +4ns edge. STATE_READY is retimed to this returned pair.
# Leave the setup-induced hold check in place: it checks against the next
# SDRAM beat. A matching hold relaxation would invalidate this contract.
set DQ_CAPTURE [get_registers {core_top:ic|m2_pocket_machine:machine|sdram:memory|dq_capture[*]}]
if {[get_collection_size $DQ_CAPTURE] != 16} {error "Expected sixteen DQ pad capture registers"}
set_multicycle_path -setup 2 -from [get_ports {dram_dq[*]}] -to $DQ_CAPTURE

# M2-03C held-data CDC contracts. Capture is enabled only after the
# two-stage toggle has arrived; the bus remains stable until completion.
set REQ_PAYLOAD [get_registers {*|sdram_req:*|addr_r[*] *|sdram_req:*|din_r[*] *|sdram_req:*|we_r *|sdram_req:*|wrl_r *|sdram_req:*|wrh_r}]
set RAM_PAYLOAD [get_registers {core_top:ic|m2_pocket_machine:machine|sdram:memory|a[*] core_top:ic|m2_pocket_machine:machine|sdram:memory|ba[*] core_top:ic|m2_pocket_machine:machine|sdram:memory|data[*] core_top:ic|m2_pocket_machine:machine|sdram:memory|dqm[*] core_top:ic|m2_pocket_machine:machine|sdram:memory|we core_top:ic|m2_pocket_machine:machine|sdram:memory|sel*}]
if {[get_collection_size $REQ_PAYLOAD] < 96 || [get_collection_size $RAM_PAYLOAD] < 40} {error "CDC request payload collection incomplete"}
set_max_delay 15.0 -from $REQ_PAYLOAD -to $RAM_PAYLOAD
set_min_delay -5.0 -from $REQ_PAYLOAD -to $RAM_PAYLOAD
set_max_skew 10.0 -from $REQ_PAYLOAD -to $RAM_PAYLOAD
# Physical ports: 0=CPU/ROM/DMA, 1=sprites, 2=BG, 3=TX/Z80/OKI.
set REQ_WRAPPERS [list {core_top:ic|m2_pocket_machine:machine|tdragon2_core:machine|sdram_arb:g_rom_hw.sd0_inst|sdram_req:u_req_inst} {core_top:ic|m2_pocket_machine:machine|tdragon2_core:machine|video_macross2:video|sdram_req:g_video_rom_hw.g_tx_ext.g_no_bg2_hw.spr_req_inst} {core_top:ic|m2_pocket_machine:machine|tdragon2_core:machine|video_macross2:video|sdram_req:g_video_rom_hw.bg_req_inst} {core_top:ic|m2_pocket_machine:machine|tdragon2_core:machine|sdram_arb:g_audiocpu_hw.p1_arb_inst|sdram_req:u_req_inst}]
set port 0
foreach wrapper $REQ_WRAPPERS {
 set rq [get_registers "${wrapper}|sdram_req"]
 set rqfirst [get_registers "core_top:ic|m2_pocket_machine:machine|sdram:memory|req${port}_s\[0\]"]
 set aq [get_registers "core_top:ic|m2_pocket_machine:machine|sdram:memory|ack${port}"]
 set aqfirst [get_registers "${wrapper}|ack_s\[0\]"]
 # The fitter may duplicate the launch toggle for fanout. Both copies
 # implement the same held transaction and are included in this filter.
 if {[get_collection_size $rq] < 1 || [get_collection_size $rq] > 2} {error "CDC port $port request launch mismatch"}
 if {[get_collection_size $aq] < 1 || [get_collection_size $aq] > 2} {error "CDC port $port ack launch mismatch"}
 foreach c [list $rqfirst $aqfirst] {if {[get_collection_size $c] != 1} {error "CDC port $port toggle endpoint mismatch"}}
 set_false_path -from $rq -to $rqfirst
 set_false_path -from $aq -to $aqfirst
 set ret_src [get_registers "core_top:ic|m2_pocket_machine:machine|sdram:memory|dout${port}_*"]
 # selN vanishes when only the aligned pair is consumed. Add existing
 # selectors from the controller inventory without ignored-name warnings.
 foreach_in_collection reg [get_registers {core_top:ic|m2_pocket_machine:machine|sdram:memory|*}] {
  if {[get_register_info $reg -name] == "core_top:ic|m2_pocket_machine:machine|sdram:memory|sel${port}"} {set ret_src [add_to_collection $ret_src [get_register_info $reg -name]]}
 }
 set ret_dst [get_registers "${wrapper}|dout*"]
 if {[get_collection_size $ret_src] < 32 || [get_collection_size $ret_dst] < 32} {error "CDC port $port return endpoint mismatch"}
 set_max_delay 40.0 -from $ret_src -to $ret_dst
 set_min_delay -5.0 -from $ret_src -to $ret_dst
 set_max_skew 10.0 -from $ret_src -to $ret_dst
 puts "M2-03C CDC port=$port request=[get_collection_size $REQ_PAYLOAD] controller=[get_collection_size $RAM_PAYLOAD] return_src=[get_collection_size $ret_src] return_dst=[get_collection_size $ret_dst]"
 incr port
}

# APF external adapter has vendor serial constraints; inactive peripherals are
# static pins. Pixel transport is source synchronous: data at pixel0, DDR clock
# at pixel90. Budget here is the preserved BSP display interface scope.
set_false_path -from [get_ports {bridge_1wire bridge_spimiso bridge_spimosi bridge_spiss}]
set_false_path -to [get_ports {bridge_1wire bridge_spimiso bridge_spimosi}]
# Scaler samples BOTH DDR halves on the actual forwarded quadrature clock.
# Retain the existing5ns setup /0ns hold external budget; these are declared
# assumptions, not a Pocket receiver datasheet or electrical certification.
set PIX90_PIN [get_pins {ic|machine|clocks|game|auto_generated|generic_pll3~PLL_OUTPUT_COUNTER|divclk}]
if {[get_collection_size $PIX90_PIN]!=1} {error "Video quadrature source mismatch"}
create_generated_clock -name scal_clk -source $PIX90_PIN [get_ports scal_clk]
set VIDEO_PINS [get_ports {scal_de scal_hs scal_vs scal_skip scal_vid[*]}]
if {[get_collection_size $VIDEO_PINS]!=16} {error "Video DDR pin collection incomplete"}
set_output_delay -clock scal_clk -max 5.0 $VIDEO_PINS
set_output_delay -clock scal_clk -min 0.0 $VIDEO_PINS
set_output_delay -clock scal_clk -clock_fall -add_delay -max 5.0 $VIDEO_PINS
set_output_delay -clock scal_clk -clock_fall -add_delay -min 0.0 $VIDEO_PINS
set_false_path -to [get_ports {scal_audmclk scal_audlrck scal_auddac}]
# Bound the audio held-bus path before synchronized acknowledgement capture.
set AUDIO_HELD [get_registers {ic|pcm_bridge|held[*]}]
set AUDIO_SAMPLE [get_registers {ic|pcm_bridge|sample[*]}]
if {[get_collection_size $AUDIO_HELD]!=16 || [get_collection_size $AUDIO_SAMPLE]!=16} {error "Audio mailbox endpoints incomplete"}
set_max_delay 40.0 -from $AUDIO_HELD -to $AUDIO_SAMPLE
set_min_delay -5.0 -from $AUDIO_HELD -to $AUDIO_SAMPLE
set_max_skew 10.0 -from $AUDIO_HELD -to $AUDIO_SAMPLE
# Analog controller inputs cross from clk_74a into clk_sys.
# Cut only the first synchronizer stage; retain downstream timing.
set ANALOG_P1 [get_registers {*|joypad:joypad_p1|pjoy_s1[*]}]
set ANALOG_P2 [get_registers {*|joypad:joypad_p2|pjoy_s1[*]}]
if {[get_collection_size $ANALOG_P1] < 1 || [get_collection_size $ANALOG_P2] < 1} {error "Analog controller first-stage synchronizers missing"}
set APF_HEADS [get_registers {*|synch_3:*|s1[*] *|synch_2:*|s1[*] *|joypad:*|pkey_s1[*] *|joypad:*|pjoy_s1[*]}]
if {[get_collection_size $APF_HEADS] < 40} {error "APF synchronizer head collection incomplete"}
set_false_path -to $APF_HEADS
set NEW_HEADS [get_registers {ic|pcm_bridge|request_s[0] ic|pcm_bridge|ack_s[0] ic|rom_loader|over_s[0] ic|rom_loader|all_s[0] ic|rom_loader|reset_74[0]}]
if {[get_collection_size $NEW_HEADS]!=5} {error "New mailbox/loader synchronizers incomplete"}
set_false_path -to $NEW_HEADS
# Vendor FIFO payloads are only read after synchronized pointer propagation.
# Bound storage->read-latch settling, rather than a phase-aligned single cycle.
set FIFO_STORE [get_registers {*|dcfifo:*|*fifo_ram*|ram_block*}]
set FIFO_READ [get_registers {*|dcfifo:*|*fifo_ram*|rd_data_out_latch*}]
if {[get_collection_size $FIFO_STORE]<128 || [get_collection_size $FIFO_READ]<32} {error "FIFO memory collection incomplete"}
set_max_delay 40.0 -from $FIFO_STORE -to $FIFO_READ
set_min_delay -5.0 -from $FIFO_STORE -to $FIFO_READ
# The real APF source clk74b and audio PLL are independent of game source74a.
# Only single-bit synchronizers, vendor dcfifo Gray pointer paths and held
# mailbox payloads cross domains. No game/memory clocks are cut as a group.
set AUDIO [get_clocks {*pocket_audio_mixer*divclk}]
# Targeted request/ack first-stage exceptions above retain the audio held-bus max/min bounds.
# There are no other game/audio crossings in the fitted IIR=0 mono wrapper.
set_clock_groups -asynchronous -group [get_clocks bridge_spiclk] -group [get_clocks {clk_74a clk_74b *divclk dram_clk scal_clk}]

# The restored boot loader drives the port0 ACK epoch while CPU reset is held.
# Only its launch toggles/selection into the existing ACK FIRST stage are cut;
# ack_s[0]->ack_s[1] and all functional downstream reset/load paths stay timed.
set LOADER_EPOCH [get_registers {ic|rom_loader|req* ic|rom_loader|active}]
set CPU_ACK_HEAD [get_registers {core_top:ic|m2_pocket_machine:machine|tdragon2_core:machine|sdram_arb:g_rom_hw.sd0_inst|sdram_req:u_req_inst|ack_s[0]}]
if {[get_collection_size $LOADER_EPOCH]<2 || [get_collection_size $CPU_ACK_HEAD]!=1} {error "Loader ACK epoch endpoints incomplete"}
set_false_path -from $LOADER_EPOCH -to $CPU_ACK_HEAD

# FIFO vendor guide, reset synchronization enabled in BOTH domains:
# https://docs.altera.com/r/docs/683522/25.1.1/fifo-ip-user-guide/recovery-and-removal-timing-violation-warnings-when-compiling-a-dcfifo
# Cut only external ACLR into the two reset synchronizer pipes. Restricting
# the source to reset_74[2] keeps their stage-to-stage D paths timed; every
# synchronized output->FIFO pointer/status recovery/removal path stays timed.
set FIFO_RESET_REGS [get_registers {*|m2_apf_loader:rom_loader|dcfifo:queue|dcfifo_*:auto_generated|dffpipe_*:rdaclr|dffe*a[0] *|m2_apf_loader:rom_loader|dcfifo:queue|dcfifo_*:auto_generated|dffpipe_*:wraclr|dffe*a[0]}]
set FIFO_RESET_SRC [get_registers {ic|rom_loader|reset_74[2]}]
if {[get_collection_size $FIFO_RESET_REGS]!=4 || [get_collection_size $FIFO_RESET_SRC]!=1} {error "FIFO reset synchronizer endpoints incomplete"}
set_false_path -from $FIFO_RESET_SRC -to $FIFO_RESET_REGS
