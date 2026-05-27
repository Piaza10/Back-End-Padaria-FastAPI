from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, clientes, ingredientes, produtos, pedidos

app = FastAPI(
    title="BakeFlow",
    description="""
BakeFlow -> foi desenvolvida para ajudar microempreendedores a 
gerenciar seus negócios de forma otimizada.
    FUNCIONALIDADES:
    """,

    version="1.0",
    contact= {
        "Nome": "Miguel Gustavo (Piaza10)",
        "email": "miguelgustavo2004@gmail.com",
        "github": "https://github.com/Piaza10"
    },

    license_info={
        "name": "MIT"
    },
    
)


app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(ingredientes.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)



app.get("/health")
def root():
    return {"status": "Padaria Online"}

