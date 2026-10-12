"""Check that every endpoint in openapi.json has a page and every page an endpoint.

python3 scripts/check_endpoint_pages.py   -> exit 1 and print each problem

Endpoint pages under datasets/ name their operation in `openapi:` frontmatter.
Mintlify does not fail the build when that operation is gone from the spec (the
page just loses its Try it bar and parameter list), and it does not add a page
for a new endpoint. An FDA get-by-record_key endpoint needs no page of its own:
its list page explains it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER = re.compile(r'^openapi:\s*"?(GET|POST|PUT|PATCH|DELETE) ([^"\s]+)"?\s*$', re.M)


def main() -> int:
    spec = json.loads((ROOT / "openapi.json").read_text())
    operations = {
        f"{method.upper()} {path}"
        for path, item in spec["paths"].items()
        for method in item
        if method in {"get", "post", "put", "patch", "delete"}
    }
    pages: dict[str, Path] = {}
    for page in sorted((ROOT / "datasets").rglob("*.mdx")):
        match = FRONTMATTER.search(page.read_text())
        if match:
            pages[f"{match.group(1)} {match.group(2)}"] = page.relative_to(ROOT)

    problems = []
    for operation, page in pages.items():
        if operation not in operations:
            problems.append(f"{page}: names {operation}, which openapi.json does not have")
    for operation in sorted(operations - pages.keys()):
        path = operation.split(" ", 1)[1]
        if path.endswith("/{record_key}") and f"GET {path.rsplit('/', 1)[0]}" in pages:
            continue
        problems.append(f"{operation}: no page under datasets/")
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
