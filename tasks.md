# Tasks

Derived from `spec.md`, ordered to match the composition already declared in MMEIA's `REFERENCE_PROJECT.md §7`: `01_Disenar_Base_Datos` → `02_Crear_API` → `03_Preparar_Despliegue`. Each task should be small enough to review in one sitting (`08_Implementacion.md` Paso 3).

## Milestone M0 — Scaffold

- [ ] Repository created, `README.md`/`spec.md`/`requirements.md`/`tasks.md` committed as first commit.
- [ ] `.github/workflows/ci.yml` — lint + test job, green on an empty test suite.
- [ ] Tag `v0.0.1`.

## Milestone M1 — Schema (applies `01_Disenar_Base_Datos`) — DONE 2026-07-22

- [x] `Categoria` table: `id`, `nombre` (unique), `descripcion`.
- [x] `Producto` table: `id`, `nombre`, `descripcion`, `precio`, `categoria_id` (FK, `ON DELETE RESTRICT`), `estado` (`CHECK` enum, default `borrador`).
- [x] `Stock` table: `id`, `producto_id` (FK, unique — 1:1, `ON DELETE CASCADE`), `cantidad` (`CHECK (cantidad >= 0)`, default 0).
- [x] `disenio.md` (Pasos 1-4 del Playbook) and `db/schema.sql` (Paso 5) committed.
- [x] Schema applied against a real, disposable PostgreSQL 16 container and verified with 5 constraint tests, all failing exactly as required (`db/VERIFICATION.md`, Paso 6).
- [x] Tag `v0.1.0`.

Playbook Checklist final (7/7): satisfied — see `db/VERIFICATION.md` and `disenio.md`.

## Milestone M2 — API (applies `02_Crear_API`)

- [ ] `POST /categorias`, `GET /categorias`, `DELETE /categorias/{id}` (FR3, with the referenced-products check).
- [ ] `POST /productos` (FR1), `GET /productos/{id}`, `GET /productos` with pagination + filters (FR2).
- [ ] `POST /productos/{id}/transicion` (FR5, state machine validation).
- [ ] `PATCH /productos/{id}/stock` (FR4, delta-based adjustment).
- [ ] `GET /productos/{id}` includes computed `agotado` (FR6).
- [ ] Pytest suite covering every acceptance criterion in `spec.md` — see `requirements.md` NFR3 for the pass/fail bar (must match `REFERENCE_PROJECT.md §10` in MMEIA).
- [ ] Tag `v0.2.0`.

## Milestone M3 — Deploy (applies `03_Preparar_Despliegue`)

- [ ] `docker/Dockerfile` for the API service.
- [ ] `docker/docker-compose.yml` — API + PostgreSQL, environment variables for the connection string, no hardcoded secrets.
- [ ] `docker compose up` from a clean checkout reaches a working API with no manual steps (NFR2).
- [ ] Tag `v0.3.0`.

## Milestone M4 — Freeze-ready

- [ ] `docs/architecture.md`, `docs/decisions.md`, `docs/deployment.md` finalized.
- [ ] Full test suite green in CI.
- [ ] Tag `v1.0.0`.
- [ ] Report the `v1.0.0` commit SHA back to MMEIA — this becomes `05_Reference_Projects/01_CRUD/REFERENCE_PROJECT.md`'s `commit_referencia`, and only then can `reference_project_validator.py` (Fase 6.2, built in parallel in MMEIA) verify this repository and the unit be frozen (Fase 6.5).

## Explicitly not a task here

Implementing OpenSpec tooling on top of `spec.md`/`requirements.md`/`tasks.md` (e.g. running the real `openspec` CLI to scaffold `openspec/`) — registered as a possible future milestone in `docs/decisions.md`, not required for `v1.0.0`.
