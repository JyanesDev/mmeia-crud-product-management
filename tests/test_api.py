"""
End-to-end verification (Playbook Paso 6), adapted: the original table has a
"sin token" column for JWT, which does not apply here (see api/contrato.md
for why this project deliberately omits Paso 5). Every other cell of the
adapted table is covered: valid, invalid body, and nonexistent resource.
"""


def crear_categoria(client, nombre="Electronica"):
    r = client.post("/categorias", json={"nombre": nombre, "descripcion": "cat"})
    assert r.status_code == 201
    return r.json()


def crear_producto(client, categoria_id, nombre="Teclado", precio=49.90):
    r = client.post(
        "/productos",
        json={"nombre": nombre, "descripcion": "d", "precio": precio, "categoria_id": categoria_id},
    )
    assert r.status_code == 201
    return r.json()


# --- Categorias ---

def test_crear_categoria_valida(client):
    body = crear_categoria(client)
    assert body["nombre"] == "Electronica"


def test_crear_categoria_nombre_duplicado(client):
    crear_categoria(client)
    r = client.post("/categorias", json={"nombre": "Electronica"})
    assert r.status_code == 422


def test_listar_categorias(client):
    crear_categoria(client, "A")
    crear_categoria(client, "B")
    r = client.get("/categorias")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_eliminar_categoria_sin_productos(client):
    cat = crear_categoria(client)
    r = client.delete(f"/categorias/{cat['id']}")
    assert r.status_code == 204


def test_eliminar_categoria_con_productos_rechazada(client):
    cat = crear_categoria(client)
    crear_producto(client, cat["id"])
    r = client.delete(f"/categorias/{cat['id']}")
    assert r.status_code == 409


def test_eliminar_categoria_inexistente(client):
    r = client.delete("/categorias/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404


# --- Productos: creacion ---

def test_crear_producto_valido(client):
    cat = crear_categoria(client)
    body = crear_producto(client, cat["id"])
    assert body["estado"] == "borrador"


def test_crear_producto_categoria_inexistente(client):
    r = client.post(
        "/productos",
        json={"nombre": "X", "precio": 10, "categoria_id": "00000000-0000-0000-0000-000000000000"},
    )
    assert r.status_code == 404


def test_crear_producto_precio_invalido(client):
    cat = crear_categoria(client)
    r = client.post("/productos", json={"nombre": "X", "precio": -1, "categoria_id": cat["id"]})
    assert r.status_code == 422


def test_crear_producto_nombre_vacio(client):
    cat = crear_categoria(client)
    r = client.post("/productos", json={"nombre": "", "precio": 10, "categoria_id": cat["id"]})
    assert r.status_code == 422


# --- Productos: lectura, listado, paginacion ---

def test_obtener_producto_incluye_stock_y_no_agotado_en_borrador(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    r = client.get(f"/productos/{prod['id']}")
    assert r.status_code == 200
    body = r.json()
    assert body["stock"]["cantidad"] == 0
    assert body["agotado"] is False  # borrador, no aplica FR6


def test_obtener_producto_inexistente(client):
    r = client.get("/productos/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404


def test_listar_productos_paginacion(client):
    cat = crear_categoria(client)
    for i in range(5):
        crear_producto(client, cat["id"], nombre=f"P{i}")
    r = client.get("/productos", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2


def test_listar_productos_page_size_se_limita_a_100(client):
    cat = crear_categoria(client)
    crear_producto(client, cat["id"])
    r = client.get("/productos", params={"page_size": 500})
    assert r.status_code == 200
    assert r.json()["page_size"] == 100


def test_listar_productos_estado_invalido(client):
    r = client.get("/productos", params={"estado": "no_existe"})
    assert r.status_code == 422


# --- Productos: actualizacion ---

def test_actualizar_producto(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    r = client.patch(f"/productos/{prod['id']}", json={"precio": 99.99})
    assert r.status_code == 200
    assert float(r.json()["precio"]) == 99.99


def test_actualizar_producto_inexistente(client):
    r = client.patch("/productos/00000000-0000-0000-0000-000000000000", json={"precio": 1})
    assert r.status_code == 404


# --- Transicion de estado (FR5) ---

def test_transicion_borrador_a_activo(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    r = client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "activo"})
    assert r.status_code == 200
    assert r.json()["estado"] == "activo"


def test_transicion_activo_a_descatalogado(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "activo"})
    r = client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "descatalogado"})
    assert r.status_code == 200


def test_transicion_salto_borrador_a_descatalogado_rechazada(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    r = client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "descatalogado"})
    assert r.status_code == 409


def test_transicion_retroceso_descatalogado_a_activo_rechazada(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "activo"})
    client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "descatalogado"})
    r = client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "activo"})
    assert r.status_code == 409


def test_transicion_producto_inexistente(client):
    r = client.post(
        "/productos/00000000-0000-0000-0000-000000000000/transicion",
        json={"estado_destino": "activo"},
    )
    assert r.status_code == 404


# --- Stock (FR4) ---

def test_ajustar_stock_incremento(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    r = client.patch(f"/productos/{prod['id']}/stock", json={"delta": 10})
    assert r.status_code == 200
    assert r.json()["cantidad"] == 10


def test_ajustar_stock_decremento_dejaria_negativo_rechazado(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    r = client.patch(f"/productos/{prod['id']}/stock", json={"delta": -1})
    assert r.status_code == 422


def test_ajustar_stock_producto_inexistente(client):
    r = client.patch("/productos/00000000-0000-0000-0000-000000000000/stock", json={"delta": 1})
    assert r.status_code == 404


# --- "agotado" derivado (FR6, ADR-003) ---

def test_agotado_true_solo_si_activo_y_sin_stock(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "activo"})
    r = client.get(f"/productos/{prod['id']}")
    assert r.json()["agotado"] is True  # activo, cantidad 0


def test_agotado_false_si_activo_con_stock(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    client.post(f"/productos/{prod['id']}/transicion", json={"estado_destino": "activo"})
    client.patch(f"/productos/{prod['id']}/stock", json={"delta": 5})
    r = client.get(f"/productos/{prod['id']}")
    assert r.json()["agotado"] is False


def test_agotado_false_si_borrador_sin_stock(client):
    cat = crear_categoria(client)
    prod = crear_producto(client, cat["id"])
    r = client.get(f"/productos/{prod['id']}")
    assert r.json()["agotado"] is False  # borrador, no aplica (ver spec.md FR6)
