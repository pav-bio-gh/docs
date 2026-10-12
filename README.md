# Pav API docs

Source for the public Pav API and MCP server documentation, built with
[Mintlify](https://mintlify.com) and published at
[docs.pav.bio](https://docs.pav.bio). The API itself lives at
`https://api.pav.bio`.

## Layout

- `docs.json`: site config and navigation. Sidebar groups of the
  **Documentation** tab:
  - Get Started: `introduction.mdx`, `quickstart.mdx`, `mcp-server.mdx`. The MCP page lives at `/mcp-server` because Mintlify
    serves its own `/mcp`.
  - Datasets: `data-overview.mdx`, then one page per endpoint under
    `datasets/`, in sub-groups: Pipeline (All Programs, Program, All Drugs,
    Drug), Deals, Patents, Companies, Global Trials, FDA. FDA has a page per
    record type's list (`datasets/fda/`) plus Drug Application; each FDA list
    page explains its get-by-key call. These pages are the API reference;
    there is no separate API Reference tab.
  - REST API: `authentication.mdx`, `rate-limits.mdx` (errors, retries).
  - Clients: `clients/` (Python SDK, CLI).
  - AI Agents: `openapi-spec.mdx`.
  - Guides: `guides/`, task walkthroughs with example output.
  - Resources: `fetching-data.mdx`.
- `data-overview.mdx` holds the dataset table (grain, join ids) and the FDA
  record-type table (date and `status` per type).
- `fetching-data.mdx` explains what every list and get endpoint shares:
  filters, dates, sorting, paging, get by id, `view=slim`, missing values.
  Endpoint pages link to it instead of repeating it.
- `introduction.mdx` routes and does not explain. It holds a short lead and
  card groups. Put tables and detail on the page a card links to.
- `webhooks/`: placeholder for planned push delivery.
- `openapi.json`: a copy of the live `https://api.pav.bio/v1/openapi.json`;
  never hand-edit it. `api.openapi` in `docs.json` points at it, and each
  endpoint page names its operation in `openapi:` frontmatter. Do not put
  `openapi` on a navigation tab or group: Mintlify then adds every endpoint to
  the sidebar a second time. Old `/api-reference/...` URLs redirect to the
  endpoint pages (`redirects` in `docs.json`).

## Endpoint pages

Each endpoint page under `datasets/` has this shape (see
`datasets/programs.mdx`):

- Frontmatter: `title`, `openapi: "GET /v1/<path>"` and a one-line
  `description`.
- `## Overview`: what one record is, anything a reader must know that the
  parameter descriptions do not say, and one line on what the example shows.
- `<RequestExample>` with the cURL, Python SDK and CLI blocks, and
  `<ResponseExample>` with the live response to the cURL sample, labeled
  "Example response (trimmed)". Mintlify shows both in the right-hand column.
  `scripts/refresh_examples.py` writes the `<ResponseExample>` (see "Updating
  after an API change"); do not hand-edit it. Every endpoint page needs one:
  without it Mintlify shows the example generated from the spec, which uses
  one Orange Book record for every FDA record type.
- Nothing else. Mintlify renders the Try it bar and the parameters and
  response fields from the spec below the overview, so never hand-write
  `<ParamField>` or `<ResponseField>` blocks for an endpoint.

Guides and the other pages are ordinary pages with an "On this page" list.

## Writing conventions

- Plain, short sentences. Say what a thing is or does. No slogans or framing
  lines.
- Never join two separate things in one sidebar group or page name ("Deals
  and patents", "Clinical and regulatory", "OpenAPI and agents"). Give each
  its own page or group. An "and" is fine when the name is one topic ("Rate
  limits and errors", "Check patents and loss of exclusivity") and in section
  subheaders ("List and get"). Only make a group when two or more pages share
  one name, like Pipeline (Programs, Drugs).
- Sidebar names are Title Case: page titles ("Rate Limits and Errors", "Data
  Overview") and group names ("Get Started"). Name an endpoint page after what
  it returns: "All Programs" for a list in a group of the same name, "Warning
  Letters" for a list otherwise, "Program" for one record. Never "List …" or
  "Get …".
- cURL samples put the query string in the quoted URL
  (`curl "https://api.pav.bio/v1/programs?phase=phase_3&target=HER2"`), never
  `curl -G -d`. URL-encode a value only when it needs it (spaces, `&`, `#`).

## Design conventions

- Theme `almond`, light by default, with the light/dark toggle kept. It
  follows the Pav app: black text, Yves Klein Blue `#002FA7` as the one accent
  (links, the current page and section, the main button), Geist. Dark mode
  uses the lighter blue `#8FA6E8` for text accents.
- Geist is self-hosted from `fonts/` (the app's files). `docs.json` points
  `fonts` at the Latin file, and two `@font-face` rules in `custom.css` give it
  the 100–900 weight range, which Mintlify's own rule leaves out.
- Text follows the app's type rules. All text is black in light mode:
  `custom.css` sets the theme's grey text shades (`--gray-500` to
  `--gray-950`) to black, so hierarchy comes from size and weight. `--gray-400`
  becomes the app's one hint grey `#71717A`, for skippable hints like the
  search shortcut. The type scale is 1px under Tailwind's default (body 15px,
  sidebar 13px), and table headers are weight 300. Field names and their type
  pills are black, not blue.
- The page column is up to 46rem wide on desktop (the theme caps it at 36rem),
  and the "On this page" rail is 15rem. Endpoint pages put the examples in that
  right-hand space instead. Check a change at 1440px and 375px.
- On endpoint pages the GET badge is a grey chip with black text, and Try it
  is ink, so the navbar's Get API key stays the one blue button.
- The logo and `favicon.svg` use the blue iso-cube mark in `#002FA7` (a
  lighter `#5A7FE0` in the dark logo).
- Every page except an endpoint page (which shows its GET badge instead) sets
  a [Lucide](https://lucide.dev) `icon:` in its frontmatter, and so does every
  card and every Datasets sub-group. `icons.library` is `lucide`, so Font Awesome names
  (`robot`, `magnifying-glass`) render blank. Check an icon name at
  lucide.dev and look at it in `mint dev`; `mint validate` does not catch a
  bad name.
- Code samples come in cURL, Python SDK and CLI tabs (`<CodeGroup>`, or
  `<RequestExample>` on an endpoint page, with `icon=`).
- `custom.css` holds the font, type and color rules above, the page width,
  the "Soon" badge on the Webhook Reference tab, the segmented code-tab
  control (icons hidden on phones so the tabs fit on one row), and the MCP
  install picker (`snippets/mcp-client-selector.jsx`). Its colors follow the
  same palette.

## Analytics

`integrations.posthog` in `docs.json` sends page views and session recordings
to the same PostHog project as pav.bio and app.pav.bio. The key is the public
`phc_` project key those sites already ship. Keep the one shared project:
it is what links a docs reader to the same person when they sign up. Filter by
`$host = docs.pav.bio` to see only the docs. Mintlify's dashboard also has its
own page-view and search analytics.

## Local preview

Requires Node LTS (20.17–24; the `mint` CLI refuses Node 25+).

```bash
npm i -g mint
mint dev            # http://localhost:3000
mint validate       # strict build check
mint broken-links   # link check
```

Opening an endpoint page makes `mint dev` grow past 2 GB. To cap it,
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

A changed parameter or field shows up on its endpoint page by itself. Pages
are not generated, so:

- A new endpoint needs its own page under `datasets/` (copy a sibling, see
  "Endpoint pages"), an entry in its `docs.json` sub-group, and a row in the
  tool table in `mcp-server.mdx`.
- A removed endpoint: delete its page and its `docs.json` entry, and add a
  redirect from its URL to the nearest page.
- Run `python3 scripts/check_endpoint_pages.py`. It lists endpoints with no
  page and pages whose endpoint the spec no longer has, and exits 1 on either.
  `mint validate` catches neither: the hourly sync still commits the new spec,
  and a page whose endpoint is gone just loses its Try it bar and parameter
  list. Then look at every changed page in `mint dev`.
- Run `python3 scripts/refresh_examples.py` with a key in `PAV_API_KEY` (or
  saved to `~/.config/pav/credentials`). It calls each endpoint page's cURL
  sample and rewrites the page's example response from the live result. When
  a sample does not return 200 it names the page, leaves it unchanged and
  exits 1; fix that sample (an id that no longer exists, a renamed parameter)
  and re-run. Read the diff before committing: a field that disappeared from
  an example disappeared from the API.

Then update any prose that mentions the change, including any guide that uses
it. Re-run every code sample you touched against the live API with a real key.
Guide examples are pasted by hand: use real trimmed responses labeled as
examples.

## Deployment

The Mintlify GitHub app deploys pushes to `main`.
