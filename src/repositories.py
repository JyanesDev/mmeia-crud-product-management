import uuid

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models import Categoria, Producto, Stock


class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, nombre: str, descripcion: str | None) -> Categoria:
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        self.db.add(categoria)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=422, detail=f"nombre de categoria duplicado: {nombre}")
        self.db.refresh(categoria)
        return categoria

    def listar(self) -> list[Categoria]:
        return self.db.query(Categoria).order_by(Categoria.nombre).all()

    def obtener(self, categoria_id: uuid.UUID) -> Categoria | None:
        return self.db.get(Categoria, categoria_id)

    def contar_productos_asociados(self, categoria_id: uuid.UUID) -> int:
        return (
            self.db.query(func.count(Producto.id))
            .filter(Producto.categoria_id == categoria_id)
            .scalar()
        )

    def eliminar(self, categoria: Categoria) -> None:
        self.db.delete(categoria)
        self.db.commit()


class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, **kwargs) -> Producto:
        producto = Producto(**kwargs)
        self.db.add(producto)
        self.db.flush()  # need producto.id before creating its Stock row
        stock = Stock(producto_id=producto.id, cantidad=0)
        self.db.add(stock)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener(self, producto_id: uuid.UUID) -> Producto | None:
        return self.db.get(Producto, producto_id)

    def listar(
        self,
        page: int,
        page_size: int,
        categoria_id: uuid.UUID | None,
        estado: str | None,
    ) -> tuple[list[Producto], int]:
        query = self.db.query(Producto)
        if categoria_id is not None:
            query = query.filter(Producto.categoria_id == categoria_id)
        if estado is not None:
            query = query.filter(Producto.estado == estado)
        total = query.count()
        items = query.order_by(Producto.nombre).offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def guardar(self, producto: Producto) -> Producto:
        self.db.commit()
        self.db.refresh(producto)
        return producto


class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_producto(self, producto_id: uuid.UUID) -> Stock | None:
        return self.db.query(Stock).filter(Stock.producto_id == producto_id).first()

    def guardar(self, stock: Stock) -> Stock:
        self.db.commit()
        self.db.refresh(stock)
        return stock
