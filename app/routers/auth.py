from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut  # vamos criar abaixo
from app.auth.hashing import hash_senha, verificar_senha
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.jwt import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == form.username).first()
    if not usuario or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    token = criar_token({"sub": usuario.email, "role": usuario.role})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/registrar", response_model=UsuarioOut, status_code=201)
def registrar(dados: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        role=dados.role
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario