# Contrato de la API

Producido siguiendo `04_Playbooks/02_Crear_API/PLAYBOOK.md` (Pasos 1-2). Cada endpoint corresponde a una operación real ya fijada en `spec.md`/`requirements.md` — ninguno especulativo.

**Desviación deliberada del Playbook, documentada (no silenciosa):** el Playbook incluye autenticación JWT (Paso 5) como parte de su resultado esperado. Este proyecto la omite a propósito: `spec.md` ya excluye autenticación explícitamente, y `05_Reference_Projects/PLAN_DE_DESARROLLO.md §1` reserva la seguridad para el segundo Reference Project del catálogo ("API — con seguridad"), no para CRUD. Aplicarla aquí duplicaría esa demostración futura. Se aplican los Pasos 1-4 y 6 completos; el Paso 5 se omite y la tabla de verificación del Paso 6 se adapta quitando la columna "sin token".

## Tabla de endpoints (Paso 1)

| Endpoint | Operación real |
|---|---|
| `POST /categorias` | alta de categoría |
| `GET /categorias` | listado |
| `DELETE /categorias/{id}` | baja — regla FR3: rechazada si tiene productos asociados |
| `POST /productos` | alta de producto |
| `GET /productos` | listado, paginado y con filtros — regla FR2 |
| `GET /productos/{id}` | detalle, incluye `stock` y `agotado` derivado — regla FR6 |
| `PATCH /productos/{id}` | edición de `nombre`/`descripcion`/`precio`/`categoria_id` — regla FR1 |
| `POST /productos/{id}/transicion` | cambio de `estado` por la máquina de estados — regla FR5 |
| `PATCH /productos/{id}/stock` | ajuste de `cantidad` por `delta` — regla FR4 |

## Contratos (Paso 2)

### `POST /categorias`
Request: `{"nombre": str, "descripcion": str | null}` → **201** `{"id","nombre","descripcion"}` | **422** (nombre vacío o duplicado)

### `GET /categorias`
→ **200** `[{"id","nombre","descripcion"}, ...]`

### `DELETE /categorias/{id}`
→ **204** | **404** (no existe) | **409** (tiene productos asociados — FR3)

### `POST /productos`
Request: `{"nombre": str, "descripcion": str|null, "precio": decimal, "categoria_id": uuid}` → **201** `{"id","nombre","descripcion","precio","categoria_id","estado":"borrador"}` | **422** (precio<=0, nombre vacío) | **404** (categoria_id inexistente)

### `GET /productos`
Query: `page`, `page_size`, `categoria_id?`, `estado?` → **200** `{"items":[...],"total","page","page_size"}` | **422** (estado fuera de enum)

### `GET /productos/{id}`
→ **200** `{"id",...,"stock":{"cantidad"},"agotado": bool}` | **404**

### `PATCH /productos/{id}`
Request: campos parciales de `nombre`/`descripcion`/`precio`/`categoria_id` → **200** | **404** | **422** (valor inválido) | **404** (categoria_id nuevo inexistente)

### `POST /productos/{id}/transicion`
Request: `{"estado_destino": str}` → **200** `{"estado": nuevo}` | **404** (producto no existe) | **409** (transición inválida — FR5)

### `PATCH /productos/{id}/stock`
Request: `{"delta": int}` → **200** `{"cantidad": nueva}` | **404** | **422** (dejaría `cantidad < 0` — FR4)
