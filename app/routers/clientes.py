from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.auth.dependencies import require_role

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=List[ClienteOut])
def listar(db: Session = Depends(get_db),
           _=Depends(require_role("admin", "caixa"))):
    return db.query(Cliente).all()


@router.get("/{id}", response_model=ClienteOut)
def buscar(id: int, db: Session = Depends(get_db),
           _=Depends(require_role("admin", "caixa"))):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.post("/", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def criar(dados: ClienteCreate, db: Session = Depends(get_db),
          _=Depends(require_role("admin", "caixa"))):
    existente = db.query(Cliente).filter(Cliente.email == dados.email).first()
    if dados.email and existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    cliente = Cliente(**dados.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.patch("/{id}", response_model=ClienteOut)
def atualizar(id: int, dados: ClienteUpdate, db: Session = Depends(get_db),
              _=Depends(require_role("admin", "caixa"))):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(id: int, db: Session = Depends(get_db),
            _=Depends(require_role("admin"))):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()