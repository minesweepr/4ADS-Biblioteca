from bdd import usuario_novo, usuario_por_email
import bcrypt

# criptografia bcrypt
def criptografar(senha: str):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar(senha: str, hash_bdd: str):
    return bcrypt.checkpw(senha.encode(), hash_bdd.encode())

# autenticação
def cadastro(nome: str, email: str, senha: str):
    usuario_novo(nome, email, criptografar(senha))

def login(email: str, senha: str):
    usuario=usuario_por_email(email,)

    if usuario is None:
        return None
    if not verificar(senha, usuario["senha"]):
        raise ValueError("Senha incorreta.")
    
    return {
        "id": usuario["id"],
        "nome": usuario["nome"],
        "email": usuario["email"],
        "tipo":  usuario["tipo"]
    }