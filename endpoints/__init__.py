import sqlite3

# Conectar ao banco de dados (ou criar um novo banco de dados se não existir)
conn = sqlite3.connect('biblioteca.db')

# Criar um objeto cursor
cur = conn.cursor()

# Criar as tabelas
cur.execute('''
    CREATE TABLE IF NOT EXISTS Aluno (
        matricula BIGINT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        Data_Nasc DATE NOT NULL,
        password VARCHAR(255),
        email VARCHAR(255),
        bolsista BOOLEAN NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Bolsista (
        matricula_aluno BIGINT,
        Nome VARCHAR(255) NOT NULL,
        FOREIGN KEY (matricula_aluno) REFERENCES Aluno(matricula)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Autor (
        id INT PRIMARY KEY,
        Nome VARCHAR(255) NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Materia (
        id INT PRIMARY KEY,
        nome_materia VARCHAR(255) NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Livros (
        id INT PRIMARY KEY,
        Titulo VARCHAR(255) NOT NULL,
        id_materia INT,
        id_autor INT,
        quantidade INT,
        FOREIGN KEY (id_materia) REFERENCES Materia(id),
        FOREIGN KEY (id_autor) REFERENCES Autor(id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Livros_alugados (
        id INT PRIMARY KEY,
        matricula_aluno BIGINT,
        id_livro INT,
        data_aluguel DATE NOT NULL,
        data_devolucao DATE,
        FOREIGN KEY (matricula_aluno) REFERENCES Aluno(matricula),
        FOREIGN KEY (id_livro) REFERENCES Livros(id)
    )
''')

# Confirmar as alterações
conn.commit()

# Fechar a conexão
conn.close()
