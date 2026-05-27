from pydantic import BaseModel, Field

class IngredienteProduto(BaseModel):
    ingrediente_id: int
    quantidade: float = Field(gt=0)


class ProdutoBase(BaseModel):
    nome: str
    preco: float = Field(gt=0)
    

class ProdutoCreate(ProdutoBase):
    ingredientes: list[IngredienteProduto] = []


class ProdutoUpdate(BaseModel):
    nome: str   | None = None
    preco: float    | None = Field(default=None, gt=0)
    ingredientes: list[IngredienteProduto]  | None = None


class IngredienteOut(BaseModel):
    id: int
    nome: str
    unidade: str
    quantidade: float

    model_config = {"from_attributes": True}


class ProdutoOut(ProdutoBase):
    id: int
    ingredientes: list[IngredienteOut] = []

    model_config = {"from_attributes": True}

