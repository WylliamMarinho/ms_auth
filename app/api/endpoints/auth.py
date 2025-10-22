from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.core.security import create_access_token, verify_password, decode_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

# Simulação de um banco de dados de usuários
# Em um projeto real, usaria um banco de dados de verdade
USERS_DB = {
    "admin": {
        "username": "admin",
        "password_hash": "$5$rounds=535000$yQWgyEHTuPiGFZte$/qA2p34wqYBdkJZX0IvsKor0MzgRGkRrNbZwk4XyMNA",  # senha 'admin' hasheada
    },
    "teste": {
        "username": "teste",
        "password_hash": "$5$rounds=535000$.xjidg3YebLN.FKF$J.xZ3TpT/QCRwqgrIuoV0nHmObshrFMjglXANAotih2",
    }
}


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = USERS_DB.get(form_data.username)
    if not user_db or not verify_password(form_data.password, user_db["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=form_data.username)
    return {"access_token": access_token}


@router.post("/authenticate")
async def authenticate_token(token_data: dict):
    # O token será passado no corpo da requisição ou como um campo no corpo
    token = token_data.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token não fornecido.")

    try:
        payload = decode_token(token)
        return {"DATA": {"usuario": payload.get("sub"), "expira": payload.get("exp")}}
    except HTTPException as e:
        raise e


@router.get("/test")
async def test_endpoint(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        return {"status": "valid", "detail": "Token válido.", "user_data": payload}
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )