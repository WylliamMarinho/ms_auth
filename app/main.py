# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 1. IMPORTE O CORS
from app.api.endpoints import auth

app = FastAPI(
    title="ms_auth",
    description="Microserviço de Autenticação",
    version="1.0.0"
)

# 2. DEFINA AS ORIGENS PERMITIDAS
# A URL do seu frontend React
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# 3. ADICIONE O MIDDLEWARE DE CORS À SUA APLICAÇÃO
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite que essas origens façam requisições
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


app.include_router(auth.router, prefix="/api/v1/auth")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Microserviço de Autenticação!"}