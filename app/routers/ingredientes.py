from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ingrediente import Ingrediente
from app.schemas.ingrediente import IngredienteUpdate, IngredienteCreate, IngredienteOut
from app.auth.dependencies import require_role
from typing import List


router = APIRouter(
    prefix="/ingredientes",
    tags=["Ingredientes"]
)

@router.get("/", response_model=List[IngredienteOut])
def listar(db: Session = Depends(get_db), 
           _= Depends(require_role("admin", "estoquista"))):
    
    return db.query(Ingrediente).all()


@router.get("/{id}", response_model=IngredienteOut)
def buscar (id: int, db: Session = Depends(get_db),
            _= Depends(require_role("admin", "estoquista"))):
    
    item = db.query(Ingrediente).filter(Ingrediente.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    return item


@router.post("/", response_model=IngredienteOut, status_code=status.HTTP_201_CREATED)
def criar(dados: IngredienteCreate, db: Session = Depends(get_db),
          _=Depends(require_role("admin", "estoquista"))):
    item = Ingrediente(**dados.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.patch("/{id}", response_model=IngredienteOut)
def atualizar(id: int, dados: IngredienteUpdate, db: Session = Depends(get_db), 
              _=Depends(require_role("admin", "estoquista"))):
    item = db.query(Ingrediente).filter(Ingrediente.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(item, campo, valor)
    
    db.commit()
    db.refresh(item)

    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(id: int, db: Session = Depends(get_db),
            _=Depends(require_role("admin"))):
    item = db.query(Ingrediente).filter(Ingrediente.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    
    db.delete(item)
    db.commit()