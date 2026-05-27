from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    caixa = "caixa"
    estoquista = "estoquista"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.caixa)