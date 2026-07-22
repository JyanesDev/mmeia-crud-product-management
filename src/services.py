import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models import Producto, TRANSICIONES_VALIDAS, ESTADOS_VALIDOS
from src.repositories import CategoriaRepository, ProductoRepository, StockRepository


class CategoriaService:
    def __init__(self, db: Session):
        self.repo = CategoriaRepository(db)

    def crear(self, nombre: str, descripcion: str | None):
        return self.repo.crear(nombre, descripcion)

    def listar(self):
        return self.repo.listar()

    def eliminar(self, categoria_id: uuid.UUID) -> None:
        categoria = self.repo.obtener(categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        asociados = self.repo.contar_productos_asociados(categoria_id)
        if asociados > 0:
            raise HTTPException(
                status_code=409,
                detail=f"No se puede eliminar: {asociados} producto(s) referencian esta categoria",
            )
        self.repo.eliminar(categoria)


class ProductoService:
    MAX_PAGE_SIZE = 100

    def __init__(self, db: Session):
        self.db = db
        self.productos = ProductoRepository(db)
        self.stocks = StockRepository(db)
        self.categorias = CategoriaRepository(db)

    def crear(self, nombre: str, descripcion: str | None, precio, categoria_id: uuid.UUID) -> Producto:
        if self.categorias.obtener(categoria_id) is None:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        return self.productos.crear(
            nombre=nombre, descripcion=descripcion, precio=precio, categoria_id=categoria_id
        )

    def obtener_o_404(self, producto_id: uuid.UUID) -> Producto:
        producto = self.productos.obtener(producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto

    def listar(self, page: int, page_size: int, categoria_id: uuid.UUID | None, estado: str | None):
        if estado is not None and estado not in ESTADOS_VALIDOS:
            raise HTTPException(status_code=422, detail=f"estado invalido: {estado}")
        page_size = min(page_size, self.MAX_PAGE_SIZE)
        items, total = self.productos.listar(page, page_size, categoria_id, estado)
        return items, total, page, page_size

    def actualizar(self, producto_id: uuid.UUID, cambios: dict) -> Producto:
        producto = self.obtener_o_404(producto_id)
        if "categoria_id" in cambios and cambios["categoria_id"] is not None:
            if self.categorias.obtener(cambios["categoria_id"]) is None:
                raise HTTPException(status_code=404, detail="Categoria no encontrada")
        for campo, valor in cambios.items():
            if valor is not None:
                setattr(producto, campo, valor)
        return self.productos.guardar(producto)

    def transicionar(self, producto_id: uuid.UUID, estado_destino: str) -> Producto:
        producto = self.obtener_o_404(producto_id)
        if estado_destino not in ESTADOS_VALIDOS:
            raise HTTPException(status_code=422, detail=f"estado invalido: {estado_destino}")
        permitidos = TRANSICIONES_VALIDAS.get(producto.estado, set())
        if estado_destino not in permitidos:
            raise HTTPException(
                status_code=409,
                detail=f"Transicion invalida: {producto.estado} -> {estado_destino}",
            )
        producto.estado = estado_destino
        return self.productos.guardar(producto)

    def ajustar_stock(self, producto_id: uuid.UUID, delta: int):
        self.obtener_o_404(producto_id)  # 404 before touching stock
        stock = self.stocks.obtener_por_producto(producto_id)
        nueva_cantidad = stock.cantidad + delta
        if nueva_cantidad < 0:
            raise HTTPException(
                status_code=422,
                detail=f"delta dejaria cantidad negativa ({nueva_cantidad})",
            )
        stock.cantidad = nueva_cantidad
        return self.stocks.guardar(stock)
