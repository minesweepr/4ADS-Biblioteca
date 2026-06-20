import sqlite3
import os

BDD_PATH = os.path.join(os.path.dirname(__file__), "biblio4ads.db")

def conector():
    conn = sqlite3.connect(BDD_PATH)
    conn.row_factory = sqlite3.Row # permite acessar colunas pelo nome ao invés do número com TULPAS
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
                    status TEXT NOT NULL CHECK(status IN ('ATIVO','FINALIZADO')) DEFAULT 'ATIVO',

                    FOREIGN KEY (id_livro) REFERENCES livro(id) ON DELETE CASCADE,
                    FOREIGN KEY (id_aluno) REFERENCES usuario(id) ON DELETE CASCADE
                );
                               
                CREATE TRIGGER IF NOT EXISTS trg_bloqueia_emprestimo
                BEFORE INSERT ON emprestimo
                WHEN EXISTS(
                    SELECT 1
                    FROM emprestimo
                    WHERE id_aluno = NEW.id_aluno
                    AND status = 'ATIVO'
                    AND data_previsao_retorno < DATETIME('now')
                )
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Aluno possui emprestimo atrasado'
                    );
                END;
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

# usuário
def usuario_novo(nome: str, email: str, senha: str):
    try:
        with conector() as conn:
            conn.execute("INSERT INTO usuario (nome, email, senha, tipo) VALUES (?,?,?,?)", (nome, email, senha, "aluno"))
    except sqlite3.IntegrityError:
        raise ValueError("Esse email já está cadastrado no sistema.")
    except sqlite3.Error as e:
        raise RuntimeError(f"Erro interno ao criar novo usuario: {e}")
    
def usuario_por_email(email: str):
    try:
        with conector() as conn:
            return conn.execute("SELECT id, nome, email, senha, tipo FROM usuario WHERE email = ?", (email,)).fetchone()
    except sqlite3.Error as e:
        raise RuntimeError(f"Erro interno ao buscar usuario: {e}")

#crud emprestimo    
from datetime import datetime

def usuario_possui_restricao(id_aluno:int):
    with conector() as conn:
        emprestimos=conn.execute("SELECT data_previsao_retorno FROM emprestimo WHERE id_aluno=? AND status='ATIVO'",(id_aluno,)).fetchall()
        agora=datetime.now()
        for e in emprestimos:
            if datetime.fromisoformat(e["data_previsao_retorno"])<agora:
                return True
        return False
    
def emprestimo_listar_todos():
    with conector() as conn:
        return conn.execute("SELECT * FROM emprestimo").fetchall()
    
def emprestimo_listar_um(id:int):
    with conector() as conn:
        return conn.execute("SELECT * FROM emprestimo WHERE id=?",(id,)).fetchone()
    
def emprestimo_novo(id_livro:int,id_aluno:int,data_previsao_retorno:str):
    if usuario_possui_restricao(id_aluno):
        raise ValueError("Aluno possui empréstimo em atraso.")
    
    livro=livro_listar_um(id_livro)
    if not livro or livro["disponivel"]==0:
        raise ValueError("Livro indisponível.")    

    with conector() as conn:
        conn.execute("INSERT INTO emprestimo(id_livro,id_aluno,data_previsao_retorno,status) VALUES(?,?,?,'ATIVO')",(id_livro,id_aluno,data_previsao_retorno))
        conn.execute("UPDATE livro SET disponivel=0 WHERE id=?",(id_livro,))
    
def emprestimo_devolver(id_emprestimo:int):
    with conector() as conn:
        emprestimo=conn.execute("SELECT id_livro FROM emprestimo WHERE id=?",(id_emprestimo,)).fetchone()
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado.")
        conn.execute("UPDATE emprestimo SET status='FINALIZADO',data_retorno=CURRENT_TIMESTAMP WHERE id=?",(id_emprestimo,))
        conn.execute("UPDATE livro SET disponivel=1 WHERE id=?",(emprestimo["id_livro"],))

def emprestimo_editar(id:int,id_livro:int,id_aluno:int,data_previsao_retorno:str):
    with conector() as conn:
        conn.execute("UPDATE emprestimo SET id_livro=?,id_aluno=?,data_previsao_retorno=? WHERE id=?",(id_livro,id_aluno,data_previsao_retorno,id))
