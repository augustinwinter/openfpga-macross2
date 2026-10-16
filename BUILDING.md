# Building the Macross II FPGA core

> **Status: verified local Quartus build configuration, incomplete public-source publication.** This document records the original project's configuration and the proven conversion to Analogue Pocket bitstream format. A fresh third-party checkout **cannot yet be claimed reproducible** because the full, licensed RTL and supporting source tree have not been uploaded here. Do not confuse a successful existing local build with a new, independent clean-room build.

For **legally obtained original ROM/PROM asset construction and SD installation**, see [REPRODUCING.md](REPRODUCING.md). Do not place ROM binaries into Git, public releases, build logs or issue attachments.

## CP48AK–CP48AO verified local baseline

| Setting | Recorded value |
|---|---|
| Quartus project | `projects/m2_pocket.qpf` / `projects/m2_pocket.qsf` |
| Top-level RTL | `apf_top` |
| FPGA | Intel/Altera Cyclone V `5CEBA4F23C8` |
| Quartus | Prime **25.1std.0 Build 1129** Lite Edition |
| Build host (from preserved flow report) | Ubuntu 22, x86_64 |
| Seed | `1` |
| Output location | `projects/output_files/` |
| Active timing file | `projects/m2_pocket.sdc` |
| Pinout Tcl | `platform/pocket/bsp/pocket/pinouts/system.tcl` |
| Source declarations | 73 direct HDL, 4 more from QIP = **77** active HDL files |
| QIP closure | 3 direct QIPs, 1 nested QIP, no missing declared HDL/QIPs |
| Missing auxiliary declarations | `mf_ddio_bidir_12.ppf` and `mf_audio_pll.cmp` (`MISC_FILE` only) |
| Quartus flow | Successful, including assembler; 0 assembler errors and warnings |
| Timing | Positive reported slacks; detailed applicability and CDC qualification are separate issues |

### Mandatory FX68K CPU microcode memory files (CP48AQ-2)

In addition to the 77 directly declared HDL sources, the synthesis requires **two non-HDL memory initialization files** loaded unconditionally by `reference/rtl/third_party/fx68k/fx68k.sv` (approximately source lines 2496 and 2507):

| Required file | Bytes | Location in verified source tree |
|---|---:|---|
| `microrom.mem` | 19,456 | `reference/rtl/third_party/fx68k/microrom.mem` |
| `nanorom.mem` | 23,520 | `reference/rtl/third_party/fx68k/nanorom.mem` |

The original QSF contains `SEARCH_PATH ../reference/rtl/third_party/fx68k`. The preserved successful `m2_pocket.map.rpt` explicitly lists **both files** as `Auto-Found Unspecified File` at `/build/reference/rtl/third_party/fx68k/`. Both files were also found at the local source root during inspection; do not silently choose a duplicate before comparing its checksum/content with the version in `reference/`.

These are **FX68K processor-internal microcode files**, not copyrighted Macross II game ROM dumps. Include the appropriate upstream files and applicable license/attribution in any complete FPGA source publication; do not omit them just because they are not listed as QSF `*_FILE` assignments.

**CP48AR verified canonical and root duplicates are byte-identical** and present in the successful Quartus mapping report:

| File | Size | SHA-256 |
|---|---:|---|
| `reference/rtl/third_party/fx68k/microrom.mem` | 19,456 | `9d13082be0cf4b04bff887e6da23de84f9f2ee4321f3a2576b4f9540615dece6` |
| `reference/rtl/third_party/fx68k/nanorom.mem` | 23,520 | `b3998009fb10605e8468cddf22fdd799a9792ba86f449de2e30615cfcefbeece` |

The local FX68K `README.md` credits **Jorge Cwik (2018)**, with a `LICENSE` file present (GPLv3). Document the upstream origin and preserve the original notices; the source's redistribution review is still open for the overall project. The root-level duplicate files are not additional distinct source inputs.

The **232** HDL files seen in the broader local source tree include reference and other material; this count must **not** be mistaken for the set compiled by the actual project. The current active-HDL count is based on direct QSF declarations and recursive QIP traversal. Included `\`include` references, non-file Tcl side effects, implicit generated-IP requirements and full license provenance need further independent inspection before claiming absolute dependency closure.

### Project-file relationships

The local source tree has:

```text
projects/m2_pocket.qpf
projects/m2_pocket.qsf
projects/m2_pocket.sdc                 # active, assigned by QSF
platform/pocket/bsp/pocket/pinouts/system.tcl
platform/pocket/megafunctions/mf_ddio_bidir_12.qip
platform/pocket/megafunctions/mf_datatable.qip
platform/pocket/megafunctions/mf_audio_pll.qip
platform/pocket/megafunctions/mf_audio_pll/mf_audio_pll_0002.qip
```

The additional `platform/pocket/bsp/pocket/sys_constr.sdc` exists but was **not** the directly assigned SDC for this proven build; substituting it would create a different configuration.

The four generated IP components reference Verilog sources already found in the preserved tree. Two `MISC_FILE` entries point at absent, non-HDL files (`.ppf` and `.cmp`). The successful Quartus flow did not require those files to produce the verified RBF, but a redistributable source release should explain or restore them if appropriate instead of generating invented replacements.

## CP48BF pinout and local-only vendor hydration (2026-10-16)

The Pocket pinout `platform/pocket/bsp/pocket/pinouts/system.tcl` **was independently proved byte-exact** against the pinned `plasticbugs/pocket-core-template` version (Git blob `42534ded84f0dbf3f454f7f4b1b42bc71c43e43c`, SHA-256 `e30e3c804a31aa38f9de8bb6c184f8dea0868b86c03eda4131f5d00ef0034a95`). It can be safely fetched under its original upstream license for local Pocket development; that does not authorize blanket source redistribution.

Run `tools/hydrate-pocket-vendor.py --accept-upstream-licenses --include-local-bridge` from the source checkout **only if** you have the protected original frozen Macross II source and have reviewed the upstream terms. The command retrieves seven unchanged vendor HDL files and this pinout at a fixed upstream commit, and independently copies the exact CP48AY-modified APF bridge from the original local source. All eight vendor HDL plus pinout remain untracked/ignored, rather than distributed in GitHub. Run `tools/audit-quartus-closure.py` to verify declared-source existence and hashes before attempting the documented Quartus command. The closure audit and a fresh build are **not yet executed/verified**.

## Rebuilding on an appropriate host

These commands reconstruct the **recorded build invocation** once the complete source tree has been legally published or otherwise made available. They have **not** been rerun from a fresh public checkout:

1. Obtain the correct Quartus Prime 25.1std.0 Lite Edition build and its Cyclone V device support from the vendor, in a compatible **x86_64 Linux** environment. The original report identifies Ubuntu 22. Merely having a different Quartus version may alter IP handling, fitter decisions, timing and bitstream hashes.
2. Obtain the **full, legally redistributable project source** and confirm the paths above exist relative to its source root. Do not assume a repository containing only this guide is compilable.
3. Make Quartus executables available on `PATH`, or invoke them through their installed absolute paths.
4. From the directory **containing the `m2_pocket.qpf` and `m2_pocket.qsf`**, run:

```bash
cd projects
quartus_sh --flow compile m2_pocket
```

The preserved compilation report records these phases (Quartus orchestrates them through its flow): `quartus_map`, `quartus_fit`, `quartus_asm`, `quartus_sta` and `quartus_eda`.

Check the new `projects/output_files/m2_pocket.flow.rpt`, `m2_pocket.fit.summary`, `m2_pocket.sta.summary` and `m2_pocket.asm.rpt`. A successful command is **not** sufficient to conclude the resulting timing margins, CDC behavior or hardware functionality match the verified baseline. Preserve full reports and inspect errors, warnings, clock constraints and minimum slacks before deployment.

## Convert the raw FPGA bitstream for Pocket

The CP48AN audit established that **reversing the bit order of each byte** of the raw Quartus RBF yields the exact previously tested Pocket `.rbf_r`. This is not a whole-file byte reversal. A version-controlled, standard-library-only converter is available as [tools/convert-rbf.py](tools/convert-rbf.py).

From the repository/source root **after Quartus compilation**, the documented command is:

```bash
python3 tools/convert-rbf.py \
  projects/output_files/m2_pocket.rbf \
  bitstream.rbf_r
```

The converter refuses to overwrite its output. The independently verified 2026-10-15 reference artifacts are:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Quartus `m2_pocket.rbf` | 1,949,788 | `23f96994feac9bae4c94bbf616fa1e6f9272b06c2a2d9dd70bf28eeab9160875` |
| Converted `bitstream.rbf_r` | 1,949,788 | `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87` |

For **the recorded, unchanged source/build environment**, enforce these checks while converting:

```bash
python3 tools/convert-rbf.py \
  projects/output_files/m2_pocket.rbf \
  bitstream.rbf_r \
  --raw-sha256 23f96994feac9bae4c94bbf616fa1e6f9272b06c2a2d9dd70bf28eeab9160875 \
  --output-sha256 93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87
```

These hashes **are reference values, not a guarantee** of bit-for-bit reproducibility on different tool versions or configurations. When experimenting, use a new output path and compare reports instead of overwriting a trusted bitstream.

## Package for Analogue Pocket

The known-good corrected core identity is:

- `core.json` metadata author: `August`
- shortname: **`Macross II`** (space retained)
- core path: **`Cores/August.Macross II/`**
- platform ID: **`nmk16_m2`** (not `nmk16_m2_test`)
- platform name/category: **Macross II / Arcade**

A completed, authorized release package needs the following Pocket files at the ZIP root:

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
Platforms/_images/nmk16_m2.bin      # Rights-cleared image needed for public packaging
Assets/nmk16_m2/common/
  macross2.rom                       # User supplies locally
  macross2_vprom.bin                 # User supplies locally
```

ROM construction and checksums are documented in [REPRODUCING.md](REPRODUCING.md). **Do not publish** the 14-file private local ZIP, because it embeds arcade ROM assets. The known-good private ZIP is `August.Macross-II_0.14.0-beta.1_2026-10-15.zip`, SHA-256 `501ecf3cb2b6723f2a1e774141c5e0f68ab2374738b3a01e5e50a9cedea16cba`. Public packages must exclude non-redistributable assets.

## License, attribution and publication gates

**This documentation is not a license grant for the original game's content or third-party FPGA implementations.**

The active HDL source audit counted 77 declared source files in `derived/`, `platform/`, `reference/`, `rtl/` and `target/`. Of these, **26** have no recognizable copyright/permission header in the first 35 lines and require source-origin review. In particular, inspect derived Thunder Dragon 2 material, NMK RTL, T80, generated PLL/IP, and Pocket integration modules. The reference tree contains GPLv3 license files for some components, including `fx68k`, `jt12`, `jt49` and `jt6295`; determine what corresponding-source and notice obligations apply to the files **actually distributed**. A notice scan alone cannot establish ownership or permission.

Until the following gates close, the repository is **private beta documentation**, not an independently reproducible public FPGA source release:

- Publish all required source HDL, generators/IP definitions, QSF/QPF/SDC/Tcl, and license notices with traceable origins and permissions.
- Audit **indirect** compilation dependencies (includes, memory initialization inputs and generated IP).
- Run a **fresh checkout build** using the published build instructions; save tool versions, resource/timing reports and final hashes.
- Execute this repo's `tools/convert-rbf.py` against an actual checked raw RBF and verify output and Pocket load.
- Test a legal **ROM-free public installer** using the user's own verified ROM/PROM files and appropriately licensed platform image.
- Keep original Macross Ver.26 installation and all preservation evidence separate.

The project's methodology remains **OBSERVE → PROVE → EXPLAIN → CHANGE → RETEST**. For ROM reconstruction and the five-menu-cache reset used to restore Pocket Arcade visibility, see [REPRODUCING.md](REPRODUCING.md).
