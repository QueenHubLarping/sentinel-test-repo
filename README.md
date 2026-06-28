# sentinel-test-repo

A small, realistic Django commerce backend used to exercise
[**Sentinel**](https://github.com/Notchayan/sentinel-hq) end-to-end on real pull
requests and real GitHub APIs.

The code here deliberately implements three non-obvious engineering decisions that
are documented as ADRs in [`docs/adr/`](docs/adr/). Sentinel reads those ADRs as its
institutional memory and flags any PR that silently reverses one of them.

## What's here

| Area | Decision it implements | Files |
|------|------------------------|-------|
| Async confirmation email | **ADR-001** — dispatch email via a Celery/Redis queue, never inline | [`checkout/`](checkout/), [`email_service/`](email_service/) |
| Transactional storage | **ADR-002** — PostgreSQL (not MongoDB) for orders/payments | [`orders/`](orders/), [`payments/`](payments/) |
| Rate limiting | **ADR-003** — enforce at the API gateway, not in app code | [`api_gateway/`](api_gateway/) |

## How Sentinel runs here

[`.github/workflows/sentinel.yml`](.github/workflows/sentinel.yml) runs the published
Sentinel action (`Notchayan/sentinel-hq`) on every pull request. On first run it
ingests this repo's `docs/adr/` into its memory graph, then judges the incoming PR's
diff against those decisions and comments if the PR reverses one.

Requirements (one-time, on the self-hosted runner):

1. A **self-hosted runner** with Ollama running and `nomic-embed-text` pulled
   (Sentinel uses local embeddings).
2. A repo **Actions secret** `GROQ_API_KEY` (Sentinel uses Groq for reasoning).

## Try the reversal demo

```bash
# Opens a PR that makes checkout email synchronous again — reversing ADR-001.
GITHUB_TOKEN=<your-pat> ./scripts/open_reversal_pr.sh
```

Sentinel should comment that the PR reverses **ADR-001 (async email)** and explain the
original 800ms-latency rationale it found in `docs/adr/ADR-001-async-email.md`.
