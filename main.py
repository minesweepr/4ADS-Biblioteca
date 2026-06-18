from bdd import *

# teste das funcionalidades basicas
init_bdd()

print("TESTE 1")
livro_novo("L'arte Della Gioia", "Goliarda Sapienza", "Because the senses follow the intellect and vice versa.")
print(livro_listar_todos())


print("\n\nTESTE 2")
livro_novo("Odisséia", "Homer", "O homem é o que ele faz, não o que ele diz que fará.")
livro_novo("O Nome da Rosa", "Umberto Eco", "Se libertar do medo do diabo é sabedoria.")
livro_novo("a", "a", "a")

print(livro_listar_todos())


print("\n\nTESTE 3")
livro_editar(2, "Odisséia", "Homero", "O homem é o que ele faz, não o que ele diz que fará.")
print(f"\n{livro_listar_um(2)}")

livro_deletar(4)

print(f"\n{livro_listar_todos()}")