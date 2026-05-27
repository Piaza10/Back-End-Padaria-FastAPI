from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete
from typing import List
from app.database import get_db
from app.models.pedido import Pedido, pedido_produtos, StatusPedido
from app.models.produto import Produto
from app.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoOut
from app.auth.dependencies import require_role


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

def _calcular_total(db: Session, produtos: list) -> float:
    """Soma: preco * quantidade de cada produto do pedido"""
    total = 0.0

    for item in produtos:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if not produto:
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item.produto_id} não encontrado"
            )
        
        total += produto.preco * item.quantidade
        return round(total, 2)

def _sincronizar_produtos(db: Session, pedido: Pedido, produtos: list):
    """Remove os vinculos antigos e insere os novos"""

    db.execute(
        delete(pedido_produtos).where(
            pedido_produtos.c.pedido_id == pedido.id
        )
    )

    for item in produtos:
        db.execute(
            insert(pedido_produtos).values(
                pedido_id = pedido.id,
                produto_id = item.produto_id,
                quantidade = item.quantidade
            )
        )
        

@router.get("/", response_model=List[PedidoOut])
def listar(db: Session = Depends(get_db),
           _=Depends(require_role("admin", "caixa"))):
    return db.query(Pedido).all()


@router.get("/{id}", response_model=PedidoOut)
def buscar(id: int, db: Session = Depends(get_db),
           _=Depends(require_role("admin", "caixa"))):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.post("/", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def criar(dados: PedidoCreate, db: Session = Depends(get_db),
          _=Depends(require_role("admin", "caixa"))):
    total = _calcular_total(db, dados.produtos)
    pedido = Pedido(cliente_id=dados.cliente_id, total=total)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    _sincronizar_produtos(db, pedido, dados.produtos)
    db.commit()
    db.refresh(pedido)
    return pedido


@router.patch("/{id}", response_model=PedidoOut)
def atualizar(id: int, dados: PedidoUpdate, db: Session = Depends(get_db),
              _=Depends(require_role("admin", "caixa"))):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status == StatusPedido.cancelado:
        raise HTTPException(status_code=400, detail="Pedido cancelado não pode ser alterado")

    if dados.status is not None:
        pedido.status = dados.status

    if dados.produtos is not None:
        pedido.total = _calcular_total(db, dados.produtos)
        _sincronizar_produtos(db, pedido, dados.produtos)

    db.commit()
    db.refresh(pedido)
    return pedido


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(id: int, db: Session = Depends(get_db),
            _=Depends(require_role("admin"))):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(pedido)
    db.commit()