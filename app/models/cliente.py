from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id       = Column(Integer, primary_key=True, index=True)
    nome     = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    email    = Column(String, unique=True, nullable=True)

    pedidos  = relationship("Pedido", back_populates="cliente")