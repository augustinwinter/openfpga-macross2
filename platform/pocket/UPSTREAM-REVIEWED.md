# Reviewed Pocket platform subset — source provenance

This directory includes a staged group of **10** original licensed Pocket integration HDL files first reviewed and published in the [Macross Ver.26 publication-batch record](https://github.com/augustinwinter/openfpga-nmk16/blob/codex/publication-bootstrap/docs/PUBLICATION-BATCH-2.md).

**Immutable source snapshot:** `augustinwinter/openfpga-nmk16` commit `17800b2c7292cecce9169acee4daf2e62914a36e`, originally matched to `plasticbugs/pocket-core-template` commit `c77563fa84bcc5754d5f1f6ba51168e8849f0e1d`. Original file paths, source bytes, individual author notices and licensing headers have been preserved exactly. The 10 files also matched the active Macross II local HDL at CP48AV.

| Reviewed relative path | Git blob SHA-1 |
|---|---|
| `platform/pocket/audio/filters/audio_filters.sv` | `bcdbf6614d97caaa1c27d5175b4ca5ce3399355f` |
| `platform/pocket/audio/filters/audio_mix.sv` | `6b70b7dc0d80267cef4f7b30efe43b755b20f00d` |
| `platform/pocket/audio/filters/dc_blocker.sv` | `30cc92d6412d683c74bf9d82bb7edee7e1140413` |
| `platform/pocket/audio/filters/iir_filter.sv` | `81e4b60ec225ff5a315200d621001412d07da53a` |
| `platform/pocket/audio/filters/iir_filter_tap.sv` | `7e9ca2353b192b17bbcc7532784538622ffadabc` |
| `platform/pocket/support/hiscore.sv` | `36979ac7ff47413d555573d6b72121b78c04e7e9` |
| `platform/pocket/support/nvram.sv` | `ee128c0c256f1386d719810e078b7001661528e3` |
| `platform/pocket/video/scanlines.sv` | `390c19797af24df4779e9106c94c6350d427dec6` |
| `platform/pocket/video/scanlines_generator.sv` | `94a6536479f65af1f2b092f1121b0f9f218a99c3` |
| `platform/pocket/video/shadowmask.sv` | `e062b2db48114fc8591379721aed25cdec5b16fb` |

The original GPL notices and named rights holders in these files are authoritative. A complete GPLv3 license text is available in [FX68K LICENSE](../../reference/rtl/third_party/fx68k/LICENSE), supplied as part of another licensed third-party source batch. This cross-reference **does not** assert all files in the broader `platform/pocket/` tree share a single license; other previously matched template files may have separate grants or outstanding review.

**Not included:** Copyrighted arcade ROM/PROMs, original artwork, unreviewed template files, edited Pocket `core_top.sv`, edited bridge command logic, project-owned RTL, vendor-generated IP not independently cleared, or build outputs. Staged files alone do not constitute a complete reproducible Pocket core. See [ATTRIBUTION.md](../../ATTRIBUTION.md) and [CROSS_PROJECT_REUSE.md](../../CROSS_PROJECT_REUSE.md).
