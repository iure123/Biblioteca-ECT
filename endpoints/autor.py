from fastapi import APIRouter, HTTPException
from .models.modelos import Autor
from database import get_db_connection

router = APIRouter()

@router.post("/autor/", response_model=Autor)
def create_autor(autor: Autor):
    """Cria um novo autor no banco de dados."""
    query = "INSERT INTO Autor (id, Nome) VALUES (?, ?)"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (autor.id, autor.Nome))
    conn.commit()
    conn.close()
    return autor

@router.get("/autor/{id}", response_model=Autor)
def read_autor(id: int):
    """Obtém os dados de um autor pelo identificador."""
    query = "SELECT * FROM Autor WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return dict(row)

@router.put("/autor/{id}", response_model=Autor)
def update_autor(id: int, autor: Autor):
    """Atualiza as informações de um autor existente."""
    query = "UPDATE Autor SET Nome = ? WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (autor.Nome, id))
    conn.commit()
    conn.close()
    return autor

@router.delete("/autor/{id}", response_model=Autor)
def delete_autor(id: int):
    """Remove um autor do banco de dados."""
    autor = read_autor(id)
    query = "DELETE FROM Autor WHERE id = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (id,))
    conn.commit()
    conn.close()
    return autor
