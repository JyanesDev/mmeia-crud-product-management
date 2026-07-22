# Requirements

## Functional

- **FR1** — Create, read, update and soft-delete (via `estado`) a Producto.
- **FR2** — List Productos with pagination and optional filters by `categoria_id` and `estado`.
- **FR3** — Create, read, update and delete a Categoria. A Categoria cannot be deleted while any Producto references it.
- **FR4** — Read and adjust the Stock of a Producto (increment/decrement, never a direct absolute overwrite — see `docs/decisions.md`, ADR-002 equivalent reasoning applied to stock mutation).
- **FR5** — Transition a Producto's `estado` only along valid paths: `borrador` → `activo` → `descatalogado`. Any other transition is rejected with a 4xx error naming the invalid transition.
- **FR6** — Derive "agotado" as a read-only computed property (`estado == activo AND stock.cantidad == 0`), never stored.

## Non-functional

- **NFR1** — Every rejected request (validation error, invalid state transition, negative stock) returns a machine-readable error code, not just a message — needed for automated tests to assert on failure *reason*, not just failure.
- **NFR2** — The API must be runnable locally via a single `docker compose up` with no manual setup beyond providing environment variables.
- **NFR3** — Test suite must cover, at minimum, every case listed in `REFERENCE_PROJECT.md §10` (Testing y validación) in the MMEIA repository — that list is the contract this project is graded against.

## Explicitly out of scope

Authentication, authorization, multi-tenancy, shopping cart, payments — see `spec.md` and MMEIA's `REFERENCE_PROJECT.md §4` for why (this project demonstrates CRUD, not SaaS or API-with-security, which are separate Reference Projects in MMEIA's catalog).

## Traceability

Every requirement here must be traceable to a section of `spec.md` before implementation starts (`tasks.md` bridges the two).
