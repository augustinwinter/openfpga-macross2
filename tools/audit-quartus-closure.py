#!/usr/bin/env python3
"""Read-only Quartus declared-source closure audit for the frozen CP48 build.

Run after local-only Pocket vendor hydration. Tests QSF/QIP/Tcl, 77 HDL files,
FX68K microcode, and all exact CP48AY/CP48BF vendor provenance checks.
This does not synthesize RTL, check transitive HDL includes or validate timing.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import runpy
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSF = ROOT / "projects/m2_pocket.qsf"
HDL_KINDS = {"SYSTEMVERILOG_FILE", "VERILOG_FILE", "VHDL_FILE", "AHDL_FILE"}
DIRECT_KINDS = HDL_KINDS | {"QIP_FILE", "SDC_FILE", "SOURCE_TCL_SCRIPT_FILE"}
QIP_KINDS = HDL_KINDS | {"QIP_FILE", "MISC_FILE"}
QIP_JOIN = re.compile(
    r'\[file\s+join\s+\$::quartus\(qip_path\)\s+"([^"]+)"\]'
)
CP48_MEM = {
    "reference/rtl/third_party/fx68k/microrom.mem":
        "9d13082be0cf4b04bff887e6da23de84f9f2ee4321f3a2576b4f9540615dece6",
    "reference/rtl/third_party/fx68k/nanorom.mem":
        "b3998009fb10605e8468cddf22fdd799a9792ba86f449de2e30615cfcefbeece",
}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()


def norm(path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise RuntimeError(f"Dependency escapes checkout: {path}")
    return resolved


def global_assignments(path: Path, qip=False):
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "-name" not in line or not line.lstrip().startswith("set_global_assignment"):
            continue
        if qip:
            m_kind = re.search(r"-name\s+([A-Z_]+)", line)
            m_name = QIP_JOIN.search(line)
            if m_kind and m_kind.group(1) in QIP_KINDS and m_name:
                yield number, m_kind.group(1), m_name.group(1)
        else:
            parts = shlex.split(line, comments=True)
            if "-name" in parts:
                idx = parts.index("-name")
                if len(parts) > idx + 2 and parts[idx + 1] in DIRECT_KINDS:
                    yield number, parts[idx + 1], parts[idx + 2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report-only", action="store_true",
        help="Print missing dependencies instead of stopping (not a PASS)",
    )
    args = parser.parse_args()
    if not QSF.is_file():
        raise RuntimeError(f"Missing Quartus project: {QSF}")

    hdl: set[Path] = set()
    qips: set[Path] = set()
    other: set[Path] = set()
    auxiliary: set[Path] = set()
    missing: set[Path] = set()

    pending: list[Path] = []
    for line, kind, name in global_assignments(QSF):
        path = norm(QSF.parent / name)
        if kind == "QIP_FILE":
            pending.append(path)
        elif kind in HDL_KINDS:
            hdl.add(path)
        else:
            other.add(path)

    while pending:
        qip = norm(pending.pop())
        if qip in qips:
            continue
        qips.add(qip)
        if not qip.is_file():
            missing.add(qip)
            continue
        for line, kind, name in global_assignments(qip, qip=True):
            path = norm(qip.parent / name)
            if kind == "QIP_FILE":
                pending.append(path)
            elif kind in HDL_KINDS:
                hdl.add(path)
            elif kind == "MISC_FILE":
                auxiliary.add(path)

    if len(hdl) != 77 or len(qips) != 4:
        raise RuntimeError(
            f"Quartus declaration count changed: {len(hdl)} HDL, {len(qips)} QIP; "
            "expected 77 and 4"
        )

    for path in hdl | other | qips:
        if not path.is_file() or path.is_symlink():
            missing.add(path)

    for rel, expected in CP48_MEM.items():
        path = ROOT / rel
        if not path.is_file() or path.is_symlink():
            missing.add(path)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"FX68K memory checksum mismatch: {rel}")

    cfg = runpy.run_path(str(ROOT / "tools/hydrate-pocket-vendor.py"))
    vendors = dict(cfg["EXPECTED"])
    vendors[cfg["BRIDGE"]] = cfg["BRIDGE_BLOB"]
    for rel, sha in vendors.items():
        path = ROOT / rel
        if not path.is_file():
            missing.add(path)
        elif path.is_symlink() or git_blob(path.read_bytes()) != sha:
            raise RuntimeError(f"Vendor original/modified blob mismatch: {rel}")

    for rel in vendors:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", "--", rel],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            raise RuntimeError(f"Vendor file unexpectedly tracked in Git: {rel}")

    pinout = ROOT / "platform/pocket/bsp/pocket/pinouts/system.tcl"
    if pinout.is_file():
        digest = hashlib.sha256(pinout.read_bytes()).hexdigest()
        if digest != "e30e3c804a31aa38f9de8bb6c184f8dea0868b86c03eda4131f5d00ef0034a95":
            raise RuntimeError("CP48BF Pocket pinout SHA-256 mismatch")

    def relative(p):
        return str(p.relative_to(ROOT))

    print("=== CP48BG: QUARTUS DECLARED-SOURCE CLOSURE AUDIT ===")
    print("Active HDL declarations:", len(hdl))
    print("Quartus QIP declarations:", len(qips))
    print("Other QSF-referenced files:", len(other))
    print("FX68K memory inputs:", len(CP48_MEM))
    print("Vendor-source provenance hashes:", len(vendors))
    print("Nonessential absent QIP MISC_FILE entries:",
          sum(not p.exists() for p in auxiliary))
    for p in sorted(auxiliary):
        if not p.exists():
            print("  OPTIONAL MISC_FILE NOT PRESENT:", relative(p))
    for p in sorted(missing):
        print("  MISSING:", relative(p))

    if missing:
        print("CLOSURE: INCOMPLETE —", len(missing), "missing input(s)")
        if not args.report_only:
            raise RuntimeError("Missing source dependencies; synthesis not attempted")
    else:
        print("CLOSURE: ALL 77 DECLARED HDL + FOUR QIPs + QSF/TCL + FX68K MEMORY PRESENT")
        print("PRIVATE LOCAL VENDOR HYDRATION: HASH VERIFIED")
    print("This is NOT a Quartus build, CDC/timing PASS, license clearance or full include audit.")
    print("READ ONLY — no synthesis, source changes, Git pushes, ROMs, or SD access.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP:", exc, file=sys.stderr)
        sys.exit(1)
