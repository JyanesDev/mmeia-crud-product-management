# mmeia-crud-product-management

Reference implementation for **`01_CRUD`**, the pilot Reference Project of [MMEIA](https://github.com/JyanesDev/MMEIA-METHODOLOGY-V2) (`05_Reference_Projects`).

This repository is the external, real, runnable counterpart to `05_Reference_Projects/01_CRUD/REFERENCE_PROJECT.md` in the MMEIA repository. MMEIA's own documentation never embeds the full code of a Reference Project (`ADR-002`/`ADR-007`) — it explains the decisions; this repository *is* the decisions applied.

**If you found this repo through MMEIA:** don't copy this project — compare it against your own. See the "Guía de comparación" section of `REFERENCE_PROJECT.md` in the MMEIA repository for the questions this project is meant to provoke, not answer for you.

## What this is

A small product-management CRUD: products, categories, stock, and an explicit product lifecycle (`borrador` → `activo` → `descatalogado`). Deliberately small — see `spec.md` for exactly what it does and does not cover.

## Stack

- **API:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Tests:** Pytest
- **Deploy:** Docker Compose
- **CI:** GitHub Actions

Boring, mainstream choices on purpose — the point of this project is the decisions in `docs/decisions.md`, not the tech stack.

## Repository layout

```text
.
├── spec.md              # what each feature must do, before any code (SDD — see below)
├── requirements.md       # functional/non-functional requirements this project satisfies
├── tasks.md              # implementation plan, derived from spec.md, milestones checked off as completed
├── disenio.md            # entity/attribute/constraint design (01_Disenar_Base_Datos, Pasos 1-4)
├── despliegue.md         # configuration/secrets inventory (03_Preparar_Despliegue, Paso 1)
├── docs/
│   ├── architecture.md  # high-level architecture diagram and rationale
│   ├── decisions.md     # this project's own ADRs (full version — MMEIA's copy is a summary)
│   └── deployment.md    # how this project is deployed, with real verification evidence
├── db/
│   ├── schema.sql        # executable DDL (01_Disenar_Base_Datos, Paso 5)
│   └── VERIFICATION.md   # real constraint-test evidence against a live PostgreSQL
├── api/
│   ├── contrato.md       # endpoint contracts (02_Crear_API, Pasos 1-2)
│   └── VERIFICATION.md   # real end-to-end test evidence
├── src/                  # application code (FastAPI + SQLAlchemy + Pydantic)
├── tests/                # 28 pytest tests
├── docker/               # Dockerfile + docker-compose.yml
├── .env.example           # variable template (03_Preparar_Despliegue, Paso 4)
└── .github/workflows/    # CI pipeline (build → test → deploy)
```

## Spec-Driven Development note

This project is built following **SDD** (see [`SDD.md`](https://github.com/JyanesDev/MMEIA-METHODOLOGY-V2/blob/main/03_Knowledge_Base/11_Inteligencia_Artificial/SDD.md) in MMEIA): `spec.md`/`requirements.md`/`tasks.md` exist and are reviewed *before* any code is written or generated. Whether these files are later migrated into a real [OpenSpec](https://github.com/JyanesDev/MMEIA-METHODOLOGY-V2/blob/main/03_Knowledge_Base/11_Inteligencia_Artificial/OpenSpec.md) scaffold (via the actual `openspec` CLI, not hand-copied) is an open decision for a later milestone — see `docs/decisions.md`.

## Milestones

See `tasks.md` for the full breakdown. Tagged releases: `v0.1.0` (schema), `v0.2.0` (API), `v0.3.0` (deploy), `v1.0.0` (stable — this is the tag MMEIA's `commit_referencia` will point to).

## License

TBD — decide before making the repository public.
