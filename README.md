# Pav API docs

Source for the public Pav API and MCP server documentation, built with
[Mintlify](https://mintlify.com) and published at
[docs.pav.bio](https://docs.pav.bio). The API itself lives at
`https://api.pav.bio`.

## Layout

- `docs.json`: site config and navigation. Sidebar groups of the
  **Documentation** tab:
  - Overview: `introduction.mdx`, `quickstart.mdx`, `data-overview.mdx`.
  - Datasets: `datasets/`, one page per dataset in collapsible sub-groups
    (Pipeline, Clinical and regulatory, Deals and patents). Each page has one
    sentence, a key-fields table, a parameters table and one example (cURL
    and Python) with a real trimmed response. There is no shared
    "Conventions" page; each parameter's own description states its rule
    (ids, comma-separated values, dates, sorting, paging).
  - REST API: `authentication.mdx`, `rate-limits.mdx` (errors, retries).
  - AI agents: `mcp-server.mdx`, `openapi-and-agents.mdx`. The MCP page lives
    at `/mcp-server` because Mintlify serves its own `/mcp`.
  - Guides: `guides/`, task walkthroughs with runnable scripts and example
    output.
  - Resources: `concepts/coverage-and-sources.mdx`.
- `introduction.mdx` routes and does not explain. It holds a lead paragraph
  and card groups (start, datasets, guides). Put tables and detail on the page a card links to.
- `api-reference/overview.mdx`: the first page of the **API Reference** tab,
  with one card per resource. The endpoint pages after it are generated.
- `webhooks/`: placeholder for planned push delivery.
- `openapi.json`: a copy of the live `https://api.pav.bio/v1/openapi.json`.
  The **API Reference** tab is generated from it; never hand-edit it. The
  sidebar group names ("Programs", "FDA") come from each tag's `x-group` in
  the spec. The page URLs come from the lowercase tag name.

## Design conventions

- Theme `almond`, dark by default with the light/dark toggle kept. The chrome
  is monochrome (`colors` near-black / near-white). The only brand color is
  the blue iso-cube mark in `logo/` and `favicon.svg`.
- Every page sets a [Lucide](https://lucide.dev) `icon:` in its frontmatter,
  and so does every card. `icons.library` is `lucide`, so Font Awesome names
  (`robot`, `magnifying-glass`) render blank. Check an icon name at
  lucide.dev and look at it in `mint dev`; `mint validate` does not catch a
  bad name.
- The API Reference shows generated code samples in cURL, Python, JavaScript
  and Go (`api.examples.languages`). Adding a language means running its
  generated sample against the live API first.
- `custom.css` holds only the "Soon" badge on the Webhook Reference tab.

## Local preview

Requires Node LTS (20.17–24; the `mint` CLI refuses Node 25+).

```bash
npm i -g mint
mint dev            # http://localhost:3000
mint validate       # strict build check
mint broken-links   # link check
```

Opening an API Reference page makes `mint dev` grow past 2 GB. To cap it,
start it with `NODE_OPTIONS=--max-old-space-size=900 mint dev`; it then stays
near 1.4 GB.

## Updating after an API change

The OpenAPI spec is the source of truth for endpoints, parameters and response
shapes. The **Sync openapi.json** workflow
(`.github/workflows/openapi-sync.yml`) runs hourly and on demand. It fetches
`https://api.pav.bio/v1/openapi.json` and, when it differs from `openapi.json`
on `main`, commits it straight to `main` (Mintlify then deploys it). Before
committing it checks that the spec names nothing about how Pav is built
(`scripts/check_backend_terms.py`), parses as OpenAPI 3.x, and still builds
the site (`mint validate`); any failure stops the run and leaves `main`
unchanged.

Run it now, and check the result:

```bash
gh workflow run openapi-sync.yml -R pav-bio-gh/docs
gh run list -R pav-bio-gh/docs --workflow openapi-sync.yml --limit 1
```

A run with an unchanged spec logs "openapi.json already matches" and commits
nothing. A run that commits logs "committed <sha> to main". A failed run
names the failing check in its log; fix the cause (for a backend term, the
route or schema description in the API) and re-run. To refresh by hand
instead:

```bash
npm run refresh-openapi   # re-pulls openapi.json from api.pav.bio
mint validate && mint broken-links
```

Then update any prose that mentions the change: the dataset page under
`datasets/`, the tool table in `mcp-server.mdx` for a new endpoint, and any
guide that uses it. Re-run every code sample you touched against the live API
with a real key, and paste real trimmed responses labeled as examples.

## Deployment

The Mintlify GitHub app deploys pushes to `main`.
