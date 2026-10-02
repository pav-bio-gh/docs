# Pav API docs

Source for the public Pav API and MCP server documentation, built with
[Mintlify](https://mintlify.com) and published at
[docs.pav.bio](https://docs.pav.bio). The API itself lives at
`https://api.pav.bio`.

## Layout

- `docs.json`: site config and navigation. Sidebar groups of the
  **Documentation** tab:
  - Get started: `introduction.mdx`, `quickstart.mdx`, `fetching-data.mdx`,
    `mcp-server.mdx`. The MCP page lives at `/mcp-server` because Mintlify
    serves its own `/mcp`.
  - Datasets: `data-overview.mdx`, then `datasets/`, one page per dataset in
    collapsible sub-groups (Pipeline, Clinical and regulatory, Deals and
    patents). Each page has a short intro, an endpoint table, a **Fields**
    section, a **Filters** section and one example with a real trimmed
    response.
  - REST API: `authentication.mdx`, `rate-limits.mdx` (errors, retries).
  - SDK and CLI: `clients/`.
  - AI agents: `openapi-and-agents.mdx`.
  - Guides: `guides/`, task walkthroughs with example output.
  - Resources: `concepts/coverage-and-sources.mdx`.
- `fetching-data.mdx` explains what every list and get endpoint shares:
  filters, dates, sorting, paging, get by id, `view=slim`, missing values.
  Dataset pages link to it instead of repeating it.
- `introduction.mdx` routes and does not explain. It holds a short lead and
  card groups. Put tables and detail on the page a card links to.
- `api-reference/overview.mdx`: the first page of the **API Reference** tab,
  with one card per resource. The endpoint pages after it are generated.
- `webhooks/`: placeholder for planned push delivery.
- `openapi.json`: a copy of the live `https://api.pav.bio/v1/openapi.json`.
  The **API Reference** tab is generated from it; never hand-edit it. The
  sidebar group names ("Programs", "FDA") come from each tag's `x-group` in
  the spec. The page URLs come from the lowercase tag name.

## Writing conventions

- Plain, short sentences. Say what a thing is or does. No slogans or framing
  lines.
- Show fields and parameters one per block: `<ResponseField name type>` under
  **Fields** and `<ParamField query type default>` under **Filters**. Never
  group several names in one row or cell. Take names, types and defaults from
  `openapi.json`.
- A dataset page lists the main fields, not all of them; it links to the API
  Reference for the rest.
- cURL samples put the query string in the quoted URL
  (`curl "https://api.pav.bio/v1/programs?phase=phase_3&target=HER2"`), never
  `curl -G -d`. URL-encode a value only when it needs it (spaces, `&`, `#`).

## Design conventions

- Theme `almond`, light by default, with the light/dark toggle kept. It
  follows the Pav app: black text, Yves Klein Blue `#002FA7` as the one accent
  (links, active items, the main button), IBM Plex Sans. Dark mode uses the
  lighter blue `#8FA6E8` for text accents.
- The logo and `favicon.svg` use the blue iso-cube mark in `#002FA7` (a
  lighter `#5A7FE0` in the dark logo).
- Every page sets a [Lucide](https://lucide.dev) `icon:` in its frontmatter,
  and so does every card. `icons.library` is `lucide`, so Font Awesome names
  (`robot`, `magnifying-glass`) render blank. Check an icon name at
  lucide.dev and look at it in `mint dev`; `mint validate` does not catch a
  bad name.
- Code samples come in cURL, Python SDK and CLI tabs (`<CodeGroup>` with
  `icon=`). The API Reference shows generated samples in the languages under
  `api.examples.languages`.
- `custom.css` holds the "Soon" badge on the Webhook Reference tab, the
  segmented code-tab control, and the MCP install picker
  (`snippets/mcp-client-selector.jsx`). Its colors follow the same palette.

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
