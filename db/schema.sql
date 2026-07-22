-- Generated per 04_Playbooks/01_Disenar_Base_Datos/PLAYBOOK.md (Paso 5), from disenio.md.
-- Order: Categoria (no dependencies) -> Producto (references Categoria) -> Stock (references Producto).

CREATE TABLE Categoria (
    id UUID PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE Producto (
    id UUID PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10,2) NOT NULL CHECK (precio > 0),
    categoria_id UUID NOT NULL REFERENCES Categoria(id) ON DELETE RESTRICT,
    estado TEXT NOT NULL DEFAULT 'borrador'
        CHECK (estado IN ('borrador', 'activo', 'descatalogado'))
);

CREATE TABLE Stock (
    id UUID PRIMARY KEY,
    producto_id UUID NOT NULL UNIQUE REFERENCES Producto(id) ON DELETE CASCADE,
    cantidad INTEGER NOT NULL DEFAULT 0 CHECK (cantidad >= 0)
);
