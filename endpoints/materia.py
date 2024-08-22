from fastapi import APIRouter, HTTPException
from typing import List
from .models.modelos import Materia
from database import get_db_connection

router = APIRouter()

@router.post("/materia/", response_model=Materia)
def create_materia(materia: Materia):
    """Cria uma nova matéria no banco de dados."""
    query = "INSERT INTO Materia (id, nome_materia) VALUES (?, ?)"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (materia.id, materia.nome_materia))
    conn.commit()
    conn.close()
    return materia

@router.get("/materia/{id}", response_model=Materia)
def read_materia(id: int):
    """Recupera uma matéria pelo identificador."""
    query = "SELECT * FROM Materia WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    return dict(row)

@router.put("/materia/{id}", response_model=Materia)
def update_materia(id: int, materia: Materia):
    """Atualiza as informações de uma matéria existente."""
    query = "UPDATE Materia SET nome_materia = ? WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (materia.nome_materia, id))
    conn.commit()
    conn.close()
    return materia

@router.delete("/materia/{id}", response_model=Materia)
def delete_materia(id: int):
    """Remove uma matéria do banco de dados."""
    materia = read_materia(id)
    query = "DELETE FROM Materia WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (id,))
    conn.commit()
    conn.close()
    return materia
