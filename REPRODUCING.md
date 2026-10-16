# Reproducing Macross II for Analogue Pocket

**Project:** Super Spacefortress Macross II (Japanese arcade ROM set `macross2`) / NMK165 / Analogue Pocket openFPGA  
**Verified installation:** `Macross II`, core version `0.14.0-beta.1`, platform ID `nmk16_m2` (2026-10-15).  
**Status:** ROM/PROM assembly independently reproduced and byte-verified at checkpoint CP48AJ; the clean core, title art and gameplay were tested on a real Pocket. **Complete public source/build reproduction is not yet available**; see [remaining publication work](#remaining-publication-work). Do not mistake a verified ROM procedure for a verified from-source FPGA rebuild.

### Existing verified build, no further FPGA recompilation

The project owner elected to **skip a fresh Quartus rebuild**. The existing tested `bitstream.rbf_r` is the protected reference; ROM-free metadata can be recovered from historical packages using [`tools/import-pocket-metadata.py`](tools/import-pocket-metadata.py), which neither rebuilds nor uploads the bitstream. The importer must record the exact existing metadata version; a historical RC1 package is not automatically a newly tested beta. The publication is still **private** pending the source/vendor licensing and game-art rights documented in [`RELEASE_READINESS.md`](RELEASE_READINESS.md).
## 1. What you need and what cannot be redistributed

You need (a) an Analogue Pocket and microSD card; (b) a legally obtained, correctly dumped **Japanese `macross2` arcade ROM set** with the specific ten files below; (c) an authorized openFPGA core distribution and its `bitstream.rbf_r`, metadata and platform support files; and (d) platform art where licensed for redistribution, or an image you have the right to use.

**Neither game ROMs nor original game artwork are distributed by this repository.** Obtain game data legally, for example from original hardware you own and are entitled to dump, or an appropriately licensed source. We provide ROM filenames, hashes and construction tools for verification, **not ROM download sites or a claim that possession of a ROM is authorized in any jurisdiction**.

The repository must also comply with licenses for third-party HDL before source/binaries can be publicly published. Parts of the engineering reference tree contain GPLv3 licenses (including `fx68k`, `jt12`, `jt49` and `jt6295`). Their inclusion and obligations in the actual release source tree require auditing; copyright notices, complete corresponding source, and any required license text must not be omitted.

## 2. Verify the ten original arcade ROM components

The required filenames, byte lengths and SHA-256s were verified directly from the user's authenticated `inputs/macross2.zip` during CP48AJ, and were also recorded by the original reconstruction manifest. The archive must contain **these exact files**, not just a similarly named bootleg, export, or alternate revision. Archive container SHA may vary with compression; the checks below are for each ROM member.

| File | Bytes | ROM stream offset | SHA-256 |
|---|---:|---:|---|
| `mcrs2j.3` | 524,288 | `0x000000` | `dae74e32833043a8e45cb7317ccbdba926e0a3e59f9bbd8c94f8b78e0673ea8e` |
| `mcrs2j.2` | 131,072 | `0x080000` | `021648bb1e23d8624dcbc76bde0c69e9b7fe1b05aeab4f51988c8f5d2bac3043` |
| `mcrs2j.1` | 131,072 | `0x0A0000` | `ef72d7ed45462d2f39a0b5e2a3935b71633644f59c023eb05f1935afd742c0db` |
| `bp932an.a04` | 2,097,152 | `0x0C0000` | `f122a49d5fa10611b28a8fab675715a0136cc6f95054da44288eeb8d966758a8` |
| `bp932an.a07` | 2,097,152 | `0x2C0000` | `4501b7dfb9be413ac9fe9c812da9ba15dc04af91a5560e19c89b38c27cd8ef7d` |
| `bp932an.a08` | 2,097,152 | `0x4C0000` | `6adc119a564bfe04e7da0eb90449391679276f94460a5020145e3f7b1b0d6bae` |
| `bp932an.a06` | 2,097,152 | `0x6C0000` | `6a48da61287692badf906359d1d0a241b47f978c7be8d31736e8206d3b5dc869` |
| `bp932an.a05` | 1,048,576 | `0x8C0000` | `2ea8a1f9820e24195621ab3b939bdc7d2a0cb39c8b85ad3853fe182c6964a1c3` |
| `mcrs2bpr.9` (horizontal PROM) | 256 | `0x9C0000` | `09caf4d9d3b969e9439ce845d35b7dde21f44335d97a75a631a03dd00e8bc1cf` |
| `mcrs2bpr.10` (vertical PROM) | 256 | `0x9C0100` | `82c14315be8bce00e93f92d9cf323bdd58c4d760b6ae983d4a3784e178c5272d` |

The eight main sections are concatenated **without byte swapping, deinterleaving, or other transformation**. Absolute offsets above are contiguous. The full *archival* image then appends horizontal and vertical PROM data in that order; this is a preservation convention, **not** an assertion that the Pocket loads both PROMs from the ROM data slot.

## 3. Assemble Pocket ROM assets locally (Python 3, standard library)

From the root of a checked-out repository, put your **own** ROM ZIP at a path of your choice and run:

```bash
python3 tools/assemble-rom.py --romset "/path/to/your/macross2.zip" --out-dir "./my-macross2-assets"
```

This tool refuses incorrect sizes or SHA-256s and will not overwrite existing output files. It produces only:

```text
my-macross2-assets/macross2.rom
my-macross2-assets/macross2_vprom.bin
```

Use `--archival` only if you also want `macross2-archival.rom`, the 10,224,128-byte preservation image with both PROMs appended. **Never substitute the larger archival file for the Pocket's `macross2.rom`**: `data.json` requires exactly `0x009C0000` bytes.

Verified results:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `macross2.rom` | 10,223,616 (`0x9C0000`) | `2f6861637fa28a283a002d67982a67195eb93c33825a2661af2cebf421cf775d` |
| `macross2_vprom.bin` | 256 | `82c14315be8bce00e93f92d9cf323bdd58c4d760b6ae983d4a3784e178c5272d` |
| Horizontal PROM (checked but *not* separately loaded by this Pocket core) | 256 | `09caf4d9d3b969e9439ce845d35b7dde21f44335d97a75a631a03dd00e8bc1cf` |
| `macross2-archival.rom` (optional) | 10,224,128 | `b1ceb2e188aad2babe18336fc6dd9a70aef623da4b079c4f81b4549e8d5d17cf` |

The original engineering archive used `mk_ioctl_stream.py`; its verified effect for this game is the identical fixed-offset raw-copy layout. An older package README mentioned `tools/prepare-rom.py`, **but that file did not exist in the inspected working source**; do not follow that stale reference. The checked-in `tools/assemble-rom.py` is intended to replace it and must undergo independent end-to-end execution before a public release.

## 4. Install the core and assets on the Pocket SD card

The *core distribution* (when cleared for release) must supply the following files. The two ROM/PROM files are **not included in a public ROM-free package**; populate them from step 3. The platform image may also need to be supplied separately if its rights have not been cleared.

```text
<SD ROOT>/
  Cores/
    August.Macross II/
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
  Platforms/
    nmk16_m2.json
    _images/
      nmk16_m2.bin                 # See artwork section
  Assets/
    nmk16_m2/
      common/
        macross2.rom             # Generated from YOUR original ROMs
        macross2_vprom.bin       # Generated from YOUR original ROMs
```

The `core.json` metadata **shortname must be `Macross II`** and the core directory must be `August.Macross II` (with a space); `platform_ids` remains `["nmk16_m2"]`. The `Platforms/nmk16_m2.json` platform is named **Macross II** in category **Arcade**, year **1993**, manufacturer **Banpresto / NMK**. Ensure the entire distribution starts with `Cores/`, `Platforms/`, and `Assets/` at ZIP root—there must be no extra outer directory.

The working `data.json` loads:
- `macross2.rom`, data slot 0, exact size `0x009C0000`, target address `0x10000000`.
- `macross2_vprom.bin`, data slot 1, exact size 256, target address `0x00000000`.

Do not install legacy `nmk16_m2_test` definitions, TEST13/SPIC cores, or old `Settings/August.MacrossII` directories unless intentionally troubleshooting a distinct archived version. Original Macross Ver.26 is a **separate** core and must not be removed or modified.

## 5. Platform banner and image rights

The physically verified private installation uses `Platforms/_images/nmk16_m2.bin`, a **171,930-byte** binary corresponding to a **521×165** 16-bit-style Pocket banner. Its SHA-256 is `63c69d1169ab5aef8cd9465dde82e0b7db793ef72893b4d942d72dbeee1315c3` (private baseline). The originating illustration was a **522×165 JPEG**, locally named `macrossII_arcade_banner.jpg`; it is **not provided in this repository** and must not be presumed redistributable.

The private conversion cropped one column, converted to grayscale, rotated the pixels counterclockwise and emitted two bytes per destination pixel. To reproduce the same specific banner byte-for-byte, the **identical original input JPEG and a separately verified image conversion script** are needed. Independent artwork can also be used if licensing permits. A tested reproducible banner-generation tool remains **pending**; this is not yet a fully solved public asset dependency.

## 6. Hardware evidence and troubleshooting

Verified on physical Analogue Pocket after the CP48AF naming correction: menu shows **Macross II** under **openFPGA → Arcade** with expected banner; **Developer → Builds** shows **Macross II 0.14.0-beta.1**; the game launches and plays. The known good bit-reversed Pocket FPGA file `bitstream.rbf_r` is **1,949,788 bytes**, SHA-256:

```text
93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87
```

The Pocket did initially show the core in **Developer → Builds** (and it played), but no entry under Arcade. We found a stale `nmk16_m2_test` reference in `System/platforms_cache.bin` after migrating to platform ID `nmk16_m2`. Removing only `cores_cache.bin` and `corelist_cache.bin` did **not** fix it. After backing up and invalidating **all five** indexes and fully rebooting the Pocket, Arcade visibility returned.

If the core is playable from Builds but missing from Arcade: first validate `core.json`, `Platforms/nmk16_m2.json` and the ID; then back up and (only if needed) remove these **five files in `<SD ROOT>/System/`** while the card is mounted on a computer:

```text
cores_cache.bin
corelist_cache.bin
platforms_cache.bin
core_viewby_platform.bin
platform_viewby_category.bin
```

Eject safely and **fully power off and restart** the Pocket; it regenerates menu indexes. Do not delete the `System` directory, other system data, game assets, save files, or unrelated cores. This procedure is based on the project's tested Pocket OS 2.7 recovery; it may differ on later firmware.

If game assets are absent: confirm the filenames, sizes, checksum and directory spelling exactly. If the core is absent even from Builds: confirm `Cores/August.Macross II/core.json` and the FPGA file are installed. Never try to fix a missing menu entry by rebuilding a working FPGA bitstream.

## 7. Release checksums and non-distribution of the private archive

The user's **personal, ROM-containing** 14-file baseline was verified on 2026-10-15 with the corrected core name. Its archive name and SHA-256, for private integrity comparison only:

```text
August.Macross-II_0.14.0-beta.1_2026-10-15.zip
SHA-256 501ecf3cb2b6723f2a1e774141c5e0f68ab2374738b3a01e5e50a9cedea16cba
```

**This archive is not approved for public redistribution**; it contains copyrighted arcade game data. A future public archive must be reconstructed *without* protected ROMs and without uncleared artwork, while preserving expected layout and user-assembly instructions.

## 8. Remaining publication work

This document enables exact recreation of **game ROM and vertical PROM assets**. The following still must be finished to support the stronger promise of a complete independently reproducible *FPGA* project:

1. **Publish auditable, licensed HDL and complete corresponding source**. The local clean design contains 232 HDL files across sources/references; public attribution and dependency selection have not been completed. Verify GPLv3 and any other licenses before public binary distribution.
2. **Publish exact Quartus project files and reproducible command sequence**: version, target device, pin constraints, PLL configuration, seed, source manifests, compile commands, Pocket bitstream reversal/packaging, and output hashes. Prior local compilation and reported positive timing margins are not yet a published reproducible build recipe.
3. **Prove the published assembler as invoked above** against user-owned source files, not only the earlier in-memory reconstruction proof.
4. **Prove a rights-cleared banner workflow**, or provide a public-domain/original-art alternative, then verify on actual Pocket hardware.
5. **Prepare ROM-free public package** and test a clean installation in which the user adds locally reconstructed assets; review generated release ZIPs for accidental copyrighted ROM inclusion.
6. Only after licensing, source and hardware release checks: publish a versioned GitHub Release and request listing via the [openFPGA Library](https://github.com/openfpga-library/analogue-pocket).

For Pocket packaging format, see [Analogue's openFPGA developer documentation](https://www.analogue.co/developer/docs/openfpga/packaging-a-core). Preserve all clean reference checkpoints and evidence; **OBSERVE → PROVE → EXPLAIN → CHANGE → RETEST**.

**No copyrighted game ROM, proprietary arcade source, or original game artwork is included in this repository.**
