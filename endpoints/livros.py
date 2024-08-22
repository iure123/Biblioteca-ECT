from fastapi import APIRouter, HTTPException
from typing import List
from .models.modelos import Livros
from database import get_db_connection
import uuid

router = APIRouter()

@router.post("/livros/", response_model=Livros)
def create_livros(livros: Livros):
    """Cria um novo livro no banco de dados."""
    query = "INSERT INTO Livros (id, Titulo, id_materia, id_autor, quantidade) VALUES (?, ?, ?, ?, ?)"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (uuid.uuid4().int, livros.Titulo, livros.id_materia, livros.id_autor, livros.quantidade))
    conn.commit()
    conn.close()
    return livros

@router.get("/livros/{id}", response_model=Livros)
def read_livros(id: int):
    """Recupera um livro pelo identificador."""
    query = "SELECT * FROM Livros WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return dict(row)

@router.put("/livros/{id}", response_model=Livros)
def update_livros(id: int, livros: Livros):
    """Atualiza as informações de um livro existente."""
    query = "UPDATE Livros SET Titulo = ?, id_materia = ?, id_autor = ?, quantidade = ? WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (livros.Titulo, livros.id_materia, livros.id_autor, livros.quantidade, id))
    conn.commit()
    conn.close()
    return livros

@router.delete("/livros/{id}", response_model=Livros)
def delete_livros(id: int):
    """Remove um livro do banco de dados."""
    livros = read_livros(id)
    query = "DELETE FROM Livros WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (id,))
    conn.commit()
    conn.close()
    return livros
