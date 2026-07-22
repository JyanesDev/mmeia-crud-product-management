from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import (
    ProductoCreate,
    ProductoUpdate,
    ProductoOut,
    ProductoDetailOut,
    ProductoListOut,
    TransicionRequest,
    TransicionOut,
    StockAdjustRequest,
    StockAdjustOut,
)
from src.services import ProductoService

router = APIRouter(prefix="/productos", tags=["productos"])


@router.post("", response_model=ProductoOut, status_code=201)
def crear_producto(payload: ProductoCreate, db: Session = Depends(get_db)):
    return ProductoService(db).crear(
        nombre=payload.nombre,
        descripcion=payload.descripcion,
        precio=payload.precio,
        categoria_id=payload.categoria_id,
    )


@router.get("", response_model=ProductoListOut)
def listar_productos(
    page: int = 1,
    page_size: int = 20,
    categoria_id: str | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
):
    items, total, page, page_size = ProductoService(db).listar(page, page_size, categoria_id, estado)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/{producto_id}", response_model=ProductoDetailOut)
def obtener_producto(producto_id: str, db: Session = Depends(get_db)):
    producto = ProductoService(db).obtener_o_404(producto_id)
    return {
        **{c: getattr(producto, c) for c in ("id", "nombre", "descripcion", "precio", "categoria_id", "estado")},
        "stock": producto.stock,
        "agotado": producto.agotado,
    }


@router.patch("/{producto_id}", response_model=ProductoOut)
def actualizar_producto(producto_id: str, payload: ProductoUpdate, db: Session = Depends(get_db)):
    cambios = payload.model_dump(exclude_unset=True)
    return ProductoService(db).actualizar(producto_id, cambios)


@router.post("/{producto_id}/transicion", response_model=TransicionOut)
def transicionar_producto(producto_id: str, payload: TransicionRequest, db: Session = Depends(get_db)):
    producto = ProductoService(db).transicionar(producto_id, payload.estado_destino)
    return {"estado": producto.estado}


@router.patch("/{producto_id}/stock", response_model=StockAdjustOut)
def ajustar_stock(producto_id: str, payload: StockAdjustRequest, db: Session = Depends(get_db)):
    stock = ProductoService(db).ajustar_stock(producto_id, payload.delta)
    return {"cantidad": stock.cantidad}
