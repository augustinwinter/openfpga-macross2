<img width="522" height="165" alt="macrossII_arcade_banner" src="https://github.com/user-attachments/assets/557417e2-baf1-4296-97d2-134e15369ddc" />



# Macross II — Analogue Pocket openFPGA

A preservation-oriented FPGA implementation of **Super Spacefortress Macross II** (Japanese NMK165 arcade hardware) for the Analogue Pocket. Maintained by August.

**Status (2026-10-15): private beta `0.14.0-beta.1`, verified playable on physical Pocket hardware. Not yet cleared for public release.** The core appears as **Macross II** under openFPGA → Arcade and as **Macross II 0.14.0-beta.1** in Developer → Builds. The original game banner, startup, sound, graphics and gameplay passed the reported Pocket checks. This is not a claim of exhaustive long-duration, Dock, or controller-configuration qualification.

## Start here: reproduce the assets

**[REPRODUCING.md — how to reconstruct the exact required arcade ROM and timing PROM, verify checksums, install the core, and resolve missing Arcade menu entries](REPRODUCING.md)**

**[tools/assemble-rom.py — verified-layout ROM assembly tool](tools/assemble-rom.py)**

**[BUILDING.md — recorded Quartus toolchain, active dependencies, bitstream conversion, and publication blockers](BUILDING.md)**

**[ATTRIBUTION.md — upstream contributors, license evidence, and unresolved provenance checks](ATTRIBUTION.md)**

**[CROSS_PROJECT_REUSE.md — reuse previously verified Macross Ver.26 dependencies without repeating their provenance audits](CROSS_PROJECT_REUSE.md)**

**[tools/convert-rbf.py — Pocket FPGA bitstream conversion](tools/convert-rbf.py)**

## Staged source publication (private; 2026-10-16)

**54 of 77 active Quartus HDL files have been uploaded and independently Git-blob-hash verified against immutable upstream evidence or the frozen local CP48AY audit.** This is not yet an independently buildable source checkout.

- **35 Pocket platform HDL** files, reused exactly from the [previously published Macross Ver.26 source](https://github.com/augustinwinter/openfpga-nmk16/tree/codex/publication-bootstrap); original notices preserved.
- **3 additional unchanged Ver.26 HDL**: FX68K's `uaddrPla.sv`, JT03 and JT6295. Original GPL/JT grants and FX68K `microrom.mem`/`nanorom.mem` are present; see [FX68K provenance](reference/rtl/third_party/fx68k/UPSTREAM.md).
- **13 additional unchanged NMK16 MiSTer HDL**: memory/cache controls, NMK112/IRQ, savestate park, FX68K ALU and original generated T80 Verilog; the upstream GPLv3 text is preserved.
- **3 one-line JT RAM mapping adaptations**, byte-for-byte reconstructed and hash verified against CP48AY local results.
- **T80 original source closure:** 13 pinned VHDL files, README/redistribution notice, QIP, GHDL compatibility patch, documentation, and the original reference generator script. The generator script still expects the **upstream** directory layout and is not certified as a local Macross II build command.

**[SOURCE_PUBLISHING_STATUS.md](SOURCE_PUBLISHING_STATUS.md)** records the 23 still-missing active HDL files and distinct vendor/source rights blockers. The one-shot, **private-repository-only** Mac importer [tools/publish-private-source.py](tools/publish-private-source.py) verifies eight modified HDL hashes and transfers those plus eight project-specific HDL and three ROM-free Quartus configuration files from the user's frozen local source. It does not upload ROMs, original artwork, proprietary vendor files or bitstreams. GitHub uploads have not changed the frozen FPGA build or Pocket SD card.

No public GitHub release or repository visibility change is authorized by this staged upload.

The project does **not** distribute copyrighted Macross II arcade game ROMs, timing PROM dumps, or uncleared original artwork. Owners must obtain required game data lawfully and assemble it locally. The reproduction guide lists all ten ROM chips with sizes, fixed offsets and SHA-256 checksums, and explains what still needs to be supplied for public release. It also identifies outstanding source and Quartus reproducibility work. Do not confuse the current documentation with a complete public RTL source release.

## Expected Pocket installation

```text
Cores/August.Macross II/
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
Assets/nmk16_m2/common/macross2.rom
Assets/nmk16_m2/common/macross2_vprom.bin
```

The **ZIP root** (when a release is legally and technically cleared) must contain `Cores/`, `Platforms/` and `Assets/` directly. The internal core shortname and folder both use **Macross II** with a space. The platform identifier is `nmk16_m2`.

The working Pocket ROM is **10,223,616 bytes**, SHA-256 `2f6861637fa28a283a002d67982a67195eb93c33825a2661af2cebf421cf775d`. Its separately loaded **256-byte** vertical timing PROM SHA-256 is `82c14315be8bce00e93f92d9cf323bdd58c4d760b6ae983d4a3784e178c5272d`. See [REPRODUCING.md](REPRODUCING.md) before constructing or installing assets.

## Engineering baseline

- Known-good Pocket bitstream: `bitstream.rbf_r`, **1,949,788 bytes**, SHA-256 `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87`.
- Corrected private, **ROM-containing** local 14-file package: `August.Macross-II_0.14.0-beta.1_2026-10-15.zip`, SHA-256 `501ecf3cb2b6723f2a1e774141c5e0f68ab2374738b3a01e5e50a9cedea16cba`. This package is **not** suitable for unrestricted public upload.
- Hardware checkpoint: clean installation, corrected core name, banner presentation and direct Arcade launch **PASS**.
- Platform discovery issue fixed: obsolete `nmk16_m2_test` references in Pocket menu caches required a five-cache invalidation; the procedure is recorded under troubleshooting in the reproduction guide.
- Local source/third-party-license audit remains necessary before uploading release HDL or binaries. Do not treat existence of third-party GPLv3 files as proof that all source-level obligations have been met.

## Release process

Before publishing: complete source provenance/licensing review, publish reproducible Quartus build instructions and required source, validate public banner replacement or authorization, and test a **ROM-free** release package with user-supplied assets. Only then attach a GitHub Release and request registration through the [openFPGA Library](https://github.com/openfpga-library/analogue-pocket).

## Credits and notices

FPGA project credit: August. Continuity and engineering collaboration included Doctor Lucy van Pelt and Codex Jordan. Original arcade game and associated audiovisual content remain the intellectual property of their respective rights holders. Third-party HDL notices and licensing must be reviewed and preserved before public source or binary release.

Development method: **OBSERVE → PROVE → EXPLAIN → CHANGE → RETEST**. Preserve known-good builds and verification evidence.
