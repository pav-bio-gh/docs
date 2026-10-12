# Agent notes for the Pav API docs

- This is a public repo. Never add secrets, API keys, private hostnames, or
  unreleased features.
- Describe behavior from the customer's side only. No vendor, infrastructure,
  database, table, module, job or process names; no operational metrics. Name
  public data sources (ClinicalTrials.gov, SEC, USPTO, FDA, company pipelines)
  only as provenance.
- `openapi.json` is a copy of `https://api.pav.bio/v1/openapi.json`. The hourly
  `openapi-sync` workflow commits the refreshed spec to `main`; by hand,
  run `npm run refresh-openapi`. Do not hand-edit it. Each endpoint has its own
  page under `datasets/` (README, "Endpoint pages"); a new endpoint needs a new
  page. Do not put `openapi` on a tab or group in `docs.json`.
- State what the API does today. Mark planned features as planned (see
  `webhooks/introduction.mdx`).
- Every code sample must run against the live API. Example responses are real,
  trimmed, and labeled as examples. `scripts/refresh_examples.py` writes the
  endpoint pages' examples from the live API; do not hand-edit them.
- Never name a sidebar group or page "X and Y" when X and Y are separate
  things. Give each its own page or group. One topic ("Rate limits and
  errors") and section subheaders are fine (README, "Writing conventions").
- Run `mint validate` and `mint broken-links` before opening a PR.
