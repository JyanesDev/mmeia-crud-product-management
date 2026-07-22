# Architecture

```text
Client --HTTP--> API (FastAPI) --SQL--> PostgreSQL
```

One API service, one relational database. No message queue, no cache, no second service — the project's scope (`spec.md`, `requirements.md`) doesn't justify any of them. This is the same "representative, not maximal" principle as MMEIA's `REFERENCE_PROJECT.md §5`.

## Layering inside the API

```text
routers/      -> HTTP concerns only (parsing, status codes)
services/     -> business rules (state machine, stock delta validation)
repositories/ -> persistence (SQLAlchemy), one per aggregate (Producto, Categoria, Stock)
models/       -> SQLAlchemy models
schemas/      -> Pydantic request/response models
```

A router never talks to a repository directly — it goes through a service, so the state-machine and stock-delta rules (the actual point of this project) live in exactly one place, not scattered across endpoints.

## What this deliberately does not include

- No auth middleware, no API gateway, no service mesh — out of scope (see `spec.md`).
- No caching layer — the data volume of a CRUD pilot never justifies one; adding it here would be exactly the kind of unjustified complexity `REFERENCE_PROJECT.md §1` warns against.
