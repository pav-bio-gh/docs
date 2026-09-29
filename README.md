# Pav API docs

Source for the public Pav API and MCP server documentation, built with
[Mintlify](https://mintlify.com) and published at
[docs.pav.bio](https://docs.pav.bio). The API itself lives at
`https://api.pav.bio`.

## Layout

- `docs.json`: site config and navigation.
- `introduction.mdx`, `quickstart.mdx`, `authentication.mdx`,
  `rate-limits.mdx`: Get started.
- `datasets/`: one page per dataset (programs, drugs, companies, clinical
  trials, deals, patents, FDA records, FDA applications and reviews, changes):
  overview, coverage, key fields, filters, and example queries with real
  trimmed responses.
- `concepts/`: search and filters, pagination, coverage and sources.
- `mcp-server.mdx`, `openapi-and-agents.mdx`: Integrations. The MCP page lives
  at `/mcp-server` because Mintlify serves its own `/mcp`.
- `guides/`: task walkthroughs with runnable scripts and example output.
- `webhooks/`: placeholder for planned push delivery.
- `openapi.json`: a copy of the live `https://api.pav.bio/v1/openapi.json`.
  The **API Reference** tab is generated from it; never hand-edit it.

## Local preview

Requires Node LTS (20.17–24; the `mint` CLI refuses Node 25+).

```bash
npm i -g mint
mint dev            # http://localhost:3000
mint validate       # strict build check
mint broken-links   # link check
```

## Updating after an API change

The OpenAPI spec is the source of truth for endpoints, parameters and response
shapes. The **Sync openapi.json** workflow
(`.github/workflows/openapi-sync.yml`) runs hourly. It fetches
`https://api.pav.bio/v1/openapi.json`, fails if the spec names how Pav is built
(`scripts/check_backend_terms.py`), and, when the spec differs from
`openapi.json`, opens or updates one pull request titled "Refresh openapi.json
from api.pav.bio" from the `openapi-sync` branch. Review and merge it.

Run it now, and check the result:

```bash
gh workflow run openapi-sync.yml -R pav-bio-gh/docs
gh run list -R pav-bio-gh/docs --workflow openapi-sync.yml --limit 1
```

A run with an unchanged spec logs "openapi.json already matches" and opens
nothing. The workflow rebuilds `openapi-sync` from `main` on every run, so
merging or closing its pull request is always safe. It needs the repository
setting "Allow GitHub Actions to create and approve pull requests". To refresh
by hand instead:

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
