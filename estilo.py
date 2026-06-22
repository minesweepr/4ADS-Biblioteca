import tkinter as tk
from telas.emprestimo import Emprestimo
from telas.home import Home
from telas.login import TelaLogin

# root do estilo
## cores
BG = "#181B1E"
NAV = "#1E2329"
CARD = "#272C32"
BORDA = "#343B42"
ACCENT = "#6CABEB"
SUCCESS = "#4E8A6E"
DANGER = "#B04040"
BRANCO = "#FFFFFF"
APAGADO = "#6C7986"

## fontes
F_TITULO = ("Arial", 20, "bold")
F_SUBTITULO = ("Arial", 16, "bold")
F_BTN = ("Arial", 11, "bold")
F_TEXTO = ("Arial", 10)
F_QUOTE = ("Arial", 10, "italic")
F_PEQUENO = ("Arial", 8)

def botao(parent, bg: str, command, text: str, **kw):
    btn = tk.Button(parent, bd=0, bg=bg, command=command, cursor="hand2", text=text, fg=BRANCO, 
                    font=F_BTN, padx=37, pady=9, activebackground=bg, activeforeground=BRANCO, **kw)
    return btn

def label_form(parent, text: str, **kw):
    return tk.Label(parent, text=text, font=F_TEXTO, fg=APAGADO, **kw)

def entry_form(parent, **kw):
    return tk.Entry(parent, font=F_TEXTO, bg=BG, fg=BRANCO, insertbackground=BRANCO, bd=0, relief="flat", 
                    highlightthickness=1, highlightbackground=BORDA, highlightcolor=ACCENT, **kw)

class NavTopo(tk.Frame):
    def __init__(self, parent, usuario: dict, sair):
        super().__init__(parent, bg=NAV)
        
        self.parent = parent

        # barra superior
        barra_sup = tk.Frame(self, bg=NAV)
        barra_sup.pack(fill="x", pady=(20, 0))

        ## barra superior, lado esquerdo
        tk.Label(barra_sup, text="Biblioteca Acadêmica", font=F_TITULO, fg=BRANCO, bg=NAV).pack(side="left", padx=23)
        ## TODO: adicionar logo/icone

        ## barra superior, lado direito
        btn_sair = botao(barra_sup, bg=DANGER, command=sair, text="Sair") # TODO: sair funcional
        btn_sair.pack(side="right", padx=23)

        tk.Label(barra_sup, text=f"({usuario.get("tipo")})", font=F_PEQUENO, fg=APAGADO, bg=NAV).pack(side="right")
        tk.Label(barra_sup, text=usuario.get("nome"), font=F_PEQUENO, fg=APAGADO, bg=NAV).pack(side="right")

        # separador
        tk.Frame(self, height=1, bg=BORDA).pack(side=tk.TOP, fill=tk.X, pady=(18, 10))
        
        # barra inferior
        barra_inf = tk.Frame(self, bg=NAV)
        barra_inf.pack(fill="x", pady=(0, 10))

        # TODO: fg muda dependendo da pagina
        self.acervo = tk.Button(barra_inf, text="Acervo", font=F_BTN, bg=NAV, fg=APAGADO, bd=0, 
                                cursor="hand2", activebackground=NAV, activeforeground=ACCENT, 
                                command=lambda: self._abrir_tela(Home))
        self.acervo.pack(side="left", padx=23)

        self.emprestimo = tk.Button(barra_inf, text="Empréstimos", font=F_BTN, bg=NAV, fg=APAGADO, 
                                    bd=0, cursor="hand2", activebackground=NAV, activeforeground=ACCENT, 
                                    command=lambda: self._abrir_tela(Emprestimo))
        self.emprestimo.pack(side="left", padx=23)

    def _abrir_tela(self, TelaClasse):
        root = self.winfo_toplevel()

        for widget in root.winfo_children():
            if not isinstance(widget, NavTopo):
                widget.destroy()

        TelaClasse(root).pack(fill="both", expand=True)