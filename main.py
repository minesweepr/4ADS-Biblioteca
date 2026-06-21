import tkinter as tk
import estilo
from bdd import init_bdd
from telas.login import TelaLogin
from telas.home import Home

"""
nome: Administrador
email: bibli@tecario.com
senha: 123456
"""
# TODO: melhorar a main
if __name__ == "__main__":
    init_bdd()

    def _login_sucesso(usuario_logado):
        tela.destroy()
        topbar = estilo.NavTopo(parent=root, usuario=usuario_logado)
        topbar.pack(side="top", fill="x")
        
        root.usuario_logado = usuario_logado
        
        home = Home(root)
        home.pack(fill="both", expand=True)

        
    root = tk.Tk()
    root.geometry("1040x690")
    root.title("Biblioteca Acadêmica")
    # mudar icone
    root.configure(bg=estilo.BG)

    tela = TelaLogin(master=root, on_success=_login_sucesso)
    tela.pack(fill="both", expand=True)

    root.mainloop()