import uuid
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# --- Categoria ---

class CategoriaCreate(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: Optional[str] = None


class CategoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    nombre: str
    descripcion: Optional[str]


# --- Producto ---

class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: Optional[str] = None
    precio: Decimal = Field(gt=0)
    categoria_id: uuid.UUID


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1)
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = Field(default=None, gt=0)
    categoria_id: Optional[uuid.UUID] = None


class StockOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cantidad: int


class ProductoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    categoria_id: uuid.UUID
    estado: str


class ProductoDetailOut(ProductoOut):
    stock: StockOut
    agotado: bool


class ProductoListOut(BaseModel):
    items: list[ProductoOut]
    total: int
    page: int
    page_size: int


class TransicionRequest(BaseModel):
    estado_destino: str


class TransicionOut(BaseModel):
    estado: str


class StockAdjustRequest(BaseModel):
    delta: int


class StockAdjustOut(BaseModel):
    cantidad: int
