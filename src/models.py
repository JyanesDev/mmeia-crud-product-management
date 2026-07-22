import uuid

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base

# db/schema.sql (M1) is the single authoritative DDL - produced by
# 01_Disenar_Base_Datos and verified in db/VERIFICATION.md. These ORM models
# map to those tables; they deliberately do NOT redeclare CHECK/UNIQUE
# constraints already enforced by the real schema, to avoid two sources of
# truth for the same rule (RR1-equivalent reasoning applied to code).

ESTADOS_VALIDOS = ("borrador", "activo", "descatalogado")

TRANSICIONES_VALIDAS = {
    "borrador": {"activo"},
    "activo": {"descatalogado"},
    "descatalogado": set(),
}


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)

    productos = relationship("Producto", back_populates="categoria")


class Producto(Base):
    __tablename__ = "producto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    categoria_id = Column(
        UUID(as_uuid=True), ForeignKey("categoria.id", ondelete="RESTRICT"), nullable=False
    )
    estado = Column(String, nullable=False, default="borrador")

    categoria = relationship("Categoria", back_populates="productos")
    stock = relationship(
        "Stock", back_populates="producto", uselist=False, cascade="all, delete-orphan"
    )

    @property
    def agotado(self) -> bool:
        """Derived, never stored - ADR-003. Only meaningful for a product being actively sold."""
        return self.estado == "activo" and self.stock is not None and self.stock.cantidad == 0


class Stock(Base):
    __tablename__ = "stock"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(
        UUID(as_uuid=True),
        ForeignKey("producto.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    cantidad = Column(Integer, nullable=False, default=0)

    producto = relationship("Producto", back_populates="stock")
