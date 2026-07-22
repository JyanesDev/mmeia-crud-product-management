# Deployment

## Local (this project's only target — see scope in `spec.md`)

```bash
docker compose -f docker/docker-compose.yml up
```

Two services: `api` (built from `docker/Dockerfile`) and `db` (official `postgres` image). Connection string and credentials via environment variables (`.env`, gitignored; `.env.example` committed with placeholder values).

## What is deliberately not here

No Kubernetes manifests, no cloud provider config, no CI/CD deploy step beyond the test pipeline — a CRUD pilot's scope doesn't justify any of it (`docs/architecture.md`). If a future Reference Project (SaaS) needs real production deployment, that's where it belongs.

## CI

`.github/workflows/ci.yml`: on every push, build the Docker image, run `pytest` against a throwaway PostgreSQL service container. No deploy step — CI here only gates merges, it doesn't ship anything.
