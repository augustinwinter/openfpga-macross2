# Source publication status — CP48BA, 2026-10-16

**Status: controlled upload to a PRIVATE GitHub repository.** Macross II is physically playable in the validated Pocket beta, but **this GitHub checkout is NOT yet complete or independently buildable**. No public release is authorized by this status record.

## CP48BD / CP48BE current checkpoint (2026-10-16)

The CP48BD local GitHub push **PASS** at commit `090a179c2742a2c22f179496aaacd58dcb2b7ec4`, transferring `rtl/pocket_pll.v`, four Quartus QIP files, and `manifests/CP48BD-clock-qip.json`. The verified current tally is **69 of 77 active HDL** in the private repository. This supersedes the older CP48BB intermediate `54/77` and conditional `68/77` notes below (retained for provenance).

All **eight still-untracked active HDL** are specifically identified and explained in [VENDOR_SOURCE.md](VENDOR_SOURCE.md): 4 Analogue APF-derived sources (one with important Macross II changes) and 4 Intel/Altera-generated source files. Read the authoritative [Analogue EULA](https://assets.analogue.co/pdf/43478bf701eb4905172acbecc3babae9/Analogue%2BEULA%2BAugust%2B14%2B2022.pdf) for the difference between distributable **Developer Applications** and restrictions around redistributing APF source. A pinned, verified but **local-only** fetch helper [tools/hydrate-pocket-vendor.py](tools/hydrate-pocket-vendor.py) provides the seven unchanged upstream template files without committing them to GitHub, subject to the original licensing terms. The modified APF command bridge cannot be recovered exactly from pristine public source.

**Separate non-HDL dependency:** `platform/pocket/bsp/pocket/pinouts/system.tcl` is declared by the uploaded Quartus QSF but is **not uploaded**. It exists in the public template, yet byte-equality against the proven frozen Macross II version remains to be checked. The already-uploaded four QIPs have `MISC_FILE` references to missing `.cmp`/`.ppf`, which did not prevent the preserved successful Quartus build.

**DO NOT** interpret a physically validated beta or 69/77 tracked HDL as a complete independent rebuild or legal publication clearance. The actual frozen Pocket RTL/bitstream, ROMs and SD card remain untouched.

## CP48BF and CP48BG follow-through

**CP48BF PASS:** the required local Pocket pinout Tcl is **exact-byte identical** to the pinned Pocket template: 45,242 bytes, Git blob `42534ded84f0dbf3f454f7f4b1b42bc71c43e43c`, SHA-256 `e30e3c804a31aa38f9de8bb6c184f8dea0868b86c03eda4131f5d00ef0034a95`. The local-only [vendor hydrator](tools/hydrate-pocket-vendor.py) now fetches this pinout automatically along with seven unchanged vendor HDL, and can optionally copy the verified modified APF command bridge directly from the protected frozen Mac source. These files remain ignored/untracked and are **not redistributed in this GitHub repository**.

A new [read-only Quartus declared-source closure audit](tools/audit-quartus-closure.py) checks the 77 active HDL files, four QIPs, Tcl/SDC, two FX68K microcode inputs, and nine local-only vendor/bridge/pinout hashes. **CP48BG PASS:** the audit ran on the user's hydrated Mac checkout and confirmed all 77 declared HDL, four QIPs, Tcl/SDC, two FX68K memory inputs and nine external-source hashes. The owner declined fresh Quartus synthesis/rebuild, and none was performed.

Current private GitHub source publication remains **69/77 active HDL**. Local hydration can supply remaining dependencies for the owner's private development but is not equivalent to source-code redistribution rights or a public-ready complete package.

## CP48BG user-executed source closure (2026-10-16)

**PASS, declared-source scope only.** The owner ran `tools/hydrate-pocket-vendor.py --accept-upstream-licenses --include-local-bridge` and `tools/audit-quartus-closure.py` on the private Mac checkout: **77/77 active HDL**, **4/4 QIP**, required QSF pinout Tcl + SDC, two checksum-verified FX68K CPU-internal memory files, and **nine** verified APF/Intel/bridge/pinout dependencies. Two absent generated-IP `MISC_FILE` entries (`mf_audio_pll.cmp` and `mf_ddio_bidir_12.ppf`) did not block the earlier Quartus flow. Frozen source and Pocket SD were unchanged, `git status` clean, no vendor HDL staged or pushed.

**Private GitHub inventory** is [ACTIVE-HDL-77.json](manifests/ACTIVE-HDL-77.json): exactly 69 tracked active HDL blobs and eight vendor-origin external-only HDL with local SHA-256 evidence. A read-only inventory verifier is [tools/verify-publication.py](tools/verify-publication.py). This closure result is **not** a fresh Quartus build, a license clearance or a public release. **The owner explicitly declined another build**, so fresh compilation is out of scope.

## CP48BH-3 — private source-preservation phase closed (2026-10-16)

**PASS, confirmed on the owner's Mac and independently checked in GitHub.** The full local Quartus declared-source inventory of **77/77 HDL** and four QIPs passed CP48BG. The private GitHub repository tracks **69 hash-verified active HDL**; eight APF/Intel-origin HDL are intentionally **local-only**, protected by upstream licensing limitations. CP48BH-3 preserved **two distinct historical Pocket metadata configurations** from two qualifying ZIP archives. The actual snapshot folders are `Cores/August.Macross II/` and `Cores/August.MacrossII/`, with **ten** JSON/text files per snapshot. Both `core.json` entries report an **empty version field**, so the snapshot archive does not assert a final canonical version. The SHA-256 and Git blob integrity of all twenty snapshots' files passed `tools/verify-publication.py`.

**GitHub preservation commit:** [`ae8ee35ac53d0cd7478f174a6bf91b8dd076d0c9`](https://github.com/augustinwinter/openfpga-macross2/commit/ae8ee35ac53d0cd7478f174a6bf91b8dd076d0c9). Snapshot manifest: [`manifests/POCKET-METADATA-SNAPSHOTS.json`](manifests/POCKET-METADATA-SNAPSHOTS.json). No game ROM/PROM, copyrighted artwork, archived ZIP, FPGA RBF/SOF, or SD-card contents were uploaded. The frozen original source, proven Pocket bitstream and SD card are unchanged. The owner explicitly **skipped a fresh FPGA rebuild**; none was conducted.

**Private publication / evidence preservation: COMPLETE. Public source-and-binary release: BLOCKED** by remaining APF/Intel source redistribution permission questions, contributor/project licensing decisions and release/package artwork/asset clearance. Nothing was automatically marked final beta or made public. No routine FPGA work or new test is required for the completed private preservation stage.

## Verified contents

The active Quartus source closure (CP48AO) comprises **77 HDL files** (73 directly listed by QSF plus four QIP dependencies), as well as non-HDL dependencies. Cross-project audits CP48AV/CP48AW/CP48AX/CP48AY established: **58** exact upstream HDL files, **11** locally modified upstream descendants, **8** project-specific HDL files.

An independent post-upload GitHub Git-tree comparison of the private `main` branch against pinned sources established:

| Source category | Active HDL uploaded and hash-verified | Notes |
|---|---:|---|
| Previously published [Macross Ver.26](https://github.com/augustinwinter/openfpga-nmk16/tree/17800b2c7292cecce9169acee4daf2e62914a36e) | **38** | 35 unmodified Pocket platform HDL, `uaddrPla.sv`, `jt03.v`, `jt6295.v`. |
| Additional exact [NMK16 MiSTer](https://github.com/kuzearcade/Arcade-NMK16_MiSTer/tree/4c9b923a87dcefee27574a8a06361e47e8e9b963) | **13** | Includes ROM caches, NMK devices, FX68K ALU, savestate and exact 605,568-byte generated `T80s.v`. |
| Locally modified JT LUT files, **exact local Git blob hashes independently matched** | **3** | `derived/jt12_exprom.v`, `jt12_logsin.v`, `jt49_exp.v`; one `(* ramstyle = "logic" *)` attribute per file. |
| **Total active HDL currently uploaded** | **54 of 77** | Byte hashes verified against immutable upstream references or the user's CP48AY local audit. |

Additional preservation materials already uploaded include original FX68K `microrom.mem` and `nanorom.mem` (synthesis dependencies), FX68K license/grant, JT source licenses, NMK16 upstream GPLv3 text, **13 original T80 VHDL files plus its README and QIP**, the upstream `ghdl-compat.patch`, GHDL-Yosys toolchain documentation and a **verbatim upstream reference generator** at `tools/upstream/gen_t80_verilog.sh`. The latter still assumes the upstream MiSTer directory layout and **has not** been adapted or executed as a Macross II build helper. The T80 original local `T80-master` source has some different revisions/sizes; this project retained the source that exactly matches the pinned NMK16 MiSTer lineage, not a guessed replacement.

## Remaining 23 active HDL (not uploaded)

### Eight known upstream-modified Macross II source files — exact content only on user's Mac

- `derived/sdram.sv`
- `derived/sdram_arb.sv`
- `derived/sdram_req.sv`
- `derived/tdragon2_core.sv`
- `derived/video_macross2.sv`
- `reference/rtl/third_party/fx68k/fx68k.sv`
- `platform/pocket/peripherals/core_bridge_cmd.sv`
- `target/pocket/core_top.sv`

The CP48AY diffs show SDRAM capture/ack/timing changes, NMK CPU bus behavior, sprite storage, FX68K instrumentation, Pocket bridge command handling, and main Pocket wrapper adaptations. These are **not safe to replace with upstream originals**. They need to be copied exactly from the frozen local source tree, with modification/provenance notices and relevant upstream licenses retained.

### Eight Macross II project-specific HDL files — exact content only on user's Mac

- `rtl/m2_apf_loader.sv`
- `rtl/m2_audio_cdc.sv`
- `rtl/m2_gameplay_video.sv`
- `rtl/m2_main_sdram.sv`
- `rtl/m2_memory.sv`
- `rtl/m2_pocket_machine.sv`
- `rtl/m2_prom_guard.sv`
- `rtl/pocket_pll.v`

Record authorship, derivative-source provenance, and licensing before any public release.

### Seven pinned Pocket-template source files awaiting terms review

Identical counterparts exist at [plasticbugs/pocket-core-template `c77563fa84bcc5754d5f1f6ba51168e8849f0e1d`](https://github.com/plasticbugs/pocket-core-template/tree/c77563fa84bcc5754d5f1f6ba51168e8849f0e1d):

- `platform/pocket/bsp/pocket/apf_top.sv`
- `platform/pocket/peripherals/io_bridge_peripheral.sv`
- `platform/pocket/peripherals/io_pad_controller.sv`
- `platform/pocket/megafunctions/mf_audio_pll/mf_audio_pll_0002.v`
- `platform/pocket/megafunctions/mf_audio_pll.v`
- `platform/pocket/megafunctions/mf_datatable.v`
- `platform/pocket/megafunctions/mf_ddio_bidir_12.v`

The three APF files contain **Analogue's own EULA-based Software License Agreement**; the other four are Intel/Altera-generated FPGA IP. Being public in someone else's template does not automatically grant this project permission to republish them under an arbitrary open-source license. The [Analogue EULA](https://www.analogue.link/pocket-eula) and the applicable Intel FPGA IP agreements need review; **do not substitute a blanket GPL declaration** for the original vendor terms. Regenerating vendor output locally may be the appropriate documented solution. These files are intentionally held pending specific authorization or regeneration-path confirmation.

## Automated local import: safely scoped CP48BB

The repository includes [tools/publish-private-source.py](tools/publish-private-source.py), a guarded one-shot importer intended to run **locally** from a fresh clone on the user's Mac. It copies only **14** verified ROM-free files (**seven** locally modified upstream HDL with verified CP48AY Git blob hashes, plus **seven** project-specific HDL) and **three** `projects/m2_pocket.qpf/.qsf/.sdc` configuration files. It preserves frozen input source, creates an import SHA-256 manifest, checks GitHub remains private via authenticated `gh`, and commits/pushes only whitelisted paths. **It has not been executed against the user's Mac.**

Two additional local source files remain **excluded from this automatic transfer** despite the prior "local-only 16" inventory:

- `platform/pocket/peripherals/core_bridge_cmd.sv` — its upstream counterpart retains **Analogue's APF Software License Agreement**, not a generic MIT/GPL header; requires the same redistribution review as the three unchanged APF files.
- `rtl/pocket_pll.v` — creation/license nature (project wrapper versus Intel-generated material) not yet established; source inspection required before any transfer.

Once CP48BB runs and independently confirms all input/output hashes, the active HDL upload count **could** increase from 54 to **68**, leaving **nine** held sources (four APF-related, five Intel/PLL-related) plus QIP/build-support closure. This conditional count is **not** a claim that the import has already happened. A complete source checkout remains unavailable until the vendor/APF holds are resolved.

## Further requirements before complete independent build

Besides the remaining HDL, the private repository still needs the **actual tested local Quartus `projects/m2_pocket.qpf`, `projects/m2_pocket.qsf`, `projects/m2_pocket.sdc`, all four QIPs and their file dependencies, BSP pinout Tcl, approved project-specific scripts, ROM-free Pocket metadata, and ROM-independent tests**. Only copy sources from the proven frozen local `scratch/CP48-clean-macross2/source`. Do not replace the source with unmodified MiSTer versions. The existing `tools/convert-rbf.py` and `tools/assemble-rom.py` are already committed.

**Private game assets must remain absent:** `macross2.rom`, `macross2_vprom.bin`, individual original arcade ROM dumps and archives, copyrighted original game banner/artwork, preserved execution traces, released private ROM-containing ZIPs, and SD-card contents. The target repository stays private until complete source/licensing and public-safe ROM-free packaging have been verified.

A successful existing Quartus compile and physically verified Pocket beta are **not** proof that a fresh checkout of this incomplete repository rebuilds or passes timing. Reproduction should be independently tested under Quartus Prime Lite 25.1std.0 Build 1129 (Ubuntu x86_64, target 5CEBA4F23C8, seed 1) once the required rights-cleared source closure is available.

## Provenance comparison references

- `augustinwinter/openfpga-nmk16` commit `17800b2c7292cecce9169acee4daf2e62914a36e`, tree `816579cab1863414d87033f03b0a846df0f1ac75`.
- `kuzearcade/Arcade-NMK16_MiSTer` commit `4c9b923a87dcefee27574a8a06361e47e8e9b963`, tree `4a5f1a57bef1b0a02f5879e7defb6b490e33169e`.
- `plasticbugs/pocket-core-template` commit `c77563fa84bcc5754d5f1f6ba51168e8849f0e1d`, tree `d42817778bca63191e21509fc43135f9ce01d2f1`.

See [BUILDING.md](BUILDING.md), [CROSS_PROJECT_REUSE.md](CROSS_PROJECT_REUSE.md), and [ATTRIBUTION.md](ATTRIBUTION.md). **Upload status is an inventory statement, not blanket copyright/licensing clearance.**
