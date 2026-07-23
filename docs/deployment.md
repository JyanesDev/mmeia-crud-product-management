# Deployment

## Local (this project's only target — see scope in `spec.md`)

```bash
cp .env.example .env   # fill in real values first
docker compose -f docker/docker-compose.yml --env-file .env up -d --build
```

Two services: `api` (built from `docker/Dockerfile`) and `db` (official `postgres:16` image, auto-initialized with `db/schema.sql` via `docker-entrypoint-initdb.d`). Connection string and credentials via environment variables (`.env`, gitignored; `.env.example` committed with placeholder values).

## What is deliberately not here

No Kubernetes manifests, no cloud provider config — a CRUD pilot's scope doesn't justify any of it (`docs/architecture.md`). If a future Reference Project (SaaS) needs real production deployment, that's where it belongs.

## CI

`.github/workflows/ci.yml`: 3 jobs chained with `needs:` — `build` (Docker image, saved as an artifact), `test` (pytest against a real PostgreSQL 16 service container), `deploy` (loads the built image; since this project's declared target is local Docker Compose, not a remote host, "deploy" here means the tested image is the artifact an operator pulls and runs — there is no remote push step).

**Honest limitation:** the workflow's YAML was validated locally (`python -c "import yaml; yaml.safe_load(...)"`) but has not been observed running on a real GitHub Actions runner in this session — no `gh` CLI was available to trigger and watch a run. It will execute for real on the next push to GitHub; if it fails there, that's new evidence to fold in before `v1.0.0`.

## Real deployment evidence (M3, 2026-07-22)

Executed for real, not simulated — `docker compose up -d --build` from a clean `.env`, both containers reached a healthy state with no manual steps beyond providing `.env` (NFR2 in `requirements.md`).

Full verification (Playbook `03_Preparar_Despliegue`, Paso 6 — all 5 points, including a genuine 5-minute wait):

```text
1. Disponibilidad     -> GET /health -> 200 {"status":"ok","version":"0.3.0"}
2. Salud               -> mismo endpoint, mismo resultado
3. Version reportada   -> "0.3.0", coincide con la esperada
4. Version anterior    -> mmeia-crud-product-management:0.2.0 presente en `docker images`
                          (reconstruida desde el tag real v0.2.0 via git worktree,
                          para que esta comprobación tenga sustancia real y no sea
                          un cheque vacío en el primer despliegue del proyecto)
5. Estabilidad 5 min    -> misma respuesta tras esperar 300s reales; contenedores
                          "Up 17 minutes (healthy)" en la comprobación final
```

Playbook Checklist final: 10/10 satisfied.
