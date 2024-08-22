from fastapi import APIRouter, HTTPException
from typing import List
from database import get_db_connection
from .models.modelos import Aluno

router = APIRouter()

@router.post("/aluno/", response_model=Aluno)
def create_aluno(aluno: Aluno):
    """Cria um novo aluno no banco de dados."""
    query = "INSERT INTO Aluno (matricula, nome, Data_Nasc, email) VALUES (?, ?, ?, ?)"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (aluno.matricula, aluno.nome, aluno.Data_Nasc, aluno.email))
    conn.commit()
    conn.close()
    return aluno

@router.get("/aluno/{matricula}", response_model=Aluno)
def read_aluno(matricula: int):
    """Obtém os dados de um aluno pelo número de matrícula."""
    query = "SELECT * FROM Aluno WHERE matricula = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (matricula,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return dict(row)

@router.get("/aluno/", response_model=List[Aluno])
def read_all_alunos():
    """Obtém todos os alunos do banco de dados."""
    query = "SELECT * FROM Aluno"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.put("/aluno/{matricula}", response_model=Aluno)
def update_aluno(matricula: int, aluno: Aluno):
    """Atualiza as informações de um aluno existente."""
    query = "UPDATE Aluno SET nome = ?, Data_Nasc = ?, email = ? WHERE matricula = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (aluno.nome, aluno.Data_Nasc, aluno.email, matricula))
    conn.commit()
    conn.close()
    return aluno

@router.delete("/aluno/{matricula}", response_model=Aluno)
def delete_aluno(matricula: int):
    """Remove um aluno do banco de dados."""
    aluno = read_aluno(matricula)
    query = "DELETE FROM Aluno WHERE matricula = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (matricula,))
    conn.commit()
    conn.close()
    return aluno
