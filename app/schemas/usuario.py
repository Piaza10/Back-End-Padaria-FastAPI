from pydantic import BaseModel
from app.models.usuario import RoleEnum

class UsuarioCreate(BaseModel):
    nome:  str
    email: str
    senha: str
    role:  RoleEnum = RoleEnum.caixa

class UsuarioOut(BaseModel):
    id:    int
    nome:  str
    email: str
    role:  RoleEnum

    model_config = {"from_attributes": True}