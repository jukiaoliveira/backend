from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlalchemy
import databases

# Banco de dados SQLite
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
)

# Conexão com o banco
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # libera qualquer origem durante desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],  # permite todos os métodos (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # permite todos os headers
)


# (entrada e saída)
class Filme(BaseModel):
    id: int
    titulo: str
    diretor: str
    ano: int

# Conectar/desconectar 
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# GET - Lista todos os filmes
@app.get("/filmes", response_model=List[Filme])
async def listar_filmes():
    query = filmes.select()
    return await database.fetch_all(query)

# POST - Cadastrar novo filme
@app.post("/filmes", response_model=Filme)
async def cadastrar_filme(filme: Filme):
    # Verificar se ID já existe
    query_verifica = filmes.select().where(filmes.c.id == filme.id)
    resultado = await database.fetch_one(query_verifica)
    if resultado:
        raise HTTPException(status_code=400, detail="ID já cadastrado.")

    query = filmes.insert().values(
        id=filme.id, titulo=filme.titulo, diretor=filme.diretor, ano=filme.ano
    )
    await database.execute(query)
    return filme

# GET - Buscar filme por ID
@app.get("/filmes/{id}", response_model=Filme)
async def buscar_filme(id: int):
    query = filmes.select().where(filmes.c.id == id)
    resultado = await database.fetch_one(query)
    if resultado:
        return resultado
    raise HTTPException(status_code=404, detail="Filme não encontrado.")

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