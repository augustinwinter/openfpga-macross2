#!/usr/bin/env python3
"""Reassemble the verified Macross II Pocket ROM assets from a user-supplied
Japanese arcade ROM ZIP (macross2.zip). Requires only Python 3 stdlib.

Does not download, include, or redistribute copyrighted game data.
"""
import argparse
import hashlib
from pathlib import Path
import zipfile

# Verified CP48AJ against the Japanese macross2.zip on 2026-10-15.
# (filename, absolute offset, expected bytes, SHA-256 of original dump)
PARTS = [
    ("mcrs2j.3",     0x000000,  524288, "dae74e32833043a8e45cb7317ccbdba926e0a3e59f9bbd8c94f8b78e0673ea8e"),
    ("mcrs2j.2",     0x080000,  131072, "021648bb1e23d8624dcbc76bde0c69e9b7fe1b05aeab4f51988c8f5d2bac3043"),
    ("mcrs2j.1",     0x0A0000,  131072, "ef72d7ed45462d2f39a0b5e2a3935b71633644f59c023eb05f1935afd742c0db"),
    ("bp932an.a04",  0x0C0000, 2097152, "f122a49d5fa10611b28a8fab675715a0136cc6f95054da44288eeb8d966758a8"),
    ("bp932an.a07",  0x2C0000, 2097152, "4501b7dfb9be413ac9fe9c812da9ba15dc04af91a5560e19c89b38c27cd8ef7d"),
    ("bp932an.a08",  0x4C0000, 2097152, "6adc119a564bfe04e7da0eb90449391679276f94460a5020145e3f7b1b0d6bae"),
    ("bp932an.a06",  0x6C0000, 2097152, "6a48da61287692badf906359d1d0a241b47f978c7be8d31736e8206d3b5dc869"),
    ("bp932an.a05",  0x8C0000, 1048576, "2ea8a1f9820e24195621ab3b939bdc7d2a0cb39c8b85ad3853fe182c6964a1c3"),
]
HPROM = ("mcrs2bpr.9", 256, "09caf4d9d3b969e9439ce845d35b7dde21f44335d97a75a631a03dd00e8bc1cf")
VPROM = ("mcrs2bpr.10", 256, "82c14315be8bce00e93f92d9cf323bdd58c4d760b6ae983d4a3784e178c5272d")
ROM_BYTES = 0x9C0000
ROM_SHA = "2f6861637fa28a283a002d67982a67195eb93c33825a2661af2cebf421cf775d"
ARCHIVE_SHA = "b1ceb2e188aad2babe18336fc6dd9a70aef623da4b079c4f81b4549e8d5d17cf"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verified_member(z, name, size, expected_sha):
    payload = z.read(name)
    if len(payload) != size:
        raise ValueError(f"{name}: size {len(payload)} != expected {size}")
    if digest(payload) != expected_sha:
        raise ValueError(f"{name}: SHA-256 mismatch; wrong ROM revision or corrupted dump")
    return payload


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--romset", type=Path, required=True, help="Your legally obtained macross2.zip")
    ap.add_argument("--out-dir", type=Path, required=True, help="Destination for verified Pocket assets")
    ap.add_argument("--archival", action="store_true",
                    help="Also save archival image containing BOTH PROMs (not for Pocket data slot)")
    args = ap.parse_args()

    with zipfile.ZipFile(args.romset) as z:
        if z.testzip() is not None:
            raise ValueError("Input ZIP failed integrity test")
        image = bytearray()
        for name, offset, size, expected_sha in PARTS:
            if len(image) != offset:
                raise ValueError(f"{name}: expected offset 0x{offset:X}, got 0x{len(image):X}")
            image.extend(verified_member(z, name, size, expected_sha))
            print(f"VERIFIED {name} @ 0x{offset:06X}")
        hprom = verified_member(z, *HPROM)
        vprom = verified_member(z, *VPROM)

    rom = bytes(image)
    full = rom + hprom + vprom
    assert len(rom) == ROM_BYTES and digest(rom) == ROM_SHA, "ROM assembly mismatch"
    assert len(full) == ROM_BYTES + 512 and digest(full) == ARCHIVE_SHA, "Archival image mismatch"

    outputs = {
        "macross2.rom": rom,
        "macross2_vprom.bin": vprom,
    }
    if args.archival:
        outputs["macross2-archival.rom"] = full

    out = args.out_dir.expanduser()
    if any((out / name).exists() for name in outputs):
        raise FileExistsError("One or more output files already exist; choose an empty destination")
    out.mkdir(parents=True, exist_ok=True)
    for name, data in outputs.items():
        path = out / name
        with path.open("xb") as stream:
            stream.write(data)
        assert path.read_bytes() == data
        print(f"CREATED {path} [{len(data)} bytes] SHA-256 {digest(data)}")
    print("PASS: all ten input chips, assembled ROM and PROMs exactly match CP48AJ")


if __name__ == "__main__":
    main()
