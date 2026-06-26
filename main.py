import tkinter as tk
import estilo as st
from bdd import init_bdd
from telas.login import TelaLogin
from telas.home import Home

class BibliotecaAcademica(tk.Tk):
    def __init__(self):
        super().__init__()
        largura = 950
        altura = 830
        coordenada_x = (self.winfo_screenwidth() - largura) // 2
        coordenada_y = (self.winfo_screenheight() - altura) // 2
        self.geometry(f"{largura}x{altura}+{coordenada_x}+{coordenada_y}")
        self.title("Biblioteca Acadêmica")
        self.configure(bg=st.BG)

        img_favicon = st.logo() 
        self.iconphoto(True, img_favicon)
        
        self.usuario_logado = None

        self.login_mostrar()

    def login_mostrar(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.tela = TelaLogin(master=self, on_success=self.login_sucesso)
        self.tela.pack(fill="both", expand=True)
        self.usuario_logado = None

    def login_sucesso(self, usuario):
        self.usuario_logado = usuario

        self.tela.destroy()
        
        topbar = st.NavTopo(parent=self, usuario=self.usuario_logado, sair=lambda: self.login_mostrar())
        topbar.pack(side="top", fill="x")
        home = Home(self)
        home.pack(fill="both", expand=True)

if __name__ == "__main__":
    init_bdd()
    BibliotecaAcademica().mainloop()