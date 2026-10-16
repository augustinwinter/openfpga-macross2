#!/usr/bin/env python3
"""Archive ALL distinct verified Pocket metadata snapshots, without guessing a winner.

ROM-free metadata only. An authentic, previously tested bitstream is read for
SHA-256 verification but is NOT imported, rebuilt, pushed, or redistributed.
Multiple historically different JSON/text configurations are preserved under
distinct content-derived folders. No variant is labelled the definitive beta.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parent.parent
ROOT = (
    Path.home() / "Documents/Codex/MacrossII-NMK165"
    / "scratch/CP48-clean-macross2"
)
PRIVATE_REPO = "augustinwinter/openfpga-macross2"
RBF_SHA256 = "93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87"
CORE_ALLOWED = {
    "AUTHORS.txt", "audio.json", "core.json", "data.json", "info.txt",
    "input.json", "interact.json", "variants.json", "video.json"
}
PLATFORM = "Platforms/nmk16_m2.json"
SNAPSHOT_ROOT = "publication/pocket-metadata-snapshots"
MANIFEST = "manifests/POCKET-METADATA-SNAPSHOTS.json"
MAX_ARCHIVES = 64


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(*args: str) -> str:
    proc = subprocess.run(
        args, cwd=REPO, text=True, capture_output=True, check=False
    )
    if proc.returncode:
        raise RuntimeError(
            f"STOP: command {args[0]} failed: " + proc.stderr[-1600:]
        )
    return proc.stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def private_push_check() -> None:
    state = json.loads(run("gh", "api", "repos/" + PRIVATE_REPO))
    if state.get("private") is not True:
        raise RuntimeError("STOP: repository is not private")
    if not state.get("permissions", {}).get("push"):
        raise RuntimeError("STOP: no permission to push private repository")


def recognize(path: Path):
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)) or len(names) > 2000:
                return None
            rbf = []
            for name in names:
                bits = PurePosixPath(name).parts
                if (
                    len(bits) == 3 and bits[0] == "Cores"
                    and bits[2] == "bitstream.rbf_r"
                    and re.fullmatch(r"[A-Za-z0-9_. -]+", bits[1])
                    and ".." not in bits[1]
                ):
                    rbf.append(name)
            if len(rbf) != 1 or PLATFORM not in names:
                return None
            raw = archive.getinfo(rbf[0])
            if raw.file_size != 1949788:
                return None
            if sha256(archive.read(rbf[0])) != RBF_SHA256:
                return None
            prefix = rbf[0].rsplit("/", 1)[0] + "/"
            if any(prefix + part not in names for part in (
                "core.json", "data.json", "variants.json"
            )):
                return None
            metadata = {}
            permitted = {prefix + n for n in CORE_ALLOWED} | {PLATFORM}
            for name in sorted(permitted.intersection(names)):
                member = archive.getinfo(name)
                if member.file_size > 128 * 1024:
                    raise RuntimeError(f"STOP: excessive metadata size in {path.name}")
                data = archive.read(name)
                if b"\0" in data:
                    raise RuntimeError(f"STOP: binary metadata in {path.name}")
                data.decode("utf-8")
                if name.endswith(".json"):
                    json.loads(data)
                metadata[name] = data
            if len(metadata) < 4:
                return None
            core = json.loads(metadata[prefix + "core.json"])
            if not isinstance(core, dict):
                return None
            version = str(core.get("version", ""))
            fingerprint = sha256(
                json.dumps(
                    {n: sha256(data) for n, data in sorted(metadata.items())},
                    sort_keys=True, separators=(",", ":")
                ).encode("utf-8")
            )
            return {
                "fingerprint": fingerprint, "files": metadata,
                "version": version, "core_folder": prefix,
                "archive": str(path.relative_to(ROOT)),
                "archive_sha256": sha256(path.read_bytes())
            }
    except (OSError, zipfile.BadZipFile, KeyError, ValueError, UnicodeError):
        return None


def main() -> None:
    if not ROOT.is_dir():
        raise RuntimeError(f"STOP: preserved CP48 source directory not found: {ROOT}")
    if run("git", "rev-parse", "--show-toplevel") != str(REPO):
        raise RuntimeError("STOP: not in a GitHub clone of Macross II")
    if run("git", "branch", "--show-current") != "main":
        raise RuntimeError("STOP: not on main")
    if run("git", "status", "--porcelain"):
        raise RuntimeError("STOP: existing changes; preserve and review")
    url = run("git", "remote", "get-url", "origin")
    if not (url.endswith("github.com/" + PRIVATE_REPO + ".git") or
            url.endswith("github.com:" + PRIVATE_REPO + ".git")):
        raise RuntimeError(f"STOP: unexpected remote: {url}")
    private_push_check()
    head = run("git", "rev-parse", "HEAD")
    if run("git", "ls-remote", "origin", "refs/heads/main").split()[0] != head:
        raise RuntimeError("STOP: remote advanced; pull first")

    archives = sorted(ROOT.rglob("*.zip"))
    if len(archives) > MAX_ARCHIVES:
        raise RuntimeError("STOP: too many ZIP archives for automatic preservation")
    snapshots = {}
    for archive in archives:
        if archive.is_symlink() or archive.stat().st_size > 80 * 1024 * 1024:
            continue
        item = recognize(archive)
        if not item:
            continue
        key = item["fingerprint"]
        if key not in snapshots:
            snapshots[key] = item
            item["archives"] = []
        elif snapshots[key]["files"] != item["files"]:
            raise RuntimeError("STOP: snapshot fingerprint collision")
        snapshots[key]["archives"].append({
            "path_relative_to_preserved_folder": item["archive"],
            "sha256": item["archive_sha256"]
        })
    if not snapshots:
        raise RuntimeError("STOP: no verified Pocket archives found")
    if (REPO / MANIFEST).exists():
        raise RuntimeError("STOP: manifest already exists; no overwrite")

    # Store each distinct candidate separately; never select RC1 vs beta by guess.
    output_files = {}
    records = []
    for ident, entry in sorted(snapshots.items()):
        files = []
        for original, data in sorted(entry["files"].items()):
            dest = f"{SNAPSHOT_ROOT}/{ident}/{original}"
            output_files[dest] = data
            files.append({
                "original_zip_path": original,
                "repository_path": dest,
                "bytes": len(data),
                "sha256": sha256(data),
                "git_blob_sha1": git_blob(data)
            })
        records.append({
            "content_fingerprint": ident,
            "core_folder_as_archived": entry["core_folder"],
            "core_version_as_archived": entry["version"],
            "archives_with_identical_metadata": sorted(
                entry["archives"], key=lambda x: x["path_relative_to_preserved_folder"]
            ),
            "metadata_files": files
        })
    manifest = {
        "checkpoint": "CP48BH2",
        "status": "Historical metadata candidates only; NO canonical release selection",
        "validated_tested_rbf_sha256_not_uploaded": RBF_SHA256,
        "number_of_distinct_metadata_sets": len(records),
        "snapshots": records,
        "strict_exclusions": [
            "bitstream.rbf_r", "arcade ROM", "PROM dumps", "original game artwork",
            "complete package ZIP", "SD-card contents", "FPGA compilation outputs"
        ],
        "not_asserted": [
            "which historical metadata snapshot was physically tested",
            "public distribution rights", "new FPGA build", "new hardware test"
        ]
    }
    output_files[MANIFEST] = (
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    for dest in output_files:
        full = REPO / dest
        if full.exists() or full.is_symlink():
            raise RuntimeError(f"STOP: refusing to overwrite: {dest}")

    print("=== CP48BH2 VERIFIED ROM-FREE SNAPSHOT PRESERVATION ===")
    print("QUALIFYING HISTORICAL ZIP ARCHIVES:",
          sum(len(s["archives"]) for s in snapshots.values()))
    print("DISTINCT METADATA CONFIGURATIONS:", len(snapshots))
    for record in records:
        print("  SNAPSHOT:", record["content_fingerprint"])
        print("    VERSION:", record["core_version_as_archived"])
        print("    FOLDER:", record["core_folder_as_archived"])
        print("    ARCHIVES:", len(record["archives_with_identical_metadata"]))
    print("STAGED BITSTREAMS, GAME ROMS, ARTWORK OR ZIP FILES: 0")
    for dest, payload in output_files.items():
        target = REPO / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        if sha256(target.read_bytes()) != sha256(payload):
            raise RuntimeError(f"STOP: copy checksum mismatch: {dest}")
    run("git", "add", "--", *sorted(output_files))
    staged = set(run("git", "diff", "--cached", "--name-only").splitlines())
    if staged != set(output_files):
        raise RuntimeError(f"STOP: unexpected staged paths: {sorted(staged)}")
    for dest, payload in output_files.items():
        staged_bytes = subprocess.run(
            ["git", "-C", str(REPO), "show", ":" + dest],
            check=True, capture_output=True
        ).stdout
        if staged_bytes != payload:
            raise RuntimeError(f"STOP: Git staging differs: {dest}")
    run("git", "-c", "core.whitespace=-blank-at-eol",
        "diff", "--cached", "--check")
    private_push_check()
    if run("git", "ls-remote", "origin", "refs/heads/main").split()[0] != head:
        raise RuntimeError("STOP: GitHub main advanced; no commit")
    run("git", "commit", "-m",
        "Preserve all verified historical ROM-free Pocket metadata snapshots")
    commit = run("git", "rev-parse", "HEAD")
    run("git", "push", "origin", "HEAD:main")
    if run("git", "ls-remote", "origin", "refs/heads/main").split()[0] != commit:
        raise RuntimeError("STOP: published commit does not match")
    print("=== CP48BH2 COMPLETE ===")
    print("GITHUB PUSH VERIFIED:", commit)
    print("DISTINCT METADATA SETS:", len(records))
    print("ORIGINAL SOURCE, SD CARD, FPGA BITSTREAMS: UNCHANGED")
    print("NO PUBLIC RELEASE, FPGA REBUILD, OR WINNER SELECTED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP:", exc, file=sys.stderr)
        sys.exit(1)
