#!/usr/bin/env python3
"""Import only ROM-free Pocket metadata from a preserved Macross II package.

No Quartus rebuild; no ROM, original artwork, timing PROM or RBF is staged.
A known-good bitstream must be present in the input archive (SHA check only).
Preserves metadata bytes and their actual core folder/version; does NOT assert
that a historical RC1 metadata set is the later 0.14.0-beta.1 version.
Only commits/pushes when GitHub stays private and the chosen archive is unique.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROJECT = Path.home() / "Documents/Codex/MacrossII-NMK165"
ARCHIVE_ROOT = PROJECT / "scratch/CP48-clean-macross2"
BITSTREAM_SHA = "93f7b62a8d8e8760fd7cdddaf334041b2646933b8539f9eebbda568bf12d1a87"
CORE_ALLOWED = {
    "AUTHORS.txt", "audio.json", "core.json", "data.json",
    "info.txt", "input.json", "interact.json", "variants.json", "video.json",
}
PLATFORM_ALLOWED = {"Platforms/nmk16_m2.json"}
MANIFEST_NAME = "manifests/POCKET-METADATA.json"
REPOSITORY = "augustinwinter/openfpga-macross2"


def run(*cmd: str) -> str:
    done = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(
            f"Command failed: {cmd[:3]}: " + done.stderr[-1500:]
        )
    return done.stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def recognize(path: Path):
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                return None
            rbf = [n for n in names if n.startswith("Cores/")
                   and n.endswith("/bitstream.rbf_r") and n.count("/") == 2]
            platform = [n for n in names if n == "Platforms/nmk16_m2.json"]
            if len(rbf) != 1 or len(platform) != 1:
                return None
            if sha256(archive.read(rbf[0])) != BITSTREAM_SHA:
                return None
            prefix = rbf[0].rsplit("/", 1)[0] + "/"
            allowed = {
                prefix + name for name in CORE_ALLOWED
            } | PLATFORM_ALLOWED
            if not (prefix + "core.json" in names
                    and prefix + "data.json" in names
                    and prefix + "variants.json" in names):
                return None
            metadata = {}
            for name in sorted(allowed.intersection(names)):
                if name.startswith("Cores/") and not name.startswith(prefix):
                    continue
                data = archive.read(name)
                if len(data) > 128 * 1024 or b"\0" in data:
                    raise RuntimeError(f"Unexpected binary/large metadata: {name}")
                data.decode("utf-8")
                if name.endswith(".json"):
                    json.loads(data)
                metadata[name] = data
            core = json.loads(metadata[prefix + "core.json"])
            version = core.get("version", "")
            if not isinstance(version, str):
                version = str(version)
            return {"archive": path, "files": metadata,
                    "folder": prefix, "version": version,
                    "archive_sha256": sha256(path.read_bytes())}
    except (OSError, zipfile.BadZipFile, KeyError, ValueError):
        return None


def main():
    if not ARCHIVE_ROOT.is_dir():
        raise RuntimeError(f"Protected historic package folder missing: {ARCHIVE_ROOT}")
    if run("git", "rev-parse", "--show-toplevel") != str(REPO):
        raise RuntimeError("Run inside a fresh Macross II private repository clone")
    if run("git", "branch", "--show-current") != "main":
        raise RuntimeError("Unexpected branch; main required")
    if run("git", "status", "--porcelain"):
        raise RuntimeError("Repository has uncommitted changes; stop")
    origin = run("git", "remote", "get-url", "origin")
    if not (origin.endswith("github.com/" + REPOSITORY + ".git")
            or origin.endswith("github.com:" + REPOSITORY + ".git")):
        raise RuntimeError("Unexpected GitHub origin")
    state = json.loads(run("gh", "api", "repos/" + REPOSITORY))
    if not state.get("private") or not state.get("permissions", {}).get("push"):
        raise RuntimeError("Private repository with push permission required")
    local = run("git", "rev-parse", "HEAD")
    remote = run("git", "ls-remote", "origin", "refs/heads/main").split()[0]
    if local != remote:
        raise RuntimeError("Repository behind/ahead of GitHub; pull first")

    candidates = []
    for archive in sorted(ARCHIVE_ROOT.rglob("*.zip")):
        if archive.is_symlink() or archive.stat().st_size > 80 * 1024 * 1024:
            continue
        item = recognize(archive)
        if item:
            candidates.append(item)
    if not candidates:
        raise RuntimeError(
            "No archived Pocket package with verified trusted RBF and metadata"
            " under CP48-clean-macross2. No files uploaded."
        )

    # Prefer explicitly versioned beta metadata; otherwise accept one RC1 set,
    # never claim metadata version that the archive itself does not contain.
    beta = [c for c in candidates if c["version"] == "0.14.0-beta.1"]
    selection = beta if beta else candidates
    distinct = {
        tuple((p, sha256(data)) for p, data in sorted(x["files"].items()))
        for x in selection
    }
    if len(distinct) != 1:
        raise RuntimeError(
            "Several distinct eligible metadata sets; no automatic selection."
            " Inspect the historical archives, do not overwrite a trusted set."
        )
    chosen = selection[0]
    files = chosen["files"]
    if Path(REPO / MANIFEST_NAME).exists():
        raise RuntimeError("Pocket metadata manifest already exists; no overwrite")

    print("=== VERIFIED ROM-FREE METADATA IMPORT ===")
    print("SOURCE ARCHIVE:", chosen["archive"])
    print("METADATA VERSION (AS-IS):", chosen["version"] or "(unlabeled)")
    print("ORIGINAL CORE FOLDER:", chosen["folder"])
    print("VALIDATED FROZEN RBF SHA256:", BITSTREAM_SHA)
    print("METADATA FILES:", len(files))
    for name in files:
        target = REPO / name
        if target.exists() or target.is_symlink():
            raise RuntimeError(f"Existing target, will not overwrite: {name}")
    manifest = {
        "checkpoint": "CP48BH",
        "source_archive_sha256": chosen["archive_sha256"],
        "core_folder_from_archive": chosen["folder"],
        "metadata_version_from_archive": chosen["version"],
        "verified_rbf_sha256_not_uploaded": BITSTREAM_SHA,
        "files": [
            {"path": name, "size": len(data), "sha256": sha256(data)}
            for name, data in sorted(files.items())
        ],
        "not_uploaded": [
            "bitstream.rbf_r", "game ROMs", "game PROMs",
            "Platforms/_images", "copyrighted game artwork"
        ],
        "release_qualification": "None: metadata import only, not release clearance",
    }
    # From here onward only write into the fresh clone. No protected source edits.
    for name, data in files.items():
        target = REPO / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if sha256(target.read_bytes()) != sha256(data):
            raise RuntimeError(f"Copy verification failed: {name}")
    output = REPO / MANIFEST_NAME
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    allowed = list(files) + [MANIFEST_NAME]
    run("git", "add", "--", *allowed)
    staged = set(run("git", "diff", "--cached", "--name-only").splitlines())
    if staged != set(allowed):
        raise RuntimeError(f"Unexpected staged changes: {sorted(staged)}")
    for name, data in files.items():
        in_git = subprocess.run(
            ["git", "-C", str(REPO), "show", ":" + name],
            check=True, capture_output=True,
        ).stdout
        if in_git != data:
            raise RuntimeError(f"Staged content changed: {name}")
    run("git", "-c", "core.whitespace=-blank-at-eol",
        "diff", "--cached", "--check")
    state = json.loads(run("gh", "api", "repos/" + REPOSITORY))
    if not state.get("private"):
        raise RuntimeError("Repository visibility changed; no upload")
    if run("git", "ls-remote", "origin", "refs/heads/main").split()[0] != local:
        raise RuntimeError("GitHub head changed; no push")

    run("git", "commit", "-m",
        "Publish ROM-free preserved Pocket metadata and exact source checksums")
    commit = run("git", "rev-parse", "HEAD")
    run("git", "push", "origin", "HEAD:main")
    published = run("git", "ls-remote", "origin", "refs/heads/main").split()[0]
    if published != commit:
        raise RuntimeError("GitHub ref did not match completed push")
    print("=== POCKET METADATA IMPORT PASS ===")
    print("REMOTE COMMIT:", published)
    print("GAME ROM/ART/BITSTREAM FILES COMMITTED: 0")
    print("ORIGINAL SOURCE AND POCKET SD: UNCHANGED")
    print("REPOSITORY: PRIVATE; NO GITHUB RELEASE CREATED")
    print("This is NOT a rebuilt/tested binary or license/public release approval.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP:", exc, file=sys.stderr)
        sys.exit(1)
