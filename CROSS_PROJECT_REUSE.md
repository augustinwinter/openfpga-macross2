# Cross-project reuse: Macross Ver.26 → Macross II (CP48AV)

**Status:** cross-repository provenance baseline, **not** a claim that files in the two build trees match. This is a read-only audit plan; **no RTL, licenses or game assets have been copied** from the original Macross repository into Macross II.

## Authoritative comparison points

The original Macross project is [augustinwinter/openfpga-nmk16](https://github.com/augustinwinter/openfpga-nmk16) (public). Its default `main` branch is a release-facing README; the engineering/publication material is on [`codex/publication-bootstrap`](https://github.com/augustinwinter/openfpga-nmk16/tree/codex/publication-bootstrap). The **fixed comparison ref** for our source inventory is `17800b2c7292cecce9169acee4daf2e62914a36e` (138 Git blobs at the inspection checkpoint, 111 files under `modules/` and `platform/`). The commit's actual Git **tree SHA** (used for direct raw tree API retrieval) is `816579cab1863414d87033f03b0a846df0f1ac75`. Keeping an immutable ref prevents updates on the moving branch from changing an audit result.

Key documents already published by the original project:

- [docs/DEPENDENCIES.md](https://github.com/augustinwinter/openfpga-nmk16/blob/codex/publication-bootstrap/docs/DEPENDENCIES.md) — withheld vs distributed dependencies and the actual build limitations.
- [docs/PUBLICATION-BATCH-2.md](https://github.com/augustinwinter/openfpga-nmk16/blob/codex/publication-bootstrap/docs/PUBLICATION-BATCH-2.md) — exact Git blob hashes, SHA-256, upstream revisions, and corrections to earlier clearance.
- [THIRD_PARTY.md](https://github.com/augustinwinter/openfpga-nmk16/blob/codex/publication-bootstrap/THIRD_PARTY.md) and [docs/LICENSING.md](https://github.com/augustinwinter/openfpga-nmk16/blob/codex/publication-bootstrap/docs/LICENSING.md) — attribution model and publication holds.
- [docs/BUILD.md](https://github.com/augustinwinter/openfpga-nmk16/blob/codex/publication-bootstrap/docs/BUILD.md) — Quartus Prime Lite **25.1std.0 Build 1129**, historical Docker image `openfpgaos-quartus-full:latest` (tag **not** a pinned image digest), ROM-free checks.
- [manifests/Stage26-production-source-sha256.json](https://github.com/augustinwinter/openfpga-nmk16/blob/codex/publication-bootstrap/manifests/Stage26-production-source-sha256.json) — proven pattern for a frozen integrity manifest; **do not use Macross Ver.26 file hashes to authenticate Macross II RTL**.
- [Macross 0.26.0 release](https://github.com/augustinwinter/openfpga-nmk16/releases/tag/0.26.0) — Pocket packaging and hardware-validation history; **do not copy game ROM assets or assume its distribution clears the rights for Macross II**.

## Immediately reusable provenance evidence

| Family | Macross Ver.26 evidence | Macross II finding / needed test |
|---|---|---|
| FX68K `microrom.mem` | 19,456 B; SHA-256 `9d13082be0cf4b04bff887e6da23de84f9f2ee4321f3a2576b4f9540615dece6`; upstream `ijor/fx68k` pin `0602ee4627b10f301298f2673d826cdd6baa9327` | **Identical by independently measured Macross II SHA-256 (CP48AR)**. Required Quartus synthesis input, not arcade ROM. |
| FX68K `nanorom.mem` | 23,520 B; SHA-256 `b3998009fb10605e8468cddf22fdd799a9792ba86f449de2e30615cfcefbeece` | **Identical by CP48AR**. Same provenance may be referenced. |
| FX68K GPL license | Published GPLv3 text SHA-256 `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986` | **Identical local SHA-256 (CP48AR)**. Does **not** show that `fx68k.sv` or `fx68kAlu.sv` is unchanged. |
| FX68K source | Original project **withheld modified `fx68k.sv` and `fx68kAlu.sv`** after discovering inaccurate upstream modification notices | Do not transfer clearance. Compare Macross II versions against pristine pinned upstream and project edit history. |
| JT03/JT49/JT6295 | Original publication includes 51 upstream-matched HDL files, original notices, upstream pins `jt12=dc9be7c1...`, `jt49=7f6abfd0...`, `jt6295=7d76b0be...` | **Candidate shared components only** until exact Git blob hash matches Macross II local files. Different source paths and possibly revisions. |
| Pocket template | Original reviewed subset includes 39 MIT/CC0 and ten independently matched GPL files; upstream `plasticbugs/pocket-core-template` pin `c77563fa84bcc5754d5f1f6ba51168e8849f0e1d` | Compare Macross II's **43** active `platform/` HDL files by content; matching an already-reviewed public blob avoids repeating its provenance search. |
| MAME | Original publication records a pinned `mamedev/mame` revision `f34f02505e32c1993c6a782b6814232cbfc74e36` and reviewed BSD-3-Clause emulator source | Hardware-behavior reference only; avoid conflating a C++ reference license with a new HDL module's rights. |
| Quartus | Successful saved Macross flow used 25.1std.0 Build 1129 on container | Macross II flow also used **25.1std.0 Build 1129** on Ubuntu x86_64; reuse general toolchain preparation, but retain **Macross II** QSF, QIPs, clocks, and constraints. |
| Core discovery / Pocket packaging | Original resolved legacy core/platform conflicts and 521×165 banner packaging | Reuse process, not IDs. Macross II's cache invalidation and `nmk16_m2` platform remain distinct. |

Separate Macross II/Z80-only material is covered by [ATTRIBUTION.md](ATTRIBUTION.md): the prior Macross core's **NMK004** should not be substituted for Macross II's **Z80/T80**, which has its own pinned VHDL and GHDL/Yosys translation recipe.

## The correct reconciliation test

Treat the Git blob SHA-1 of a file as a **content hash** (`SHA1(b"blob "+ascii(byte_length)+b"\\0"+file_bytes)`), independent of its path. Compare against the fixed Ver.26 publication tree.

Classify **each active Macross II HDL** and required non-HDL companion as:

1. **EXACT_PUBLISHED_MATCH:** identical bytes to a file on the fixed Macross Ver.26 publication branch. Record the original path, provenance record and any existing license/notice; review the effect of integrating it into Macross II. **This is reused evidence, not blanket license clearance.**
2. **SAME_BASENAME_DIFFERENT_BYTES:** possible related version or modified descendant. Review original pinned upstream commit, local history and actual diff. Do **not** copy the previous project’s license decision automatically.
3. **NO_PUBLISHED_COUNTERPART:** truly project-specific or absent from the *published* Ver.26 subset. Compare against its authoritative upstream source or trace creation; absence from the public subset does **not** prove independent authorship.

**Important:** The original Ver.26 public branch was intentionally **incomplete and not independently buildable**. Lack of a match to its published 138 blobs does not mean the files are unrelated, novel, or privately authored. A broader comparison against the original frozen local source tree and pinned upstreams is needed for those.

Do **not** transfer original Macross's ROM map, original core/project identifiers (`August.Macross`, `nmk16`), 320×224/270° presentation assumptions, build reports, bitstream hashes, or frozen Stage26 HDL manifest as if they belonged to Macross II. The active Macross II FPGA baseline is 77 HDL files and two FX68K microcode memory files; its hardware-tested Pocket bitstream SHA-256 is `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87`.

## CP48AV results — exact local-to-public comparison (2026-10-16)

The user ran a read-only Git blob content-hash comparison from the **actual frozen Macross II Quartus QSF and four recursively resolved QIPs** against the Ver.26 publication tree SHA `816579cab1863414d87033f03b0a846df0f1ac75`. The project had **77 active HDL files** and **6 selected companion files**. Results:

| Classification | Active HDL | Non-HDL companions | Total |
|---|---:|---:|---:|
| **EXACT byte match** | **38** | **6** | **44** |
| Same filename, different bytes | **3** | 0 | **3** |
| No counterpart in the published Ver.26 tree | **36** | 0 | **36** |
| **Total inspected** | **77** | **6** | **83** |

**38 exact HDL:** **35** `platform/pocket/` integration modules and three upstream files:

- `reference/rtl/third_party/fx68k/uaddrPla.sv` ↔ Ver.26 `modules/cpu-fx68k/uaddrPla.sv`
- `reference/rtl/third_party/jt12/hdl/jt03.v` ↔ Ver.26 `modules/jt03/jt03.v`
- `reference/rtl/third_party/jt6295/hdl/jt6295.v` ↔ Ver.26 `modules/jt6295/jt6295.v`

**Six exact non-HDL companions:** `fx68k/microrom.mem`, `fx68k/nanorom.mem`, and four copies of original component GPL `LICENSE` files (FX68K, JT12, nested JT49, JT6295); some identical license bodies occur at multiple Ver.26 source paths. Earlier CP48AR confirms the local memory hashes. A shared license body alone does not identify the licensing status of every surrounding source file.

**Three same-basename, different-byte HDL requiring targeted diffs:**

- `derived/jt12_exprom.v` ↔ `modules/jt03/jt12_exprom.v`
- `derived/jt12_logsin.v` ↔ `modules/jt03/jt12_logsin.v`
- `derived/jt49_exp.v` ↔ `modules/jt49/jt49_exp.v`

**36 HDL absent from the *previously published* Ver.26 snapshot:** `derived/` **5**, `platform/` **8**, `reference/` **14**, `rtl/` **8**, `target/` **1**. **Absence from this partial publication is not evidence of independent authorship.** Some of these exact files may originate from the pre-existing NMK16 MiSTer implementation or from unpublished Ver.26 RTL.

**Consequences:** Reuse the file-specific Ver.26 source-provenance and license evidence for **exact matches**, subject to the original publication's caveats; do **not** silently label all 38 as license-cleared or replace any three modified audio files. Focus new work on resolving remaining source provenance and comparing to upstream.

## Next evidence source: NMK16 MiSTer pinned tree

The [kuzearcade/Arcade-NMK16_MiSTer](https://github.com/kuzearcade/Arcade-NMK16_MiSTer) repository is an additional upstream evidence source, **not a replacement for the tested Pocket RTL**. A GitHub read on 2026-10-16 identified commit `4c9b923a87dcefee27574a8a06361e47e8e9b963`, tree `4a5f1a57bef1b0a02f5879e7defb6b490e33169e`, with **796 tracked blobs**. It contains paths corresponding to previously unmatched modules, including `rtl/tdragon2/tdragon2_core.sv`, `rtl/macross2/video_macross2.sv`, `rtl/nmk112/nmk112.sv`, `rtl/nmk_irq/nmk_irq.sv`, `rtl/rom_cache*`, `rtl/oki_rom_cache.sv`, `rtl/sdram*.sv` and `rtl/third_party_gen/t80/T80s.v`. Those are **candidate related filenames, not yet proven identical local files**. Compare SHA-1 Git blobs against the **fixed** upstream tree before carrying forward attribution or concluding that the Pocket integration modified them.

## Outcome required for closing CP48AV

A read-only inventory report from the actual local **Macross II clean source**, showing exact matches, basename-related versions, and absent published counterparts. Only after reviewing that report should we import the original Macross **license evidence and attribution** for specifically matched components. Never silently copy/source-replace/overwrite active RTL, the private release, or Pocket SD files.

The longer-term reusable pattern applies to other Pocket projects (e.g. Mazinger Z and Tron): maintain a **shared third-party provenance index** keyed by immutable upstream commit and exact content hash, while retaining project-specific license/derivative checks and hardware verification.
