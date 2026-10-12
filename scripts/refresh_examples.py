"""Rewrite each endpoint page's example response from the live API.

PAV_API_KEY=... python3 scripts/refresh_examples.py   -> rewrites datasets/**/*.mdx

For every page under datasets/, it calls the URL in the page's cURL sample and
replaces the page's <ResponseExample> with the response, trimmed: a list keeps
its first row; inside a record an array of objects keeps its first item
(`companies` its first two) and an array of strings its first three. Values are
never edited and every field the API returned stays. Exits 1, writing nothing
for that page, when a sample does not return 200.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURL = re.compile(r'curl "?(https://api\.pav\.bio/v1/[^"\s]+)"?')
BLOCK = re.compile(r"\n*<ResponseExample>.*?</ResponseExample>\n*", re.S)
WIDTH = 80


def api_key() -> str:
    key = os.environ.get("PAV_API_KEY")
    saved = Path.home() / ".config" / "pav" / "credentials"
    if not key and saved.exists():
        key = saved.read_text().strip()
    if not key:
        sys.exit("set PAV_API_KEY or save a key to ~/.config/pav/credentials")
    return key


def fetch(url: str, key: str) -> tuple[int, object]:
    request = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {key}", "User-Agent": "pav-docs-examples"}
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, None


def trim(value, key=None):
    if isinstance(value, dict):
        return {k: trim(v, k) for k, v in value.items()}
    if isinstance(value, list):
        keep = 1 if any(isinstance(v, (dict, list)) for v in value) else 3
        if key == "companies":
            keep = 2  # a deal's two parties, a drug's developers
        return [trim(v) for v in value[:keep]]
    return value


def render(value, indent: int = 0) -> str:
    """JSON with short objects and arrays kept on one line."""
    flat = json.dumps(value, ensure_ascii=False, separators=(", ", ": "))
    if isinstance(value, dict) and value:
        flat = "{ " + flat[1:-1] + " }"
    if not isinstance(value, (dict, list)) or not value or indent + len(flat) <= WIDTH - 4:
        return flat
    pad = " " * (indent + 2)
    if isinstance(value, dict):
        items = [f"{pad}{json.dumps(k)}: {render(v, indent + 2)}" for k, v in value.items()]
        return "{\n" + ",\n".join(items) + "\n" + " " * indent + "}"
    items = [f"{pad}{render(v, indent + 2)}" for v in value]
    return "[\n" + ",\n".join(items) + "\n" + " " * indent + "]"


def example(body: dict) -> str:
    if isinstance(body.get("data"), list):
        body = {**body, "data": [trim(row) for row in body["data"][:1]]}
    else:
        body = trim(body)
    lines = [f"  {json.dumps(k)}: {render(v, 2)}" for k, v in body.items()]
    return "{\n" + ",\n".join(lines) + "\n}"


def main() -> int:
    key = api_key()
    failed = 0
    for page in sorted((ROOT / "datasets").rglob("*.mdx")):
        rel = page.relative_to(ROOT)
        text = page.read_text()
        match = CURL.search(text)
        if not match:
            continue
        status, body = fetch(match.group(1), key)
        if status != 200 or not isinstance(body, dict):
            failed += 1
            print(f"{rel}: {status} from {match.group(1)}; left unchanged")
            continue
        block = (
            "\n\n<ResponseExample>\n\n```json Example response (trimmed)\n"
            + example(body)
            + "\n```\n\n</ResponseExample>\n"
        )
        page.write_text(BLOCK.sub("\n", text).rstrip("\n") + block)
        print(f"{rel}: updated from {match.group(1)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
