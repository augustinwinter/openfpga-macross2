#!/usr/bin/env python3
"""CP48BB: safely import exact local Macross II RTL and project constraints.

Run only from a FRESH clone of augustinwinter/openfpga-macross2.
Reads, never changes, the verified source at scratch/CP48-clean-macross2/source.
Copies only whitelisted ROM-free files into this PRIVATE repository and pushes
the commit after local byte/hash and remote-visibility checks.
Requires git and authenticated GitHub CLI (gh).
Does NOT import proprietary Analogue APF or Intel/Altera generated IP.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPOSITORY = "augustinwinter/openfpga-macross2"
ROOT = (
    Path.home()
    / "Documents/Codex/MacrossII-NMK165"
    / "scratch/CP48-clean-macross2/source"
)
REPO = Path(__file__).resolve().parent.parent
PROVEN = {
    "derived/sdram.sv": "608c0a97e199a96dda122f0aa081e7262e1aeaff",
    "derived/sdram_arb.sv": "82e98256a82dda476be6070df9296a40bb748431",
    "derived/sdram_req.sv": "44c4c577dd6842b7c19d1b2b104eda97bafae753",
    "derived/tdragon2_core.sv": "fcfbeae8c2ddf157a8b500faa22ff54e3afdcb3c",
    "derived/video_macross2.sv": "c344f1e68639c40a40754c046821d1b19914552c",
    "reference/rtl/third_party/fx68k/fx68k.sv":
        "b326f23a9f8dd13d58e872ebf0db2c26d8914919",
    "platform/pocket/peripherals/core_bridge_cmd.sv":
        "89afdaaafb4fc406b8f226d593b9913e44395380",
    "target/pocket/core_top.sv": "e8fc88becb6a264518b4c948cb6af8eb0f39a488",
}
PROJECT = [
    "rtl/m2_apf_loader.sv",
    "rtl/m2_audio_cdc.sv",
    "rtl/m2_gameplay_video.sv",
    "rtl/m2_main_sdram.sv",
    "rtl/m2_memory.sv",
    "rtl/m2_pocket_machine.sv",
    "rtl/m2_prom_guard.sv",
    "rtl/pocket_pll.v",
]
PROJECT_CONFIG = [
    "projects/m2_pocket.qpf",
    "projects/m2_pocket.qsf",
    "projects/m2_pocket.sdc",
]
ALL = list(PROVEN) + PROJECT + PROJECT_CONFIG
MANIFEST = "manifests/CP48BB-local-source.json"


def run(*args: str) -> str:
    proc = subprocess.run(
        list(args), cwd=REPO, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(
            f"Command failed: {args[0]} {args[1] if len(args)>1 else ''}\n"
            + proc.stderr[-1400:]
        )
    return proc.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\\0" + data
    ).hexdigest()


def stop(message: str) -> None:
    raise RuntimeError("STOP: " + message)


def main() -> None:
    print("=== CP48BB: VERIFIED PRIVATE SOURCE IMPORT ===", flush=True)
    if not ROOT.is_dir():
        stop(f"Frozen source not found: {ROOT}")
    if not shutil.which("git") or not shutil.which("gh"):
        stop("Both git and authenticated GitHub CLI (gh) are required")
    if run("git", "rev-parse", "--show-toplevel") != str(REPO):
        stop("Run this script from the fresh private GitHub clone")
    if run("git", "branch", "--show-current") != "main":
        stop("Expected main branch")
    remote = run("git", "remote", "get-url", "origin")
    if not (
        remote.endswith("github.com/augustinwinter/openfpga-macross2.git")
        or remote.endswith("github.com:augustinwinter/openfpga-macross2.git")
    ):
        stop(f"Unexpected origin: {remote}")
    if run("git", "status", "--porcelain"):
        stop("Fresh checkout is not clean; preserve changes and investigate")
    state = json.loads(run("gh", "api", f"repos/{REPOSITORY}"))
    if state.get("private") is not True:
        stop("Repository is not private")
    if not state.get("permissions", {}).get("push"):
        stop("Authenticated account has no push permission")
    run("git", "fetch", "origin", "main")
    if run("git", "rev-parse", "HEAD") != run(
        "git", "rev-parse", "origin/main"
    ):
        stop("Remote branch advanced, update clone before importing")
    for prerequisite in (
        "reference/rtl/third_party/fx68k/LICENSE",
        "reference/rtl/NMK16-UPSTREAM-LICENSE",
        "SOURCE_PUBLISHING_STATUS.md",
    ):
        if not (REPO / prerequisite).is_file():
            stop(f"Missing expected published prerequisite: {prerequisite}")

    inventory = []
    # Validate ALL inputs and existing destinations before writing a byte.
    for relative in ALL:
        if relative.startswith("/") or ".." in Path(relative).parts:
            stop(f"Unsafe relative path: {relative}")
        source = ROOT / relative
        target = REPO / relative
        if not source.is_file() or source.is_symlink():
            stop(f"Missing / linked frozen source file: {relative}")
        payload = source.read_bytes()
        if not payload or b"\\0" in payload:
            stop(f"Missing or binary payload, not suitable for this batch: {relative}")
        try:
            payload.decode("utf-8")
        except UnicodeDecodeError:
            stop(f"Non-UTF-8 source file requires separate review: {relative}")
        actual = blob_sha(payload)
        required = PROVEN.get(relative)
        if required and actual != required:
            stop(
                f"Frozen modification hash changed: {relative}\n"
                f"expected {required}\nactual   {actual}"
            )
        if target.exists() and target.read_bytes() != payload:
            stop(f"Destination exists with different bytes: {relative}")
        inventory.append({
            "path": relative,
            "size": len(payload),
            "git_blob_sha1": actual,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "provenance": "CP48AY verified descendant"
                if relative in PROVEN else "Macross II local project/config source",
        })
    print("Verified", len(inventory), "ROM-free local source files.")
    print("Verified eight existing CP48AY modified-file hashes.")
    for entry in inventory:
        print("  ", entry["path"], entry["sha256"][:16])

    # Only modify the fresh clone, never the frozen source.
    for relative in ALL:
        source = ROOT / relative
        target = REPO / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(source, target)
        if blob_sha(target.read_bytes()) != blob_sha(source.read_bytes()):
            stop(f"Byte validation failed after copy: {relative}")

    manifest = REPO / MANIFEST
    if manifest.exists():
        stop(f"Manifest already exists: {MANIFEST}")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps({
            "checkpoint": "CP48BB",
            "private_repo": REPOSITORY,
            "source_root_relative": "scratch/CP48-clean-macross2/source",
            "description": "Exact private source import; no game assets or vendor IP",
            "files": inventory,
        }, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    run("git", "add", "--", *ALL, MANIFEST)
    staged = set(run("git", "diff", "--cached", "--name-only").splitlines())
    allowed = set(ALL) | {MANIFEST}
    if staged != allowed:
        stop(
            "Unexpected staged paths; DO NOT PUSH.\n"
            f"Actual: {sorted(staged)}\nExpected: {sorted(allowed)}"
        )
    run("git", "diff", "--cached", "--check")
    if not json.loads(run("gh", "api", f"repos/{REPOSITORY}")).get("private"):
        stop("Repository visibility changed before commit")
    run("git", "commit", "-m",
        "Import 16 exact local Macross II HDL files and ROM-free Quartus configs")
    sha = run("git", "rev-parse", "HEAD")
    run("git", "push", "origin", "HEAD:main")
    if run("git", "rev-parse", "HEAD") != run(
        "git", "rev-parse", "origin/main"
    ):
        stop("Push result requires investigation")
    print("PRIVATE GITHUB IMPORT VERIFIED:", sha)
    print("ACTIVE HDL TRANSFERRED: 16")
    print("PROJECT CONFIG FILES TRANSFERRED: 3")
    print("NO ORIGINAL SOURCE MODIFIED; NO ROMS/ARTWORK/SD/FPGA BINARIES TRANSFERRED")
    print("Vendor APF/Intel IP and remaining Quartus QIPs STILL REQUIRE REVIEW")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr, flush=True)
        sys.exit(1)
