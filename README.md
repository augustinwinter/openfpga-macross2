# Macross II — Analogue Pocket openFPGA

An openFPGA implementation of **Super Spacefortress Macross II** (NMK165 arcade hardware), maintained by August.

**Status:** Private release preparation. The clean RC1 FPGA bitstream has compiled, passed reported timing analysis, and completed an initial successful Analogue Pocket hardware smoke test on October 15, 2026. Longer gameplay, controller configurations, Dock compatibility, and long-term stability have not been exhaustively qualified. The earlier instrumented TEST13 package is preserved as a diagnostic reference.

## Release packaging (in preparation)

A distributable release ZIP must have these folders at the ZIP root, not inside an extra parent directory:

```text
Cores/August.MacrossII/
  AUTHORS.txt
  audio.json
  bitstream.rbf_r
  core.json
  data.json
  info.txt
  input.json
  interact.json
  variants.json
  video.json
Platforms/nmk16_m2.json
Platforms/_images/nmk16_m2.bin
Assets/nmk16_m2/common/
  macross2.rom
  macross2_vprom.bin
```

The ROM and timing PROM are **required to play**. Their filenames, expected sizes, and layout are specified here so owners can configure personal installations; **no copyrighted game ROM is in this repository**. Inclusion in a publicly downloadable archive requires appropriate redistribution authorization. A private local package may contain a user's own assets.

The Pocket menu title is **Macross II**; the intended platform ID is `nmk16_m2`. The platform banner must be generated from the previously supplied original Macross II artwork and validated on Pocket hardware.

## RC1 engineering evidence

- Clean bitstream: `bitstream.rbf_r`, 1,949,788 bytes; SHA-256 `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87`.
- Original working private RC1 core-only ZIP: SHA-256 `b38feb9eedf9eb90881597518cedd25e6e70bc571b98f855fa8e968726f9fb0e`.
- The working RC1 test uses legacy platform `nmk16_m2_test`. Final platform migration and banner are not yet complete.
- RC1 booted and ran with visuals and sound on physical Analogue Pocket hardware; the APF debug log showed successful ROM/PROM loading, bitstream loading, and clean unload.

## Distribution and updates

When final packaging, rights, license attribution, and presentation verification are complete, the versioned archive should be attached to a GitHub Release. To be indexed by Pocket Sync and other update tools, the public repository must be registered with the [openFPGA Library](https://github.com/openfpga-library/analogue-pocket) using its **Add Core** issue flow.

Project methodology: **OBSERVE → PROVE → EXPLAIN → CHANGE → RETEST**. Preserve successful bitstreams and test evidence; do not infer functionality from compilation alone.

## Credits and third-party notices

FPGA core release credit: August. The project builds on third-party HDL, toolchains, and the original NMK arcade hardware; exact source-level attribution and compatible redistributable licenses must be confirmed before public publication. **Macross II** and its copyrighted game assets remain the property of their respective rights holders.
