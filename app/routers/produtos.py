from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete
from typing import List
from app.database import get_db
from app.models.produto import Produto, produto_ingredientes
from app.models.ingrediente import Ingrediente
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoOut
from app.auth.dependencies import require_role

router = APIRouter(prefix="/produtos", tags=["Produtos"])


def _sincronizar_ingredientes(db: Session, produto: Produto, ingredientes: list):
    """Remove os vínculos antigos e insere os novos com quantidade."""
    db.execute(
        delete(produto_ingredientes).where(
            produto_ingredientes.c.produto_id == produto.id
        )
    )
    for item in ingredientes:
        ingrediente = db.query(Ingrediente).filter(
            Ingrediente.id == item.ingrediente_id
        ).first()
        if not ingrediente:
            raise HTTPException(
                status_code=404,
                detail=f"Ingrediente {item.ingrediente_id} não encontrado"
            )
        db.execute(
            insert(produto_ingredientes).values(
                produto_id=produto.id,
                ingrediente_id=item.ingrediente_id,
                quantidade=item.quantidade
            )
        )


@router.get("/", response_model=List[ProdutoOut])
def listar(db: Session = Depends(get_db),
           _=Depends(require_role("admin", "estoquista", "caixa"))):
    return db.query(Produto).all()


@router.get("/{id}", response_model=ProdutoOut)
def buscar(id: int, db: Session = Depends(get_db),
           _=Depends(require_role("admin", "estoquista", "caixa"))):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.post("/", response_model=ProdutoOut, status_code=status.HTTP_201_CREATED)
def criar(dados: ProdutoCreate, db: Session = Depends(get_db),
          _=Depends(require_role("admin", "estoquista"))):
    produto = Produto(nome=dados.nome, preco=dados.preco)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    if dados.ingredientes:
        _sincronizar_ingredientes(db, produto, dados.ingredientes)
        db.commit()
        db.refresh(produto)
    return produto


@router.patch("/{id}", response_model=ProdutoOut)
def atualizar(id: int, dados: ProdutoUpdate, db: Session = Depends(get_db),
              _=Depends(require_role("admin", "estoquista"))):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if dados.nome  is not None: produto.nome  = dados.nome
    if dados.preco is not None: produto.preco = dados.preco
    if dados.ingredientes is not None:
        _sincronizar_ingredientes(db, produto, dados.ingredientes)
    db.commit()
    db.refresh(produto)
    return produto


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(id: int, db: Session = Depends(get_db),
            _=Depends(require_role("admin"))):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()