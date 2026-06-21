from bdd import *
from autenticacao import *

# teste das funcionalidades basicas
# CRUD livros
init_bdd()

print("TESTE 1")
livro_novo("L'arte Della Gioia", "Goliarda Sapienza", "Because the senses follow the intellect and vice versa.")
print([dict(livro) for livro in livro_listar_todos()])


print("\n\nTESTE 2")
livro_novo("Odisséia", "Homer", "O homem é o que ele faz, não o que ele diz que fará.")
livro_novo("O Nome da Rosa", "Umberto Eco", "Se libertar do medo do diabo é sabedoria.")
livro_novo("a", "a", "a")

print([dict(livro) for livro in livro_listar_todos()])


print("\n\nTESTE 3")
livro_editar(2, "Odisséia", "Homero", "O homem é o que ele faz, não o que ele diz que fará.")
print(f"\n{[dict(livro_listar_um(2)) if livro_listar_um(2) else None]}")

livro_deletar(4)

print(f"\n{[dict(livro) for livro in livro_listar_todos()]}")

# cadastro
try:
    cadastro("nteste", "eteste", "teste")

    usuario_bdd=usuario_por_email("eteste")
    print(f"dados no banco: {[dict(usuario_bdd)]}")
    print("deu tudo certo no cadastro")
except ValueError as e:
    print(f"erro de valor {e}")
except RuntimeError as e:
    print(f"erro de run {e}")

# login
try:
    login("eteste", "teste")
    print("deu tudo certo no login")
except ValueError as e:
    print(f"erro de valor {e}")
except RuntimeError as e:
    print(f"erro de run {e}")


# Emprestimo, devolução e restrição
from datetime import datetime,timedelta

print("\n\nTESTE 4 - pedir EMPRESTIMO")

data_prevista=(datetime.now()+timedelta(days=7)).isoformat()

emprestimo_novo(id_livro=1,id_aluno=1,data_previsao_retorno=data_prevista)

print("\nLivro 1:")
print(dict(livro_listar_um(1)))

print("\nEmprestimos:")
print([dict(e) for e in emprestimo_listar_todos()])

print("\nRestricao:", usuario_possui_restricao(1))

print("\n\nTESTE 5 - emprestimo no mesmo LIVRO")

try:
    emprestimo_novo(id_livro=1,id_aluno=1,data_previsao_retorno=data_prevista)
    print("ERRO: deveria bloquear")
except Exception as e:
    print("Bloqueado corretamente:", e)

print("\nLivro 1:")
print(dict(livro_listar_um(1)))

print("\nEmprestimos:")
print([dict(e) for e in emprestimo_listar_todos()])


print("\n\nTESTE 6 - GERAR ATRASO / Restrição")

ontem=(datetime.now()-timedelta(days=1)).isoformat()

with conector() as conn:
    conn.execute("UPDATE emprestimo SET data_previsao_retorno=? WHERE id=1",(ontem,))

print("\nEmprestimos:")
print([dict(e) for e in emprestimo_listar_todos()])

print("\nRestricao:", usuario_possui_restricao(1))


print("\n\nTESTE 7 - tentar EMPRESTIMO com RESTRIÇAO")

try:
    emprestimo_novo(id_livro=2,id_aluno=1,data_previsao_retorno=data_prevista)
    print("ERRO: deveria bloquear")
except Exception as e:
    print("Bloqueado corretamente:", e)

print("\nLivro 2:")
print(dict(livro_listar_um(2)))

print("\nEmprestimos:")
print([dict(e) for e in emprestimo_listar_todos()])

# devolver livro na qual restriçao esta vinculada
print("\n\nTESTE 8 - DEVOLUCAO")

emprestimo_devolver(1)

print("\nLivro 1:")
print(dict(livro_listar_um(1)))

print("\nEmprestimos:")
print([dict(e) for e in emprestimo_listar_todos()])

print("\nRestricao:", usuario_possui_restricao(1))

# tendo tirado a restriçao
print("\n\nTESTE 9 - NOVO EMPRESTIMO LIBERADO")

emprestimo_novo(id_livro=2,id_aluno=1,data_previsao_retorno=data_prevista)

print("\nLivro 2:")
print(dict(livro_listar_um(2)))

print("\nEmprestimos:")
print([dict(e) for e in emprestimo_listar_todos()])

print("\n\nTESTE 10 - EDITAR EMPRESTIMO")
print("\nANTES:", dict(emprestimo_listar_um(2)))
emprestimo_editar(2,2,1,"2030-12-31")
print("\nDEPOIS:", dict(emprestimo_listar_um(2)))