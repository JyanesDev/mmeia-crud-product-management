# API verification (Playbook Paso 6, tabla adaptada)

Ejecutado de verdad, no simulado: 28 tests de `pytest` contra un contenedor PostgreSQL 16 real y desechable (`docker run --rm`), más una comprobación adicional de arranque real del servidor (`uvicorn`) con peticiones `curl` reales. Sin JWT (ver `api/contrato.md` — desviación deliberada y documentada del Paso 5).

## Tabla de verificación adaptada (sin columna "sin token")

| Endpoint | Válido | Body/valor inválido | Inexistente |
|---|---|---|---|
| `POST /categorias` | 201 ✅ | 422 (nombre duplicado) ✅ | — |
| `GET /categorias` | 200 ✅ | — | — |
| `DELETE /categorias/{id}` | 204 ✅ | 409 (con productos, FR3) ✅ | 404 ✅ |
| `POST /productos` | 201 ✅ | 422 (precio≤0, nombre vacío) ✅ | 404 (categoria_id) ✅ |
| `GET /productos` | 200 ✅ | 422 (estado inválido) ✅ | — |
| `GET /productos/{id}` | 200 ✅ | — | 404 ✅ |
| `PATCH /productos/{id}` | 200 ✅ | — | 404 ✅ |
| `POST /productos/{id}/transicion` | 200 ✅ | 409 (salto y retroceso) ✅ | 404 ✅ |
| `PATCH /productos/{id}/stock` | 200 ✅ | 422 (cantidad negativa) ✅ | 404 ✅ |

Adicional (regla derivada, ADR-003/FR6): `agotado` verificado en sus 3 combinaciones reales (activo+0 → true, activo+stock → false, borrador+0 → false).

## Resultado real de la ejecución

```
28 passed, 1 warning in 1.78s
```

## Smoke test de arranque real (servidor vivo, no TestClient)

```
$ uvicorn src.main:app --port 8123
$ curl -X POST /categorias {"nombre":"Electronica",...}
201 {"id":"a065b6e5-...","nombre":"Electronica",...}
$ curl -X POST /productos {"nombre":"Teclado mecanico","precio":49.90,...}
201 {"id":"af56013a-...","estado":"borrador",...}
```

Playbook Checklist final (adaptado, 4/5 aplicables — la casilla de JWT no aplica, ver `api/contrato.md`): satisfecho.

**Date:** 2026-07-22. **Stack:** FastAPI 0.139.2, SQLAlchemy 2.0.51, PostgreSQL 16.
