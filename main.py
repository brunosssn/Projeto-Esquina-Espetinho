from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI(title="Sistema de Gerenciamento do Espetinho da Esquina", version="1.3")

#Modelos-----------------------------------------------------------------------------------------------------------
#Cadastro de Funcionário
class FuncionarioEntrada(BaseModel):
    nome: str
    CPF: str
    data_de_nascimento: str
    cargo: str
    senha: str

class Funcionario(FuncionarioEntrada):
    id: str

#Cadastro de Gerente
class GerenteEntrada (BaseModel):
    nome: str
    CPF: str
    data_de_nascimento: str
    cargo: str
    senha: str

class Gerente(GerenteEntrada):
    id: str

#Cadastro de Categoria
class categoriaEntrada(BaseModel):
    categoria: str

class categoria(categoriaEntrada):
    id: str

#Cadastro dos produtos
class produtoEntrada(BaseModel):
    nome: str
    categoria_id: str
    descricao: str

class produto(produtoEntrada):
    id: str

#Cadastro dos pedidos
class pedidoEntrada(BaseModel):
    itens: str
    numero_da_mesa: str
    atendente_id: str
    estado_pedido: str

class pedido(pedidoEntrada):
    id: str


#Dados em Lista-------------------------------------------------------------------------------------------------------
funcionario_db: List[Funcionario] = []
gerente_db: List[Gerente] = []
categoria_db: List[categoria] = []
produto_db: List[produto] = []
pedido_db: List[pedido] = []


#Helpers (def)--------------------------------------------------------------------------------------------------------
def encontrar_funcionario(id: str) -> Funcionario:
    for a in funcionario_db:
        if a.id == id:
            return a
    raise HTTPException(status_code=404, detail="Funcionário não cadastrado")

def encontrar_gerente(id: str) -> Gerente:
    for b in gerente_db:
        if b.id == id:
            return b
    raise HTTPException(status_code=404, detail="Gerente não cadastrado")

def encontrar_produto(id: str) -> produto:
    for c in produto_db:
        if c.id == id:
            return c
    raise HTTPException(status_code=404, detail="Produto não cadastrado")

def encontrar_pedido(id: str) -> pedido:
    for d in pedido_db:
        if d.id == id:
            return d
    raise HTTPException(status_code=404, detail="Pedido não cadastrado")


#Métodos com Funcionário---------------------------------------------------------------------------------------------------
@app.get("/")
def raiz():
     return {"A API está funcionando!"}

@app.post("/Funcionário", response_model=Funcionario, status_code=201)
def criar_funcionario(dados: FuncionarioEntrada):
    novo = Funcionario(id=str(uuid.uuid4()), **dados.model_dump())
    funcionario_db.append(novo)
    return novo

@app.get("/Funcionário", response_model=List[Funcionario])
def listar_funcionarios():
    return funcionario_db

@app.get("/Funcionário/{id}", response_model=Funcionario)
def buscar_funcionario(id: str):
    return encontrar_funcionario(id)

@app.delete("/Funcionário/{id}", status_code=204)
def remover_funcionario(id: str):
    for i, a in enumerate(funcionario_db):
        if a.id == id:
            funcionario_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")

#Métodos com Gerente------------------------------------------------------------------------------------------------------
@app.post("/Gerente", response_model=Gerente, status_code=201)
def criar_gerente(dados: GerenteEntrada):
    nova = Gerente(id=str(uuid.uuid4()), **dados.model_dump())
    gerente_db.append(nova)
    return nova

@app.get("/Gerente/{id}", response_model=Gerente)
def buscar_gerente(id: str):
    return encontrar_gerente(id)

@app.delete("/Gerente/{id}", status_code=204)
def remover_gerente(id: str):
    for i, d in enumerate(gerente_db):
        if d.id == id:
            gerente_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Gerente não encontrado")

#Métodos com categoria------------------------------------------------------------------------------------------------------
@app.post("/Categoria", response_model=categoria, status_code=201)
def criar_categoria(dados: categoriaEntrada):
    nova = categoria(id=str(uuid.uuid4()), **dados.model_dump())
    categoria_db.append(nova)
    return nova

#Métodos com produtos------------------------------------------------------------------------------------------------------
@app.post("/Produto", response_model=produto, status_code=201)
def criar_produto(dados: produtoEntrada):
    nova = produto(id=str(uuid.uuid4()), **dados.model_dump())
    produto_db.append(nova)
    return nova

@app.get("/Produto", response_model=List[produto])
def listar_produtos():
    return produto_db

@app.get("/Produto/{id}", response_model=produto)
def buscar_produto(id: str):
    return encontrar_produto(id)

@app.delete("/Produto/{id}", status_code=204)
def remover_produto(id: str):
    for i, d in enumerate(produto_db):
        if d.id == id:
            produto_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Produto não encontrado")

#Métodos com pedidos------------------------------------------------------------------------------------------------------
@app.post("/Pedido", response_model=pedido, status_code=201)
def criar_pedido(dados: pedidoEntrada):
    nova = pedido(id=str(uuid.uuid4()), **dados.model_dump())
    pedido_db.append(nova)
    return nova

@app.get("/Pedido", response_model=List[pedido])
def listar_pedidos():
    return pedido_db

@app.get("/Pedido/{id}", response_model=pedido)
def buscar_pedido(id: str):
    return encontrar_pedido(id)

@app.patch("/pedidos/{id}", response_model=pedido)
def atualizar_estado_pedido(id: str, novo_estado: str):
    for p in pedido_db:
        if p.id == id:
            p.estado_pedido = novo_estado
            return p       
    raise HTTPException(status_code=404, detail="Pedido não encontrado")