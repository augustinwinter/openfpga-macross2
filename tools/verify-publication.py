#!/usr/bin/env python3
"""Read-only audit of the PRIVATE GitHub publication's exact active HDL inventory.

This is a *source-manifest* check, not a Quartus rebuild, FPGA test, licensing
clearance, release approval, or a promise of bitstream reproducibility.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "manifests/ACTIVE-HDL-77.json"
FORBIDDEN_EXT = (".rom", ".zip", ".chd", ".rbf", ".rbf_r", ".sof", ".jic", ".pof")
SUPPORT_FILES = (
    "projects/m2_pocket.qpf",
    "projects/m2_pocket.qsf",
    "projects/m2_pocket.sdc",
    "reference/rtl/third_party/fx68k/microrom.mem",
    "reference/rtl/third_party/fx68k/nanorom.mem",
    "tools/hydrate-pocket-vendor.py",
    "tools/audit-quartus-closure.py",
    "VENDOR_SOURCE.md",
    "BUILDING.md",
)
PINOUT = "platform/pocket/bsp/pocket/pinouts/system.tcl"


def git(*args: str, okay=(0,)) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True, check=False,
    )
    if result.returncode not in okay:
        raise RuntimeError(
            f"Git check failed: {' '.join(args)}: "
            + result.stderr.decode(errors="replace")[-900:]
        )
    return result


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()


def main() -> None:
    if not MANIFEST.is_file():
        raise RuntimeError("Missing ACTIVE-HDL-77.json manifest")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = data["files"]
    if len(entries) != 77 or len({x["path"] for x in entries}) != 77:
        raise RuntimeError("Manifest is not a unique 77-file active source set")

    tracked = set(
        git("ls-files", "-z").stdout.decode("utf-8").strip("\0").split("\0")
    )
    for name in SUPPORT_FILES:
        if name not in tracked:
            raise RuntimeError(f"Required source/support item missing: {name}")

    exact, external = 0, 0
    for item in entries:
        path = item["path"]
        target = ROOT / path
        if item["status"] == "tracked_verified":
            if path not in tracked or not target.is_file():
                raise RuntimeError(f"Manifest-tracked source is missing: {path}")
            observed = blob_sha(target.read_bytes())
            if observed != item["git_blob_sha1"]:
                raise RuntimeError(f"Blob SHA mismatch: {path}")
            exact += 1
        elif item["status"] == "external_local_only":
            if path in tracked:
                raise RuntimeError(f"Vendor-held item is tracked in Git: {path}")
            git("check-ignore", "-q", path)
            if target.exists():
                if not target.is_file() or target.is_symlink():
                    raise RuntimeError(f"Invalid local vendor source: {path}")
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
                if actual != item["local_sha256"]:
                    raise RuntimeError(f"Local vendor SHA-256 mismatch: {path}")
            external += 1
        else:
            raise RuntimeError(f"Unexpected source manifest status: {path}")

    if (exact, external) != (69, 8):
        raise RuntimeError(f"Unexpected source closure: {exact} tracked/{external} held")
    if len(data["qips"]) != 4 or any(x not in tracked for x in data["qips"]):
        raise RuntimeError("Four Quartus QIPs are not tracked")

    if PINOUT in tracked:
        raise RuntimeError("Vendor Pocket pinout unexpectedly committed")
    git("check-ignore", "-q", PINOUT)
    pin = ROOT / PINOUT
    if pin.is_file() and hashlib.sha256(pin.read_bytes()).hexdigest() != (
        "e30e3c804a31aa38f9de8bb6c184f8dea0868b86c03eda4131f5d00ef0034a95"
    ):
        raise RuntimeError("CP48BF pinout hash mismatch")

    forbidden = [
        path for path in tracked
        if path.lower().endswith(FORBIDDEN_EXT)
        or path.startswith(("Assets/", "Platforms/_images/", "private/"))
    ]
    if forbidden:
        raise RuntimeError(f"Unexpected binaries/game assets in Git: {forbidden}")

    history_name = "manifests/POCKET-METADATA-SNAPSHOTS.json"
    history_files = set()
    snapshot_count = 0
    if history_name in tracked:
        history = json.loads((ROOT / history_name).read_text(encoding="utf-8"))
        snapshots = history.get("snapshots", [])
        if (
            history.get("number_of_distinct_metadata_sets") != len(snapshots)
            or not snapshots
        ):
            raise RuntimeError("Pocket metadata snapshot manifest is inconsistent")
        for snap in snapshots:
            fingerprint = snap["content_fingerprint"]
            if len(fingerprint) != 64 or any(
                char not in "0123456789abcdef" for char in fingerprint
            ):
                raise RuntimeError("Invalid Pocket snapshot identifier")
            for item in snap["metadata_files"]:
                p = item["repository_path"]
                prefix = f"publication/pocket-metadata-snapshots/{fingerprint}/"
                if (
                    not p.startswith(prefix)
                    or ".." in Path(p).parts
                    or p in history_files
                    or p not in tracked
                ):
                    raise RuntimeError(f"Unexpected Pocket metadata path: {p}")
                content = (ROOT / p).read_bytes()
                if (
                    len(content) != item["bytes"]
                    or hashlib.sha256(content).hexdigest() != item["sha256"]
                    or blob_sha(content) != item["git_blob_sha1"]
                    or not p.lower().endswith((".json", ".txt"))
                ):
                    raise RuntimeError(f"Pocket metadata hash/type mismatch: {p}")
                history_files.add(p)
        unexpected = {
            p for p in tracked
            if p.startswith("publication/pocket-metadata-snapshots/")
        } - history_files
        if unexpected:
            raise RuntimeError(f"Unmanifested Pocket metadata: {sorted(unexpected)}")
        snapshot_count = len(snapshots)

    print("=== VERIFIED SOURCE PUBLICATION INVENTORY ===")
    print("Active Quartus HDL: 77")
    print("Git-tracked HDL matching source manifest: 69 PASS")
    print("Vendor-origin HDL withheld from Git: 8 PASS")
    print("Quartus QIP files: 4 PASS")
    print("Pocket pinout: local-only, hash-checked when present")
    print("Git-tracked ROM/FPGA outputs: 0 PASS")
    print("ROM-free Pocket metadata snapshots hash-verified:", snapshot_count)
    print("No FPGA build, vendor redistribution, or Pocket test performed.")
    print("SOURCE-MANIFEST AUDIT: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP:", exc, file=sys.stderr)
        sys.exit(1)
