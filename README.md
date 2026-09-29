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
shapes. Every production API deploy opens (or updates) a pull request titled
"Refresh openapi.json from api.pav.bio" on the `openapi-sync` branch when the
live spec differs from `openapi.json`. Review and merge it. To refresh by hand:

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
