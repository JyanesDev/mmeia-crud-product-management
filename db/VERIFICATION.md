# Schema verification (Playbook Paso 6)

Executed against a real, disposable `postgres:16` container (`docker run --rm`), not simulated. Container destroyed immediately after.

## 1. Apply schema.sql

```
CREATE TABLE
CREATE TABLE
CREATE TABLE
```

3 tables created without errors, in dependency order (Categoria → Producto → Stock).

## 2. Constraint tests (each expected to fail)

| # | Test | Real result |
|---|---|---|
| 1 | `Categoria.nombre` duplicado | `ERROR: duplicate key value violates unique constraint "categoria_nombre_key"` |
| 2 | `Producto.categoria_id` inexistente | `ERROR: ... violates foreign key constraint "producto_categoria_id_fkey"` |
| 3 | `Producto.estado` fuera del enum (`'archivado'`) | `ERROR: ... violates check constraint "producto_estado_check"` |
| 4 | `Stock.cantidad` negativa | `ERROR: ... violates check constraint "stock_cantidad_check"` |
| 5 | `DELETE` de una `Categoria` referenciada por un `Producto` (`requirements.md` FR3) | `ERROR: ... violates foreign key constraint "producto_categoria_id_fkey" on table "producto"` |

All 5 failed exactly as `disenio.md` required — none passed silently, none failed for the wrong reason. Playbook Checklist final, casilla 7 ("Las pruebas de restricción fallan exactamente como se describe"): satisfied.

**Date:** 2026-07-22. **Engine:** PostgreSQL 16 (official Docker image).
