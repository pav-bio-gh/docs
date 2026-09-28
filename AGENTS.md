# Agent notes for the Pav API docs

- This is a public repo. Never add secrets, API keys, internal hostnames, or
  unreleased features.
- Describe behavior from the customer's side only. No vendor, infrastructure,
  database, table, module, job or internal process names; no internal
  metrics. Name public data sources (ClinicalTrials.gov, SEC, USPTO, company
  pipelines) only as provenance.
- `openapi.json` is copied from `https://api.pav.bio/v1/openapi.json` with
  `npm run refresh-openapi`. Do not hand-edit it, and do not hand-list API
  reference pages in `docs.json`; the `openapi` tab generates them.
- State what the API does today. Mark planned features as planned (see
  `webhooks/introduction.mdx`).
- Every code sample must run against the live API. Example responses are real,
  trimmed, and labeled as examples.
- Run `mint validate` and `mint broken-links` before opening a PR.
