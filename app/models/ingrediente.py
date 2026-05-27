from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    unidade = Column(String, nullable=False)
    estoque = Column(Float, nullable=False, default=0.0)