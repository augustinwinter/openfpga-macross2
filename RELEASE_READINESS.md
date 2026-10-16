# Macross II — publication completion and release gates

**2026-10-16 status:** The *private repository staging and source inventory* are complete to the extent proven and permitted. Full **public source-and-binary publication is NOT complete**, and no new public release has been created. This document identifies the explicit external rights and asset dependencies, rather than presenting a private repository as a public release.

## Completed without further FPGA rebuilding

- Existing Macross II Pocket beta `0.14.0-beta.1` was physically tested before publication work; freeze and preserve its bitstream SHA-256 `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87`. Do not recompile or substitute newly built FPGA binaries.
- CP48BG **PASS** on the owner's private hydrated Mac checkout: exactly 77 active HDL, 4 Quartus QIPs, QSF SDC and pinout Tcl, 2 FX68K CPU microcode files and 9 local external-source SHA validations. The two absent QIP auxiliary `MISC_FILE` entries were not needed in the recorded successful Quartus compile.
- The private GitHub repository tracks **69 active HDL source files**, all recorded by exact Git blob SHA in `manifests/ACTIVE-HDL-77.json`. Eight APF/Intel source files remain excluded from Git; the locally modified APF bridge and seven unchanged upstream files are byte-authenticated locally via `tools/hydrate-pocket-vendor.py`.
- The immutable public-origin source pins, GPL/JT/FX68K notices, original T80 VHDL lineage, four QIPs, relevant build scripts, source provenance and ROM-assembly instructions are included. `tools/verify-publication.py` checks the published manifest and guards against accidentally tracked game/binary assets.
- The owner **explicitly skipped a fresh Quartus rebuild**. Therefore independent clean-checkout bitstream equality, CDC/timing signoff and fresh hardware testing are unclaimed. There is no requirement to repeat those tests just to finish documentation.

## Pocket metadata without new FPGA compilation

The repository contains [`tools/import-pocket-metadata.py`](tools/import-pocket-metadata.py). **CP48BH initially stopped safely** because multiple historical Pocket ZIPs associated with the **exact existing tested FPGA bitstream SHA-256** `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87` had **different metadata configurations**. No metadata was committed by the failed importer.

The revised **CP48BH2** importer preserves **every distinct eligible ROM-free configuration** in its own deterministic content-hash namespace under `publication/pocket-metadata-snapshots/<fingerprint>/`. Its manifest `manifests/POCKET-METADATA-SNAPSHOTS.json` records each archived version and core folder **exactly as found**, all source ZIP hashes and file hashes. The exact existing RBF is **read only to validate** the origin of the metadata; **it is not uploaded**, and no game ROMs, PROMs, artwork, or original installer ZIPs are imported. Duplicates collapse by metadata-content SHA, not by arbitrary filename/date or version ordering.

**These are historical snapshots, not selectable/certified Pocket release packages.** If RC1 and beta JSON files differ, both are preserved and neither is automatically designated the definitive publicly tested beta. [`tools/verify-publication.py`](tools/verify-publication.py) validates all snapshots after publication. The revised importer is prepared in GitHub but its CP48BH2 run on the owner's Mac is **not yet recorded**. No Quartus rebuild or hardware retest is required.
## External blockers before public publication

1. **Analogue APF source rights.** Four active APF-origin files (one locally modified command bridge) and the externally hosted exact Pocket pinout need a documented, permissible public-source delivery model. The original EULA includes both developer-application distribution language and APF software restrictions. Obtain official clarification before uploading the modified APF framework code or asserting public corresponding-source completeness.
2. **Intel/Altera generated-IP redistribution.** Four active vendor-generated Verilog files have separate Intel/Altera notices and tool agreements. Record whether redistributing these exact generated sources with their headers is allowed, or use a rights-cleared generation/hydration recipe whose result matches the frozen input.
3. **Original code licensing and GPL compliance.** Establish rights and chosen terms for the project-specific contributions; preserve all applicable third-party notices and comply with GPL corresponding-source obligations before distributing the compiled beta publicly.
4. **ROM-free Pocket release assets.** A public beta must contain only the frozen tested RBF and the corresponding rights-cleared `Cores/` JSON/text plus `Platforms/nmk16_m2.json`. Users supply `macross2.rom` and `macross2_vprom.bin` independently. Original banner/title art and `Platforms/_images/nmk16_m2.bin` must be excluded or replaced with demonstrably rights-cleared art. The currently preserved test installer is not certified ROM-free.

## Actions explicitly out of scope

- No fresh Quartus build; no new FPGA timing/CDC qualification; no hardware retest.
- No upload of ROM, PROM, game-art or vendor-origin source on assumptions; no automatic switch from private to public.
- No fabricated missing `.cmp`/`.ppf` auxiliary files; no replacement of modified Macross II RTL with pristine upstream code.

## Completion condition

Record the vendor/source permissions and author licensing decision, then assemble an exact **ROM-free** distribution using the already-tested bitstream (do not rebuild), with attribution, licenses, installation notes, and verified ZIP contents. Publish/tag only when all externally owned components and binary corresponding-source obligations are satisfied. Otherwise retain the fully documented private source staging and mark public release **blocked**, not falsely complete.

