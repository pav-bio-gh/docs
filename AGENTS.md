# Agent notes for the Pav API docs

- This is a public repo. Never add secrets, internal hostnames, database or
  bucket names, internal commands, or unreleased features.
- `openapi.json` is copied from `https://api.pav.bio/v1/openapi.json` with
  `npm run refresh-openapi`. Do not hand-edit it, and do not hand-list API
  reference pages in `docs.json` — the `openapi` tab generates them.
- State what the API does today. Mark planned features as planned (see
  `webhooks/introduction.mdx`).
- Run `mint validate` and `mint broken-links` before opening a PR.
