from pydantic import BaseModel, Field
from datetime import datetime
from app.models.pedido import StatusPedido

class ProdutoPedido(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)

class PedidoCreate(BaseModel):
    cliente_id:  int
    produtos:    list[ProdutoPedido]

class PedidoUpdate(BaseModel):
    status:   StatusPedido        | None = None
    produtos: list[ProdutoPedido] | None = None

class ProdutoNoPedidoOut(BaseModel):
    id:         int
    nome:       str
    preco:      float
    quantidade: int

    model_config = {"from_attributes": True}

class PedidoOut(BaseModel):
    id:        int
    cliente_id: int
    status:    StatusPedido
    total:     float
    criado_em: datetime
    produtos:  list[ProdutoNoPedidoOut] = []

    model_config = {"from_attributes": True}