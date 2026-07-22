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

## Open decision — OpenSpec adoption

Not yet decided: whether to migrate `spec.md`/`requirements.md`/`tasks.md` into a real OpenSpec-managed structure (via the actual `openspec` CLI) once this project has more than one contributor. Registered as a candidate for a milestone after `v1.0.0`, not a blocker for the pilot.
