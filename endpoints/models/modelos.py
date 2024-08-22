from pydantic import BaseModel
from typing import Optional
from datetime import date

class Aluno(BaseModel):
    matricula: int
    nome: str
    Data_Nasc: date
    email: Optional[str] = None

    class Config:
        orm_mode = True

class Bolsista(BaseModel):
    matricula_aluno: int
    Nome: str

    class Config:
        orm_mode = True

class Autor(BaseModel):
    id: int
    Nome: str

    class Config:
        orm_mode = True

class Materia(BaseModel):
    id: int
    nome_materia: str

    class Config:
        orm_mode = True

class Livros(BaseModel):
    id: int
    Titulo: str
    id_materia: Optional[int] = None
    id_autor: Optional[int] = None

    class Config:
        orm_mode = True

class LivrosAlugados(BaseModel):
    id: int
    matricula_aluno: int
    id_livro: int
    data_aluguel: date
    data_devolucao: Optional[date] = None

    class Config:
        orm_mode = True
