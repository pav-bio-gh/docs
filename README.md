# Pav API docs

Source for the public Pav API and MCP server documentation, built with
[Mintlify](https://mintlify.com). This repo is the single source of the public
docs; the API itself lives at `https://api.pav.bio`.

## Layout

- `docs.json` — site config and navigation.
- `introduction.mdx`, `quickstart.mdx`, `authentication.mdx`, `mcp.mdx`,
  `rate-limits.mdx` — Get started.
- `concepts/` — entities, hybrid search, data quality and coverage.
- `webhooks/` — placeholder for push delivery.
- `openapi.json` — a copy of the live `https://api.pav.bio/v1/openapi.json`. The
  **API Reference** tab is generated from it; never hand-edit it.

## Local preview

Requires Node LTS (20.17–24; the `mint` CLI refuses Node 25+).

```bash
npm i -g mint
mint dev            # http://localhost:3000
mint validate       # strict build check
mint broken-links   # internal link check
```

## Updating after an API change

The API's OpenAPI schema is the source of truth for endpoints, parameters and
response shapes. After an API deploy:

```bash
npm run refresh-openapi   # re-pulls openapi.json from api.pav.bio
mint validate && mint broken-links
```

Then commit `openapi.json` together with any prose that mentions the change
(new entities go in `concepts/entities.mdx`; new MCP tools in the table in
`mcp.mdx`).

## Deployment

The Mintlify GitHub app deploys pushes to `main`. The site is served at the
custom domain configured in the Mintlify dashboard.
