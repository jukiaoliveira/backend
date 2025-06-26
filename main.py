from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlalchemy
import databases
import shutil
import os

# Configuração do banco SQLite
DATABASE_URL = "sqlite:///./filmes.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Tabela de filmes
filmes = sqlalchemy.Table(
    "filmes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("titulo", sqlalchemy.String),
    sqlalchemy.Column("diretor", sqlalchemy.String),
    sqlalchemy.Column("ano", sqlalchemy.Integer),
    sqlalchemy.Column("imagem", sqlalchemy.String),  # Caminho da imagem
)

# Criação do banco
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

# App FastAPI
app = FastAPI()

# Liberação de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos da pasta /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelos de resposta
class Filme(BaseModel):
    id: int
    titulo: str
    diretor: str
    ano: int
    imagem: Optional[str] = None

# Conexão com o banco
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# GET - Listar todos os filmes
@app.get("/filmes", response_model=List[Filme])
async def listar_filmes():
    query = filmes.select()
    return await database.fetch_all(query)

# GET - Buscar filme por ID
@app.get("/filmes/{id}", response_model=Filme)
async def buscar_filme(id: int):
    query = filmes.select().where(filmes.c.id == id)
    resultado = await database.fetch_one(query)
    if resultado:
        return resultado
    raise HTTPException(status_code=404, detail="Filme não encontrado.")

# POST - Cadastrar novo filme com imagem
@app.post("/filmes", response_model=Filme)
async def cadastrar_filme(
    id: int = Form(...),
    titulo: str = Form(...),
    diretor: str = Form(...),
    ano: int = Form(...),
    imagem: UploadFile = File(...)
):
    # Verifica se ID já existe
    query_verifica = filmes.select().where(filmes.c.id == id)
    resultado = await database.fetch_one(query_verifica)
    if resultado:
        raise HTTPException(status_code=400, detail="ID já cadastrado.")

    # Salvar a imagem
    pasta = "static"
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, imagem.filename)
    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(imagem.file, buffer)

    caminho_relativo = f"/static/{imagem.filename}"

    # Inserir filme no banco
    query = filmes.insert().values(
        id=id,
        titulo=titulo,
        diretor=diretor,
        ano=ano,
        imagem=caminho_relativo
    )
    await database.execute(query)

    return {
        "id": id,
        "titulo": titulo,
        "diretor": diretor,
        "ano": ano,
        "imagem": caminho_relativo
    }

# DELETE - Remover filme por ID
@app.delete("/filmes/{id}")
async def deletar_filme(id: int):
    query = filmes.select().where(filmes.c.id == id)
    resultado = await database.fetch_one(query)

    if not resultado:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")

    delete_query = filmes.delete().where(filmes.c.id == id)
    await database.execute(delete_query)

    return {"mensagem": f"Filme com ID {id} foi deletado com sucesso."}