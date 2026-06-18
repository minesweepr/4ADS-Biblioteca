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