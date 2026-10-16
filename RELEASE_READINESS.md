# Macross II — publication completion and release gates

**2026-10-16 status:** The *private repository staging and source inventory* are complete to the extent proven and permitted. Full **public source-and-binary publication is NOT complete**, and no new public release has been created. This document identifies the explicit external rights and asset dependencies, rather than presenting a private repository as a public release.

## Completed without further FPGA rebuilding

- Existing Macross II Pocket beta `0.14.0-beta.1` was physically tested before publication work; freeze and preserve its bitstream SHA-256 `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87`. Do not recompile or substitute newly built FPGA binaries.
- CP48BG **PASS** on the owner's private hydrated Mac checkout: exactly 77 active HDL, 4 Quartus QIPs, QSF SDC and pinout Tcl, 2 FX68K CPU microcode files and 9 local external-source SHA validations. The two absent QIP auxiliary `MISC_FILE` entries were not needed in the recorded successful Quartus compile.
- The private GitHub repository tracks **69 active HDL source files**, all recorded by exact Git blob SHA in `manifests/ACTIVE-HDL-77.json`. Eight APF/Intel source files remain excluded from Git; the locally modified APF bridge and seven unchanged upstream files are byte-authenticated locally via `tools/hydrate-pocket-vendor.py`.
- The immutable public-origin source pins, GPL/JT/FX68K notices, original T80 VHDL lineage, four QIPs, relevant build scripts, source provenance and ROM-assembly instructions are included. `tools/verify-publication.py` checks the published manifest and guards against accidentally tracked game/binary assets.
- The owner **explicitly skipped a fresh Quartus rebuild**. Therefore independent clean-checkout bitstream equality, CDC/timing signoff and fresh hardware testing are unclaimed. There is no requirement to repeat those tests just to finish documentation.

## Pocket metadata without new FPGA compilation

The repository also contains [`tools/import-pocket-metadata.py`](tools/import-pocket-metadata.py). It finds a preserved **historical** Pocket ZIP in the owner's protected `scratch/CP48-clean-macross2/` folder, accepts only one well-defined metadata set with the **verified existing FPGA bitstream SHA-256** `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87` present in the archive, and transfers **only** a small allowlist of core JSON/text and `Platforms/nmk16_m2.json` to the private GitHub repository. It records the actual historical metadata version and folder without silently upgrading RC1 to beta. It **does not upload the RBF**, arcade game ROMs, PROMs, artwork or the original package. No Quartus rebuild or hardware retest is performed.

The importer is staged in GitHub but **has not been run** on the owner's Mac. If an older RC1 metadata archive is the only verified match, it will be recorded accurately as RC1 material rather than misrepresented as the newer beta's metadata. This is not a public release authorization.
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

