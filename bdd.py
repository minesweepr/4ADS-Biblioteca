import sqlite3
import os

BDD_PATH = os.path.join(os.path.dirname(__file__), "bookshelf.db")

def conector():
    conn = sqlite3.connect(BDD_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_bdd():
        with conector() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    tipo TEXT NOT NULL DEFAULT 'aluno' CHECK(tipo IN ('aluno', 'bibliotecario'))
                );
 
                CREATE TABLE IF NOT EXISTS livro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    quote TEXT,
                    disponivel INTEGER NOT NULL DEFAULT 1
                );
 
                CREATE TABLE IF NOT EXISTS emprestimo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_livro INTEGER NOT NULL,
                    id_aluno INTEGER NOT NULL,
                    data_emprestimo DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    data_previsao_retorno DATETIME NOT NULL,
                    data_retorno DATETIME,

                    FOREIGN KEY (id_livro) REFERENCES livro(id) ON DELETE CASCADE,
                    FOREIGN KEY (id_aluno) REFERENCES usuario(id) ON DELETE CASCADE
                );
            """)

# CRUD livros
def livro_listar_todos():
     with conector() as conn:
         return conn.execute("SELECT * FROM livro").fetchall()

def livro_listar_um(id: int):
    with conector() as conn:
         return conn.execute("SELECT * FROM livro WHERE id = ?", (id,)).fetchone()

def livro_novo(titulo: str, autor: str, quote: str):
    with conector() as conn:
        conn.execute("INSERT INTO livro (titulo, autor, quote) VALUES (?,?,?)", (titulo, autor, quote))

def livro_editar(id: int, titulo: str, autor: str, quote: str):
    with conector() as conn:
        conn.execute("UPDATE livro SET titulo = ?, autor = ?, quote = ? WHERE id = ?", (titulo, autor, quote, id))

def livro_deletar(id: int):
    with conector() as conn:
        conn.execute("DELETE FROM livro WHERE id = ?", (id,))