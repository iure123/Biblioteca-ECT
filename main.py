from fastapi import FastAPI
from endpoints import alunos, autor, materia, livros, livros_alugados

app = FastAPI()

# Inclui os endpoints dos módulos separados
app.include_router(alunos.router)
app.include_router(autor.router)
app.include_router(materia.router)
app.include_router(livros.router)
app.include_router(livros_alugados.router)

if __name__ == "__main__":
    from uvicorn import run
    run("main:app", host ="0.0.0.0", port = 8000, reload = True)