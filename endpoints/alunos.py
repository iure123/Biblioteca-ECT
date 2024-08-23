import bcrypt
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from pydantic import BaseModel
from database import get_db_connection
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .models.modelos import Aluno, Token, TokenData

# Configurações do JWT
SECRET_KEY = "your_secret_key"  # Substitua por uma chave secreta segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Instância do roteador
router = APIRouter()

# Configuração da segurança
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginForm(BaseModel):
    username: str
    password: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> 'TokenData':
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        matricula: int = payload.get("matricula")
        if matricula is None:
            raise credentials_exception
        token_data = TokenData(matricula=matricula)
    except JWTError:
        raise credentials_exception
    return token_data


# Rotas
@router.post("/token", response_model=Token)
def login(form_data: LoginForm):
    query = "SELECT matricula, password FROM Aluno WHERE matricula = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (form_data.username,))
    user = cur.fetchone()
    conn.close()
    if user is None or not verify_password(form_data.password, user[1]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"matricula": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/aluno/me", response_model=TokenData)
def get_user_info(current_user: TokenData = Depends(get_current_user)):
    """Retorna as informações do usuário atual."""
    return current_user

@router.post("/aluno/", response_model=Aluno)
def create_aluno(aluno: Aluno, token: str = Depends(oauth2_scheme)):
    """Cria um novo aluno no banco de dados."""
    query = "INSERT INTO Aluno (matricula, nome, Data_Nasc, email, bolsista, password) VALUES (?, ?, ?, ?, ?, ?)"
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = get_password_hash(aluno.password)
    cur.execute(query, (aluno.matricula, aluno.nome, aluno.Data_Nasc, aluno.email, aluno.bolsista, hashed_password))
    conn.commit()
    conn.close()
    return aluno

@router.get("/aluno/{matricula}", response_model=Aluno)
def read_aluno(matricula: int, token: str = Depends(oauth2_scheme)):
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
def read_all_alunos(token: str = Depends(oauth2_scheme)):
    """Obtém todos os alunos do banco de dados."""
    query = "SELECT * FROM Aluno"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.put("/aluno/{matricula}", response_model=Aluno)
def update_aluno(matricula: int, aluno: Aluno, token: str = Depends(oauth2_scheme)):
    """Atualiza as informações de um aluno existente."""
    query = "UPDATE Aluno SET nome = ?, Data_Nasc = ?, email = ?, bolsista = ? WHERE matricula = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (aluno.nome, aluno.Data_Nasc, aluno.email, aluno.bolsista, matricula))
    conn.commit()
    conn.close()
    return aluno

@router.delete("/aluno/{matricula}", response_model=Aluno)
def delete_aluno(matricula: int, token: str = Depends(oauth2_scheme)):
    """Remove um aluno do banco de dados."""
    aluno = read_aluno(matricula, token)
    query = "DELETE FROM Aluno WHERE matricula = ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (matricula,))
    conn.commit()
    conn.close()
    return aluno
