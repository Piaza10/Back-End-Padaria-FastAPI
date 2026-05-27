from pydantic import BaseModel, Field

class IngredienteBase(BaseModel):
    nome: str 
    unidade: str 
    estoque: float = Field(ge=0, description="Não pode ser negativo")


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(BaseModel):
    nome: str | None = None 
    unidade: str | None = None
    estoque: float | None = Field(default=None, ge=0)

class IngredienteOut(IngredienteBase):
    id: int

    model_config = {"from_attributes": True}