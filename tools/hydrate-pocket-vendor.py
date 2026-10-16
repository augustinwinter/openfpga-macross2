#!/usr/bin/env python3
"""Hydrate *untracked* vendor source dependencies from the pinned Pocket template.

Original upstream licenses still apply. This script does not grant license rights,
does not place vendor files in Git, and does not substitute for legal clearance.
Requires explicit --accept-upstream-licenses; never overwrites existing bytes.

The eight files are the 7 CP48AX-exact vendor/template HDL counterparts plus the
template's pinout Tcl. Unlike the 7 HDL, the pinout Tcl has NOT YET been confirmed
byte-identical to the successful frozen Macross II source: compare before compiling.
"""

import argparse
import hashlib
import subprocess
import sys
import urllib.request
from pathlib import Path

PIN = "c77563fa84bcc5754d5f1f6ba51168e8849f0e1d"
UPSTREAM = "plasticbugs/pocket-core-template"
EXPECTED = {
    "platform/pocket/bsp/pocket/apf_top.sv":
        "3eda9ab341a980f58b93f4750c3b2fbd48833ef7",
    "platform/pocket/peripherals/io_bridge_peripheral.sv":
        "bfb9d00512ad119ecc284a5f81d9f9cceb98b2a1",
    "platform/pocket/peripherals/io_pad_controller.sv":
        "478b22ff0136e7d9e061383d2246083b506db086",
    "platform/pocket/megafunctions/mf_audio_pll/mf_audio_pll_0002.v":
        "86e4d755aeb8afd9a8384114b25377f7b532a6af",
    "platform/pocket/megafunctions/mf_audio_pll.v":
        "663340626d78b5683b27682640b4fd7cee14def5",
    "platform/pocket/megafunctions/mf_datatable.v":
        "0db807d1d41609d30a1fbb0acc8278dc4737d6b1",
    "platform/pocket/megafunctions/mf_ddio_bidir_12.v":
        "6bac1ab99a010304edf88808197fa7703ac340b9",
}
PINOUT = (
    "platform/pocket/bsp/pocket/pinouts/system.tcl",
    "42534ded84f0dbf3f454f7f4b1b42bc71c43e43c",
)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def run(*argv: str) -> str:
    result = subprocess.run(argv, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(
            f"{' '.join(argv)}: {result.stderr[-1000:]}"
        )
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--accept-upstream-licenses", action="store_true",
        help="Confirm you will obtain/use the upstream APF and Intel sources under their own licenses",
    )
    parser.add_argument(
        "--include-template-pinout", action="store_true",
        help="Also hydrate unverified template system.tcl; compare its hash with the frozen successful build before compiling",
    )
    args = parser.parse_args()
    if not args.accept_upstream_licenses:
        parser.error(
            "explicit --accept-upstream-licenses is required; "
            "see https://assets.analogue.co/pdf/43478bf701eb4905172acbecc3babae9/"
            "Analogue%2BEULA%2BAugust%2B14%2B2022.pdf and the Intel IP notices"
        )

    root = Path(__file__).resolve().parent.parent
    tracked = run("git", "-C", str(root), "rev-parse", "--show-toplevel")
    if tracked != str(root):
        raise RuntimeError("Run from a Macross II repository clone, not a source copy")

    items = list(EXPECTED.items())
    if args.include_template_pinout:
        items.append(PINOUT)

    downloaded = []
    for relative, expected_sha in items:
        target = root / relative
        if target.is_symlink():
            raise RuntimeError(f"Refusing symlink path: {relative}")
        url = (
            f"https://raw.githubusercontent.com/{UPSTREAM}/{PIN}/{relative}"
        )
        request = urllib.request.Request(
            url, headers={"User-Agent": "Macross-II-Licensed-Dependency-Hydrator"}
        )
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read()
        actual = git_blob(data)
        if actual != expected_sha:
            raise RuntimeError(
                f"Upstream hash mismatch for {relative}: {actual}"
            )
        if target.exists() and target.read_bytes() != data:
            raise RuntimeError(
                f"Existing file differs from PINNED template: {relative}. "
                "Do not overwrite frozen/local code."
            )
        downloaded.append((relative, target, data, expected_sha))

    for relative, target, data, sha in downloaded:
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        if git_blob(target.read_bytes()) != sha:
            raise RuntimeError(f"Byte verification failed: {relative}")
        print("VERIFIED:", relative, sha)

    print("\nHYDRATION COMPLETE — local files only, none staged or pushed.")
    print("CHECK: the modified APF core_bridge_cmd.sv is NOT supplied here.")
    if args.include_template_pinout:
        print("WARNING: pinout Tcl lineage not yet compared to Macross II frozen source.")
    else:
        print("CHECK: the required pinout system.tcl is NOT supplied here.")
    print("No FPGA synthesis was run. Vendor terms continue to apply.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP:", exc, file=sys.stderr)
        sys.exit(1)
