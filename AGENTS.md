# Agent notes for the Pav API docs

- This is a public repo. Never add secrets, API keys, private hostnames, or
  unreleased features.
- Describe behavior from the customer's side only. No vendor, infrastructure,
  database, table, module, job or process names; no operational metrics. Name
  public data sources (ClinicalTrials.gov, SEC, USPTO, FDA, company pipelines)
  only as provenance.
- `openapi.json` is a copy of `https://api.pav.bio/v1/openapi.json`. The hourly
  `openapi-sync` workflow opens a pull request here that refreshes it; by hand,
  run `npm run refresh-openapi`. Do not hand-edit it, and do not hand-list API
  reference pages in `docs.json`; the `openapi` tab generates them.
- State what the API does today. Mark planned features as planned (see
  `webhooks/introduction.mdx`).
- Every code sample must run against the live API. Example responses are real,
  trimmed, and labeled as examples.
- Run `mint validate` and `mint broken-links` before opening a PR.
