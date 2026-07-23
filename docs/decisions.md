# Decisions (ADR log)

Full version of the three decisions summarized in MMEIA's `REFERENCE_PROJECT.md §6`. MMEIA's copy is the pedagogical distillation for comparison; this is the project's own working decision log, expanded with implementation-level detail MMEIA's documentation deliberately leaves out (`ADR-002`/`ADR-007`: code and its full rationale live here, not in MMEIA).

## ADR-001 — Stock as its own table, not a column on Producto

**Status:** Accepted.

**Context:** a Producto needs to expose a current stock quantity.

**Alternatives:**
- (a) `Producto.stock_cantidad` column.
- (b) A separate `Stock` table, 1:1 with `Producto`.

**Decision:** (b).

**Rationale:** stock changes on every sale/restock; product identity data (name, price, category) changes rarely. Coupling both in one row/table means every stock-only update touches the Producto row too, and forecloses adding stock-movement history later without a schema migration that moves data, not just adds a column.

**Consequences:** one extra join for any query that needs both product and stock data together — accepted, since reads of the combined view are the common case and a single indexed join is cheap.

## ADR-002 — Estado as an explicit state machine, not a boolean

**Status:** Accepted.

**Context:** a Producto needs a lifecycle: not yet published, published, retired.

**Alternatives:**
- (a) `activo: boolean`.
- (b) `estado: enum(borrador, activo, descatalogado)` with application-level transition validation.

**Decision:** (b).

**Rationale:** a boolean cannot represent "not yet published" distinctly from "retired", and cannot prevent an invalid transition (retired → active without going back through draft) — both are real rules this project needs to enforce, not leave to the caller's discipline.

**Consequences:** every state change goes through a dedicated endpoint (`POST /productos/{id}/transicion`) instead of a generic `PATCH`, so the transition table has exactly one enforcement point.

## ADR-003 — "Agotado" is a derived query, never a stored state

**Status:** Accepted.

**Context:** clients need to know if a product is out of stock.

**Alternatives:**
- (a) A fourth `estado` value, `agotado`.
- (b) Compute it at read time from `estado == activo AND stock.cantidad == 0`.

**Decision:** (b).

**Rationale:** (a) creates two sources of truth (`estado` and `Stock.cantidad`) that could disagree — a product marked `agotado` whose stock got restocked without anyone updating `estado`. Deriving it removes that failure mode by construction.

## ADR-004 — `psycopg[binary]` (psycopg3) instead of `psycopg2-binary`

**Status:** Accepted.

**Context:** `pip install psycopg2-binary` failed at build time (`pg_config not found`) — no precompiled wheel exists yet for Python 3.14, which is very new.

**Alternatives:**
- (a) Install PostgreSQL's build toolchain locally just to compile `psycopg2-binary` from source.
- (b) Switch to `psycopg[binary]` (psycopg3), which does publish wheels for new Python versions.

**Decision:** (b).

**Rationale:** installing a full compiler toolchain for a single dependency, in a project that needs it for nothing else, is accidental complexity that a real alternative avoids. psycopg3 is the actively maintained evolution of the same driver family, with first-class SQLAlchemy 2.0 support.

**Consequences:** the SQLAlchemy connection string uses the `postgresql+psycopg://` dialect prefix, not the bare `postgresql://` most psycopg2 tutorials show — a detail that matters if this project's driver choice is ever revisited.

**Follow-through in M3:** `docker/Dockerfile` deliberately targets `python:3.12-slim`, not 3.14 — this incident is exactly why: 3.12 is stable and has broad wheel support for this project's dependencies, avoiding a repeat of the same problem inside the deployed container.

## ADR-005 — Skipping the JWT step of `02_Crear_API/PLAYBOOK.md`

**Status:** Accepted.

**Context:** the Playbook this project composes with for its API includes a JWT authentication step (Paso 5) as part of its own definition of "API funcional y protegida".

**Alternatives:**
- (a) Apply Paso 5 literally, adding a minimal JWT middleware to all 9 endpoints.
- (b) Skip it, documented.

**Decision:** (b).

**Rationale:** this project's own `spec.md` already excludes authentication before M2 started, and MMEIA's `05_Reference_Projects/PLAN_DE_DESARROLLO.md §1` reserves security specifically for the *second* Reference Project of its catalog ("API — con seguridad"). Adding JWT here would be scope creep relative to this project's own spec, and would prematurely duplicate a demonstration better made elsewhere with more context.

**Consequences:** the API has no auth of any kind — anyone who can reach the port can call every endpoint. Correct for this project's declared scope; would be a real defect in any project whose spec doesn't explicitly exclude auth.

## Open decision — OpenSpec adoption

Not yet decided: whether to migrate `spec.md`/`requirements.md`/`tasks.md` into a real OpenSpec-managed structure (via the actual `openspec` CLI) once this project has more than one contributor. Registered as a candidate for a milestone after `v1.0.0`, not a blocker for the pilot.
