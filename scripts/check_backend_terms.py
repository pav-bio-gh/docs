"""Fail when a file names how Pav is built (vendors, infrastructure, internal jargon).

python3 scripts/check_backend_terms.py <file> [<file> ...]   -> exit 1 and print each hit

A copy of the term list in pav-bio-gh/pav `platform/src/pav/enterprise_api/public_copy.py`
(`BACKEND_TERMS`), which the Pav API's own tests and deploy job enforce. Keep the two in
step. Product and vendor names are stored as SHA-256 hashes so this public repo does not
list them; generic wording is a plain pattern.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

GENERIC = re.compile(
    r"embedding|\bvector\b|scrap(e|ed|er|ing)|\betl\b|\bsql\b|data lake|fuzzy|run id|"
    r"crosswalk|keyset|\binternal\b|hybrid|semantic|canonical|resolv|confidence|"
    r"extracted|captured|\blegacy\b|stemming|linkage|prediction market|HTTPValidationError|"
    r"[a-z_]+\.[a-z_]+_(current|map|org)\b",
    re.IGNORECASE,
)

# sha256 of lowercased single words or two-word phrases.
HASHED = {
    "72970853ef1af198b035ccb385b3806a91fa60b5959bb27276eb464d2655701a",
    "635d603dcb715a7cb9d84c0c1891fb2347b3aaf930e76ca191741b01886ebeff",
    "c40dc72b0228e5850d8b173ff861a48acfb4a15b37b2849cbb6584bbadbc7907",
    "c1e9075ec2f631360c5fd774483629f9d0923769bfe82b2f3cfba3dfa93ba213",
    "c63a9876a150404eded185f01f7a574c6c9a96ce13e49a0e6b74db7c73ed0d23",
    "3347d0bdd97e6df866abddb2c3de496bbf1ad77d74745b688e70bc73bba31d8c",
    "23e5fe687c517d15a2d337201eda012b130d6680d7231dba51969631ef5f18bc",
    "e3ce9cc5efa9354c42b30704bed3e17cfad9ba9968592ffaa06b41dc7256cf4c",
    "d203a277f19a8f7d78fe8e9a621534b2cbd8ef1f0d809908ffc481e778858872",
    "caa54b0f54aa747d627d5d8a35f5e123317f8c3116cd321936e4fe0dcfe6d1d9",
    "44f3c8ab3bb645ae5c9471328dd7e1bacbd33dcca2e5865249dd005267ec4047",
    "e14d19846871cebcda43aeffc53a5a51619024682c37b51f74d1f26993300185",
    "a942b37ccfaf5a813b1432caa209a43b9d144e47ad0de1549c289c253e556cd5",
    "a478b4566be5cb007a5d8ae532c7eeac2cd3be26ad639a65c1dd11b3bf95c51b",
    "f344a3efa4668566d6fc2b09c5f6bfcc5b89d45cf426ab2560c2c6803e0201eb",
    "7edef0ca65ec70f862c5f624cee9d3970f22bc7afb32d2f7918e37cab16b8021",
    "e3b1e92b54e99f73344dfd942d957a4755c44a53217ddb03a79d23489c871e5e",
    "f19245cd282c13da78e784166d3d25007fdacdf34cd34dae4b47bcad5e4c1801",
    "1099ce900f147cf50627957017707cf936a7f3747a62c06bf3e7a28150f79c2a",
    "5eacb1d4a58ff383d7d22bc06308e25c48749c56084d8758601ba92835f2949b",
    "3c5221ad785c1eb3e91b28225485279e177c63e40fc5e46e06358b6b0e7fbd40",
}

# sha256 of lowercased URL schemes (the letters before "://").
SCHEMES = {
    "7a5443b6636713baa6350c1cf3ec620b2771a8d411ea3180c5d46b502b9ab77d",
}

TOKEN = re.compile(r"[a-z0-9_]+")
SCHEME = re.compile(r"\b([a-z]{2})://")


def _h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def hits(text: str) -> list[str]:
    found = [m.group(0) for m in GENERIC.finditer(text)]
    lower = text.lower()
    words = TOKEN.findall(lower)
    grams = set(words) | {f"{a} {b}" for a, b in zip(words, words[1:])}
    found += sorted(g for g in grams if _h(g) in HASHED)
    found += sorted(f"{m.group(1)}://" for m in SCHEME.finditer(lower) if _h(m.group(1)) in SCHEMES)
    return found


def main(argv: list[str]) -> int:
    failed = False
    for name in argv:
        found = hits(Path(name).read_text(encoding="utf-8"))
        for term in found:
            print(f"{name}: backend term {term!r}")
        failed = failed or bool(found)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
