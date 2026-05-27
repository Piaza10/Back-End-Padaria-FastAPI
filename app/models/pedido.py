from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class StatusPedido(str, enum.Enum):
    aberto     = "aberto"
    finalizado = "finalizado"
    cancelado  = "cancelado"

pedido_produtos = Table(
    "pedido_produtos",
    Base.metadata,
    Column("pedido_id",   ForeignKey("pedidos.id"),   primary_key=True),
    Column("produto_id",  ForeignKey("produtos.id"),  primary_key=True),
    Column("quantidade",  Integer, nullable=False),
)

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.aberto, nullable=False)
    total = Column(Float, nullable=False, default=0.0)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    cliente = relationship("Cliente", back_populates="pedidos")
    produtos = relationship("Produto", secondary=pedido_produtos, backref="pedidos")