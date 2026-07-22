# Spec

Written before any code, per SDD (see `README.md`). Each feature below is what MMEIA's `08_Implementacion.md` Paso 2 calls a spec: entradas, comportamiento, criterio de aceptación, casos borde. Traced to `requirements.md`.

## Feature: Crear Producto (FR1)

**Entradas:** `nombre` (string, requerido, no vacío), `descripcion` (string, opcional), `precio` (decimal, > 0), `categoria_id` (UUID, debe existir).

**Comportamiento:** crea un Producto en estado `borrador`. Crea automáticamente su fila `Stock` asociada con `cantidad = 0`.

**Criterio de aceptación:**
- Dado un `categoria_id` inexistente → 404, nunca crea el producto.
- Dado un `precio <= 0` → 422.
- Dado un `nombre` vacío o solo espacios → 422.
- Éxito → 201, devuelve el Producto con `estado: "borrador"` y su Stock en `cantidad: 0`.

## Feature: Transición de estado (FR5)

**Entradas:** `producto_id`, `estado_destino`.

**Comportamiento:** valida la transición contra la máquina de estados (`borrador → activo → descatalogado`, sin saltos, sin retroceso) antes de aplicarla.

**Criterio de aceptación:**
- `borrador → activo`: éxito.
- `activo → descatalogado`: éxito.
- `borrador → descatalogado` (salto): rechazado, 409, código de error `INVALID_TRANSITION`.
- `descatalogado → activo` (retroceso): rechazado, 409, mismo código.
- Transición a un estado igual al actual: rechazada, 409 (no es una transición).

## Feature: Ajustar Stock (FR4)

**Entradas:** `producto_id`, `delta` (entero, puede ser negativo).

**Comportamiento:** aplica `cantidad = cantidad + delta`. Nunca acepta un valor absoluto directo (evita condiciones de carrera entre dos ajustes concurrentes — ver `docs/decisions.md`).

**Criterio de aceptación:**
- Un `delta` que dejaría `cantidad < 0` → rechazado, 422, sin aplicar ningún cambio parcial.
- Un `delta` válido → 200, devuelve la nueva `cantidad`.

## Feature: Consultar "agotado" (FR6)

**Entradas:** `producto_id`.

**Comportamiento:** devuelve `agotado: true` únicamente si `estado == "activo"` AND `stock.cantidad == 0`. Un producto en `borrador` o `descatalogado` con `cantidad == 0` nunca se reporta como `agotado` — ese campo solo tiene sentido para algo que se está intentando vender activamente.

**Criterio de aceptación:**
- `activo` + `cantidad: 0` → `agotado: true`.
- `activo` + `cantidad: 5` → `agotado: false`.
- `borrador` + `cantidad: 0` → `agotado: false` (no aplica, no está a la venta).

## Feature: Listar Productos con paginación y filtros (FR2)

**Entradas:** `page` (entero, default 1), `page_size` (entero, default 20, máx. 100), `categoria_id` (opcional), `estado` (opcional).

**Criterio de aceptación:**
- Más elementos que `page_size` → respuesta incluye metadatos de paginación (`total`, `page`, `page_size`) y solo la página pedida.
- `page_size > 100` → se limita a 100, nunca error.
- Filtro por `estado` inválido (fuera del enum) → 422.

## Feature: Eliminar Categoria con Productos asociados (FR3)

**Criterio de aceptación:**
- Categoria sin productos asociados → 204, elimina.
- Categoria con al menos un producto asociado → 409, no elimina, mensaje explica cuántos productos la referencian.
