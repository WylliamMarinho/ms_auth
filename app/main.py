from fastapi import FastAPI
from app.api.endpoints import auth

app = FastAPI(
    title="ms_auth",
    description="Microserviço de Autenticação",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Microserviço de Autenticação!"}