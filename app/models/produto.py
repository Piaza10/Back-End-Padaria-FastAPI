from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base


produto_ingredientes = Table(
    "produto_ingredientes",
    Base.metadata,

    Column("produto_id", ForeignKey("produtos.id"), primary_key=True),
    Column("ingrediente_id", ForeignKey("ingredientes.id"), primary_key=True),
    Column("quantidade", Float, nullable=False)
)

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    preco = Column(Float, nullable=False)

    ingrediente = relationship("Ingrediente",
                               secondary=produto_ingredientes, 
                               backref="produtos")