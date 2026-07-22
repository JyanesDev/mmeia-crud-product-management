from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import CategoriaCreate, CategoriaOut
from src.services import CategoriaService

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.post("", response_model=CategoriaOut, status_code=201)
def crear_categoria(payload: CategoriaCreate, db: Session = Depends(get_db)):
    return CategoriaService(db).crear(payload.nombre, payload.descripcion)


@router.get("", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return CategoriaService(db).listar()


@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: str, db: Session = Depends(get_db)):
    CategoriaService(db).eliminar(categoria_id)
