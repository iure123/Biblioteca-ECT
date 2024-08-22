from fastapi import APIRouter, HTTPException
from typing import List
from .models.modelos import LivrosAlugados
from database import get_db_connection

router = APIRouter()

@router.post("/livros_alugados/", response_model=LivrosAlugados)
def create_livros_alugados(livros_alugados: LivrosAlugados):
    """Cria um novo registro de livro alugado no banco de dados."""
    query = "INSERT INTO Livros_alugados (id, matricula_aluno, id_livro, data_aluguel, data_devolucao) VALUES (?, ?, ?, ?, ?)"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (livros_alugados.id, livros_alugados.matricula_aluno, livros_alugados.id_livro, livros_alugados.data_aluguel, livros_alugados.data_devolucao))
    conn.commit()
    conn.close()
    return livros_alugados

@router.get("/livros_alugados/{id}", response_model=LivrosAlugados)
def read_livros_alugados(id: int):
    """Recupera um registro de livro alugado pelo identificador."""
    query = "SELECT * FROM Livros_alugados WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Livro alugado não encontrado")
    return dict(row)

@router.put("/livros_alugados/{id}", response_model=LivrosAlugados)
def update_livros_alugados(id: int, livros_alugados: LivrosAlugados):
    """Atualiza as informações de um registro de livro alugado existente."""
    query = "UPDATE Livros_alugados SET matricula_aluno = ?, id_livro = ?, data_aluguel = ?, data_devolucao = ? WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (livros_alugados.matricula_aluno, livros_alugados.id_livro, livros_alugados.data_aluguel, livros_alugados.data_devolucao, id))
    conn.commit()
    conn.close()
    return livros_alugados

@router.delete("/livros_alugados/{id}", response_model=LivrosAlugados)
def delete_livros_alugados(id: int):
    """Remove um registro de livro alugado do banco de dados."""
    livros_alugados = read_livros_alugados(id)
    query = "DELETE FROM Livros_alugados WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (id,))
    conn.commit()
    conn.close()
    return livros_alugados
