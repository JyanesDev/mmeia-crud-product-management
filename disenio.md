# Diseño de datos

Producido siguiendo `04_Playbooks/01_Disenar_Base_Datos/PLAYBOOK.md` (Pasos 1-4) de MMEIA. Entidades y reglas ya fijadas en `spec.md`/`requirements.md` y en las decisiones de `docs/decisions.md` (ADR-001/002/003).

## Categoria
- id — identificador único
- nombre — regla: cada categoría se identifica de forma única por su nombre (necesario para que un filtro por categoría en `GET /productos` sea inequívoco)
- descripcion — regla: contexto opcional, sin restricción de negocio

## Producto
- id — identificador único
- nombre — regla: "todo producto debe tener un nombre" (`spec.md` FR1: requerido, no vacío)
- descripcion — regla: opcional (`spec.md` FR1)
- precio — regla: "el precio debe ser positivo" (`spec.md` FR1: `precio > 0`)
- categoria_id — regla: "todo producto pertenece a una categoría existente" (`spec.md` FR1: `categoria_id` debe existir)
- estado — regla: "el producto sigue un ciclo de vida `borrador → activo → descatalogado`, sin saltos ni retrocesos" (ADR-002, `spec.md` FR5)

## Stock
- id — identificador único
- producto_id — regla: "cada producto tiene exactamente un registro de stock" (ADR-001: tabla propia, relación 1:1, nunca columna de Producto)
- cantidad — regla: "la cantidad nunca puede ser negativa" (`spec.md` FR4: un `delta` que la dejaría negativa se rechaza sin aplicar ningún cambio parcial)

---

## Tipos de dato y clave primaria (Paso 2)

- **Categoria:** id (UUID, PK), nombre (TEXT), descripcion (TEXT)
- **Producto:** id (UUID, PK), nombre (TEXT), descripcion (TEXT), precio (NUMERIC(10,2)), categoria_id (UUID), estado (TEXT)
- **Stock:** id (UUID, PK), producto_id (UUID), cantidad (INTEGER)

Ningún importe en coma flotante (`precio` usa `NUMERIC`, no `FLOAT`/`DOUBLE`) — mismo criterio que el propio Playbook exige en su Paso 2.

## Relaciones y claves foráneas (Paso 3)

- `Producto.categoria_id → FK Categoria.id` (1:N — una Categoria tiene muchos Productos)
- `Stock.producto_id → FK Producto.id` (1:1 — forzado con `UNIQUE` sobre `producto_id`, coherente con ADR-001: Stock es una tabla propia pero nunca comparte un Producto entre dos filas de Stock)

Sin relaciones N:M en este dominio (alcance deliberadamente pequeño, `spec.md` "Explícitamente out of scope").

## Restricciones desde las reglas de negocio (Paso 4)

- `Categoria.nombre` → `UNIQUE`
- `Producto.nombre` → `NOT NULL`
- `Producto.precio` → `NOT NULL, CHECK (precio > 0)`
- `Producto.categoria_id` → `NOT NULL, REFERENCES Categoria(id) ON DELETE RESTRICT` (`requirements.md` FR3: una Categoria con productos asociados no puede eliminarse — `RESTRICT` lo hace cumplir en el propio esquema, no solo en la aplicación)
- `Producto.estado` → `NOT NULL, CHECK (estado IN ('borrador','activo','descatalogado')), DEFAULT 'borrador'` (ADR-002; el `CHECK` es la máquina de estados a nivel de valores válidos — la restricción de *transición* entre estados, al depender del valor anterior, se aplica en la capa de servicio de la API, no en el esquema)
- `Stock.producto_id` → `NOT NULL, UNIQUE, REFERENCES Producto(id) ON DELETE CASCADE` (si un Producto se elimina, su Stock deja de tener sentido — pero nótese que `spec.md` FR1 nunca elimina un Producto realmente, solo lo transiciona a `descatalogado`; este `ON DELETE` es una garantía de integridad para el caso excepcional, no el camino habitual)
- `Stock.cantidad` → `NOT NULL, CHECK (cantidad >= 0), DEFAULT 0`

Ninguna restricción aquí carece de una regla de negocio que la exija (criterio de finalización del Paso 4 del Playbook).
