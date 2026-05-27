from pydantic import BaseModel, EmailStr

class ClienteBase(BaseModel):
    nome:     str
    telefone: str | None = None
    email:    EmailStr | None = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome:     str | None = None
    telefone: str | None = None
    email:    EmailStr | None = None

class ClienteOut(ClienteBase):
    id: int

    model_config = {"from_attributes": True}