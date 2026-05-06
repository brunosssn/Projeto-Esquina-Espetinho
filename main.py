from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI(title="API Escolar", version="1.0.0")

# ═══════════════════ MODELOS ═══════════════════

class AlunoEntrada(BaseModel):
    nome: str
    matricula: str
    email: str

class Aluno(AlunoEntrada):
    id: str

class DisciplinaEntrada(BaseModel):
    nome: str
    codigo: str
    descricao: str

class Disciplina(DisciplinaEntrada):
    id: str

class MatriculaEntrada(BaseModel):
    aluno_id: str
    disciplina_id: str

class Matricula(MatriculaEntrada):
    id: str

class InfracaoEntrada(BaseModel):
    aluno_id: str
    disciplina_id: str
    descricao: str
    gravidade: str

class Infracao(InfracaoEntrada):
    id: str
    data: str

# ═══════════════════ DADOS EM MEMÓRIA ═══════════════════

alunos_db:      List[Aluno]      = []
disciplinas_db: List[Disciplina] = []
matriculas_db:  List[Matricula]  = []
infracoes_db:   List[Infracao]   = []

# ═══════════════════ HELPERS ═══════════════════

def encontrar_aluno(id: str) -> Aluno:
    for a in alunos_db:
        if a.id == id:
            return a
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

def encontrar_disciplina(id: str) -> Disciplina:
    for d in disciplinas_db:
        if d.id == id:
            return d
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# ═══════════════════ ALUNOS ═══════════════════

@app.get("/")
def raiz():
    return {"mensagem": "API Escolar funcionando! 🏫"}

@app.post("/alunos", response_model=Aluno, status_code=201)
def criar_aluno(dados: AlunoEntrada):
    novo = Aluno(id=str(uuid.uuid4()), **dados.model_dump())
    alunos_db.append(novo)
    return novo

@app.get("/alunos", response_model=List[Aluno])
def listar_alunos():
    return alunos_db

@app.get("/alunos/{id}", response_model=Aluno)
def buscar_aluno(id: str):
    return encontrar_aluno(id)

@app.put("/alunos/{id}", response_model=Aluno)
def editar_aluno(id: str, dados: AlunoEntrada):
    for i, a in enumerate(alunos_db):
        if a.id == id:
            atualizado = Aluno(id=id, **dados.model_dump())
            alunos_db[i] = atualizado
            return atualizado
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.delete("/alunos/{id}", status_code=204)
def remover_aluno(id: str):
    for i, a in enumerate(alunos_db):
        if a.id == id:
            alunos_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

# ═══════════════════ DISCIPLINAS ═══════════════════

@app.post("/disciplinas", response_model=Disciplina, status_code=201)
def criar_disciplina(dados: DisciplinaEntrada):
    nova = Disciplina(id=str(uuid.uuid4()), **dados.model_dump())
    disciplinas_db.append(nova)
    return nova

@app.get("/disciplinas", response_model=List[Disciplina])
def listar_disciplinas():
    return disciplinas_db

@app.get("/disciplinas/{id}", response_model=Disciplina)
def buscar_disciplina(id: str):
    return encontrar_disciplina(id)

@app.put("/disciplinas/{id}", response_model=Disciplina)
def editar_disciplina(id: str, dados: DisciplinaEntrada):
    for i, d in enumerate(disciplinas_db):
        if d.id == id:
            atualizada = Disciplina(id=id, **dados.model_dump())
            disciplinas_db[i] = atualizada
            return atualizada
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

@app.delete("/disciplinas/{id}", status_code=204)
def remover_disciplina(id: str):
    for i, d in enumerate(disciplinas_db):
        if d.id == id:
            disciplinas_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

# ═══════════════════ MATRÍCULAS ═══════════════════

@app.post("/matriculas", response_model=Matricula, status_code=201)
def matricular_aluno(dados: MatriculaEntrada):
    encontrar_aluno(dados.aluno_id)
    encontrar_disciplina(dados.disciplina_id)
    for m in matriculas_db:
        if m.aluno_id == dados.aluno_id and m.disciplina_id == dados.disciplina_id:
            raise HTTPException(status_code=409, detail="Aluno já matriculado nesta disciplina")
    nova = Matricula(id=str(uuid.uuid4()), **dados.model_dump())
    matriculas_db.append(nova)
    return nova

@app.get("/alunos/{id}/disciplinas", response_model=List[Disciplina])
def disciplinas_do_aluno(id: str):
    encontrar_aluno(id)
    ids_disc = {m.disciplina_id for m in matriculas_db if m.aluno_id == id}
    return [d for d in disciplinas_db if d.id in ids_disc]

@app.get("/disciplinas/{id}/alunos", response_model=List[Aluno])
def alunos_da_disciplina(id: str):
    encontrar_disciplina(id)
    ids_alunos = {m.aluno_id for m in matriculas_db if m.disciplina_id == id}
    return [a for a in alunos_db if a.id in ids_alunos]

@app.delete("/matriculas/{id}", status_code=204)
def cancelar_matricula(id: str):
    for i, m in enumerate(matriculas_db):
        if m.id == id:
            matriculas_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Matrícula não encontrada")

# ═══════════════════ INFRAÇÕES ═══════════════════

@app.post("/infracoes", response_model=Infracao, status_code=201)
def registrar_infracao(dados: InfracaoEntrada):
    encontrar_aluno(dados.aluno_id)
    encontrar_disciplina(dados.disciplina_id)
    nova = Infracao(
        id=str(uuid.uuid4()),
        data=datetime.now().isoformat(),
        **dados.model_dump()
    )
    infracoes_db.append(nova)
    return nova

@app.get("/infracoes", response_model=List[Infracao])
def listar_infracoes():
    return infracoes_db

@app.get("/infracoes/{id}", response_model=Infracao)
def buscar_infracao(id: str):
    for inf in infracoes_db:
        if inf.id == id:
            return inf
    raise HTTPException(status_code=404, detail="Infração não encontrada")

@app.get("/alunos/{id}/infracoes", response_model=List[Infracao])
def infracoes_do_aluno(id: str):
    encontrar_aluno(id)
    return [inf for inf in infracoes_db if inf.aluno_id == id]

@app.get("/disciplinas/{id}/infracoes", response_model=List[Infracao])
def infracoes_da_disciplina(id: str):
    encontrar_disciplina(id)
    return [inf for inf in infracoes_db if inf.disciplina_id == id]

@app.put("/infracoes/{id}", response_model=Infracao)
def editar_infracao(id: str, dados: InfracaoEntrada):
    for i, inf in enumerate(infracoes_db):
        if inf.id == id:
            atualizada = Infracao(id=id, data=inf.data, **dados.model_dump())
            infracoes_db[i] = atualizada
            return atualizada
    raise HTTPException(status_code=404, detail="Infração não encontrada")

@app.delete("/infracoes/{id}", status_code=204)
def remover_infracao(id: str):
    for i, inf in enumerate(infracoes_db):
        if inf.id == id:
            infracoes_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Infração não encontrada")