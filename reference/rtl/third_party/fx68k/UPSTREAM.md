# FX68K upstream companion files — verified source batch

**Source:** [Macross Ver.26 publication snapshot](https://github.com/augustinwinter/openfpga-nmk16/tree/17800b2c7292cecce9169acee4daf2e62914a36e/modules/cpu-fx68k) (public commit `17800b2c7292cecce9169acee4daf2e62914a36e`), previously audited against [ijor/fx68k](https://github.com/ijor/fx68k) at immutable upstream commit `0602ee4627b10f301298f2673d826cdd6baa9327`; see [original publication-batch record](https://github.com/augustinwinter/openfpga-nmk16/blob/codex/publication-bootstrap/docs/PUBLICATION-BATCH-2.md).

These **five** files have been transferred to the Macross II tree **without modifying their contents**. Blob SHA-1 below is Git's *blob-object hash*, not the SHA-1 of the bare file data.

| File | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `LICENSE` | `f288702d2fa16d3cdf0035b15a9fcbc552cd88e7` | `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986` |
| `fx68k.txt` | `b9c3c5a4dced49ff317d05736176fa4bf2632f2d` | `2a7d451e8f7ae8683e4ec4f40a9b3adf91fb5c8b5d569c0f4cdb2b5de090811d` |
| `microrom.mem` | `22558e867b7b1665a5e605ce1b53c5cdf392d5d3` | `9d13082be0cf4b04bff887e6da23de84f9f2ee4321f3a2576b4f9540615dece6` |
| `nanorom.mem` | `df7d74d970220878da97d5082590999cc2d171b2` | `b3998009fb10605e8468cdd799a9792ba86f449de2e30615cfcefbeece` |
| `uaddrPla.sv` | `e24e951e3fb643a1894f278237aec2bc5b281375` | `07ceb3b1fbbd74f255c2a909151fe5efd38a575ba4f6aa47c6208050d2e27326` |

The memory files are **FX68K internal CPU microcode**, not Macross II game dumps. CP48AQ-2 and CP48AR verified Quartus locates them through the existing FX68K `SEARCH_PATH` and that the clean Macross II source matches these two hashes.

**Publication limitation:** `fx68k.sv` and `fx68kAlu.sv` in the frozen Macross II tree are **modified** relative to public sources. They have **not** been transferred or cleared merely by publishing these companion files. Do not replace frozen working HDL with pristine sources. See [project attribution](../../../../ATTRIBUTION.md) and [reuse report](../../../../CROSS_PROJECT_REUSE.md).

No copyrighted game ROM, firmware, artwork, or unreviewed modified HDL is present in this batch.
