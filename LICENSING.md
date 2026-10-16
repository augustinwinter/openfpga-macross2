# Third-party licenses and project publication terms

**This is a mixed-license engineering source tree, not a blanket MIT/GPL grant.** File-level copyrights and licenses remain authoritative. No global license is asserted for files or contributions whose rights are not established. This note is an inventory, not legal advice.

## Included and preserved materials

- **FX68K:** Jorge Cwik, GPLv3 per `reference/rtl/third_party/fx68k/LICENSE` and its `fx68k.txt` copyright/licensing grant; the two CPU-internal microcode `.mem` files are source dependencies, not game ROMs.
- **JT03/JT12, JT49, JT6295:** José Tejada and contributors; original GPL notices and component license files are kept in `reference/rtl/third_party/jt12/` and `reference/rtl/third_party/jt6295/`. Three locally modified JT lookup files add only a Quartus RAM synthesis attribute, retained without stripping original notices.
- **NMK16 MiSTer and derivations:** kuzearcade and relevant upstream contributors; original GNU GPLv3 terms are reproduced in `reference/rtl/NMK16-UPSTREAM-LICENSE`, with exact commit pins in `CROSS_PROJECT_REUSE.md`. SDRAM, NMK CPU and video descendants have modified local versions with inherited obligations; exact inclusion does not erase upstream copyright.
- **T80:** Daniel Wallner, MikeJ, Sorgelig and other credited authors; preserve the upstream T80 `README` conditions and the 13 original VHDL sources, corresponding generated `T80s.v`, patch and generation documentation. The generated netlist is not public-domain simply because a tool produced it.
- **Pocket platform utilities:** mixed MIT/CC0/GPL or other per-file grants from the Pocket template and contributors. See the individual SPDX/copyright notices and `platform/pocket/UPSTREAM-REVIEWED.md`. A general license label for the entire `platform/pocket` folder would be inaccurate.
- **MAME reference material:** hardware behavior was compared with `mamedev/mame`; if expression from particular BSD-3-Clause C++ files was adapted, corresponding named authors and BSD-3-Clause notices must be preserved. Behavioral equivalence alone does not confer or require a license.

## External-only, not Git-distributed

Four Analogue APF-origin HDL files and four Intel/Altera-generated FPGA megafunction files remain deliberately **not tracked in GitHub** while their original source redistribution rights are reviewed. The verified Analogue pinout Tcl is also external-only. Exact hashes and local retrieval are documented in `VENDOR_SOURCE.md`. The locally modified APF command bridge is **not reproducible from the unmodified public template alone** and is imported only from the owner's verified source tree. Private local hydration is not public source delivery.

## Still requiring explicit decisions or permission

1. Obtain authoritative confirmation of distribution rights and required notices/combined terms for the **modified Analogue APF command bridge**, and for the unchanged APF files and generated Intel/Altera sources. Analogue's developer-application distribution allowance is not an unrestricted source redistribution license.
2. Record an intentional license grant for newly authored Macross II-only RTL, scripts, and other contributions, respecting any copyleft inheritance; do **not** guess the author's choice or automatically license vendor-owned material.
3. For any release of GPL-covered FPGA compiled works, meet applicable complete-corresponding-source and license/notice obligations. A Github tree missing eight HDL source inputs is **not** declared a complete corresponding-source distribution.
4. Keep original game ROM/PROM dumps, copyrighted game artwork, private ROM-containing test ZIPs and SD-card contents out of GitHub and public release bundles without separate rights.

**Public release is held** pending the above. The owner elected not to conduct a new FPGA build, so no independent rebuild certification will be claimed. See `RELEASE_READINESS.md` for precise exit criteria.

