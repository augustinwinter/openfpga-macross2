# CP48BE — External Pocket/Intel source and build closure

**Status (2026-10-16):** private source staging; not yet a source-complete or independently rebuild-verified release.

## GitHub source checkpoint

CP48BD (commit `090a179c2742a2c22f179496aaacd58dcb2b7ec4`) uploaded the locally verified project-authored `rtl/pocket_pll.v`, three top-level Quartus QIPs, their one nested QIP, and an exact SHA manifest. The active HDL now tracked in GitHub is **69 of 77**; the Quartus source list and four QIP files have been transferred. The frozen FPGA, working Pocket beta and private game ROMs were not changed.

## What is held and why

The eight tracked-source gaps are **four Analogue APF HDL files** and **four Intel/Altera-generated HDL files**, previously hash verified by CP48AX/CP48BC:

| Component | Frozen Macross II SHA-256 | Origin and distribution consideration |
|---|---|---|
| `platform/pocket/bsp/pocket/apf_top.sv` | `b24c9c77a28a4b2bb6f2c55cd02baaeb56f19a197370ad797a77bb5c2f2c6d47` | Original Analogue APF header / EULA |
| `platform/pocket/peripherals/io_bridge_peripheral.sv` | `077191434dfd7ca24cce83945788e41b4d0a53f16e34153683d091a7e855806b` | Original Analogue APF header / EULA |
| `platform/pocket/peripherals/io_pad_controller.sv` | `33e27048825c292a7cbeaadb00507aea2d6601719e597890fdd09c41371186f9` | Original Analogue APF header / EULA |
| `platform/pocket/peripherals/core_bridge_cmd.sv` | `7b40163b4682e926dcab455bb8209864d25e4c349631e23c9913a5b91b137ec9` | APF-derived and locally modified (debug transport); exact byte hash proven at CP48AY |
| `platform/pocket/megafunctions/mf_audio_pll/mf_audio_pll_0002.v` | `94df902acb41f1349bf6d4777a2c42ca0191d3b664850beb2937b6869fa6f400` | Intel/Altera PLL module |
| `platform/pocket/megafunctions/mf_audio_pll.v` | `f52a39ef0c865727279c402cd3d734f506496b7a1dc3f5b4d66d78ca30b37259` | Intel/Altera PLL wizard-generated |
| `platform/pocket/megafunctions/mf_datatable.v` | `af996b1eed7a37567b1ace181ff64427ae2f9e8fcf2d730641e8c1bc91278f92` | Intel/Altera dual-port RAM wizard-generated |
| `platform/pocket/megafunctions/mf_ddio_bidir_12.v` | `73674edb40a6314f9b00829942bedcad9e183515bcdbb327095f96401799c536` | Intel/Altera DDR I/O wizard-generated |

The first three APF and four Intel HDL files are **exact blob matches** to the publicly viewable [plasticbugs Pocket template pinned at `c77563fa84bcc5754d5f1f6ba51168e8849f0e1d`](https://github.com/plasticbugs/pocket-core-template/tree/c77563fa84bcc5754d5f1f6ba51168e8849f0e1d). A public upstream copy does **not** by itself create an unrestricted right to relicense/re-upload an original vendor source to this repository.

The original [Analogue EULA (August 14, 2022)](https://assets.analogue.co/pdf/43478bf701eb4905172acbecc3babae9/Analogue%2BEULA%2BAugust%2B14%2B2022.pdf) distinguishes distribution of third-party **Developer Applications**, which it expressly contemplates, from broader restrictions on copying, publishing, distributing or modifying the underlying APF software. Section 1 says applicable **MIT or GPL grants prevail** when inconsistent with the EULA. This leaves a file-by-file question for the modified APF bridge, and does **not** clear blanket source redistribution or automatic GPL relicensing.

Intel-generated modules retain original Intel/Altera IP license statements. Permission to synthesize an Intel-targeted FPGA or ship an ordinary compiled core is not automatically a permission to relicense or upload all generated IP source. The actual applicable Intel Quartus / Intel FPGA IP license requires separate review. **Do not upload these eight withheld HDL or rely on the presence of similar public mirrors alone.**

## Source hydration WITHOUT copying vendor HDL into Git

[tools/hydrate-pocket-vendor.py](tools/hydrate-pocket-vendor.py) retrieves the **seven unchanged files** from the fixed template commit **to the developer's local clone only**. Each downloaded item must match its previously verified Git blob SHA-1 before it is used. It does not write to Git staging or GitHub, and .gitignore excludes these vendor paths.

It requires explicit acknowledgment of applicable upstream terms:

```sh
python3 tools/hydrate-pocket-vendor.py --accept-upstream-licenses
```

**This does not make a full independent build:** the modified Macross II `core_bridge_cmd.sv` has no byte-identical public counterpart, and the project requires `platform/pocket/bsp/pocket/pinouts/system.tcl` as declared in `projects/m2_pocket.qsf`. The template has a `system.tcl` with immutable blob SHA `42534ded84f0dbf3f454f7f4b1b42bc71c43e43c`, but **equality to the Macross II frozen local pinout is not yet proved**. The hydration script can optionally fetch the template version under `--include-template-pinout`, but warns it has not been compared; **do not use that version for a claimed reproduction until independently checked**.

The actual local `core_bridge_cmd.sv` should be made available only through a rights-appropriate, exact-byte mechanism after the APF reuse and modification terms have been resolved. Replacing it with the pristine public APF bridge would alter the verified Macross II functionality.

## Four QIPs and missing auxiliary files

CP48BC found **four existing QIP files**: `mf_audio_pll.qip`, `mf_audio_pll/mf_audio_pll_0002.qip`, `mf_datatable.qip`, `mf_ddio_bidir_12.qip`. Two `MISC_FILE` references target absent `mf_audio_pll.cmp` and `mf_ddio_bidir_12.ppf`. Neither was required by the previously successful saved Quartus synthesis/assembler; they are not asserted to be active HDL dependencies. Do not invent their contents.

## Not finished

A repository with **69/77 tracked active HDL files** is not source complete just because all QIPs are tracked. The Pocket Tcl pinout, all transitive includes/resources and the precise Quartus invocation need final validation. A fresh-clone Quartus compilation and a validated ROM-free core package, then licensing review for any public distribution, remain outstanding. The existing physical Pocket beta is a protected known-good baseline.

No game ROMs, PROM dumps, copyrighted game graphics, raw RBFs, SD contents or unreviewed vendor HDL were uploaded during this checkpoint.
