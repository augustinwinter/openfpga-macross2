# Historical Pocket metadata snapshots — evidence archive

**Status:** historical, ROM-free metadata preservation; **not** a public Pocket release or proof of one canonical core version.

The same already-tested Macross II FPGA RBF SHA-256 can occur in more than one preserved installer with different `core.json`, metadata files or core folder names. CP48BH found multiple distinct configurations and stopped without copying or uploading anything. The CP48BH2 importer remedies this ambiguity **without guessing** which archive was the final beta.

Run the guarded local `tools/import-pocket-metadata.py` from the checked-out private repository, after pulling its latest `main`. It identifies each ZIP with a single `Cores/<name>/bitstream.rbf_r` whose SHA-256 is `93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87`, requires `Platforms/nmk16_m2.json` and the basic Pocket metadata, and stores **only** a small whitelist of UTF-8 JSON/text in `publication/pocket-metadata-snapshots/<content fingerprint>/`.

Each namespace retains the original `Cores/<name>/...` and `Platforms/nmk16_m2.json` relative paths so configurations remain distinguishable. The generated `manifests/POCKET-METADATA-SNAPSHOTS.json` lists actual archived versions, relative source archive paths and checksums, and every imported file's SHA-256 and Git blob SHA-1. Identical metadata sets from different ZIP archives share one snapshot and each source archive's hash is recorded.

**Excluded from Git:** the FPGA bitstream itself, game ROM/PROM dumps, artwork/banners/platform images, ZIP archives and physical SD-card contents. The bitstream is read only to qualify a metadata source. The original frozen Quartus/FPGA sources are never edited.

**Next release selection remains deliberate:** neither newest filename nor higher version determines what was physically tested. This archive does not automatically create `Cores/` at repository root, assign canonical release status or authorize public redistribution. Vendor-source licensing and GPL corresponding-source obligations still apply; see [RELEASE_READINESS.md](../../RELEASE_READINESS.md).
