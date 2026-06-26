import tkinter as tk
import os
from telas.emprestimo import Emprestimo
from telas.home import Home
from PIL import Image, ImageTk, ImageColor, ImageChops

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
F_PAG = ("Arial", 14, "bold")
F_BTN = ("Arial", 11, "bold")
F_BTN_ATV = ("Arial", 11, "bold", "underline")
F_TEXTO = ("Arial", 10)
F_QUOTE = ("Arial", 10, "italic")
F_PEQUENO = ("Arial", 8)

## caminhos
CAMINHO = os.path.dirname(__file__)
CAMINHO_LOGO = os.path.join(CAMINHO, "assets", "icone.png")
CAMINHO_CAPA = os.path.join(CAMINHO, "assets", "capa_livro_cinza.png")

def botao(parent, bg: str, command, text: str, **kw):
    btn = tk.Button(parent, bd=0, bg=bg, command=command, cursor="hand2", text=text, fg=BRANCO, 
                    font=F_BTN, padx=37, pady=9, activebackground=bg, activeforeground=BRANCO, **kw)
    return btn

def label_form(parent, text: str, **kw):
    return tk.Label(parent, text=text, font=F_TEXTO, fg=APAGADO, **kw)

def entry_form(parent, **kw):
    return tk.Entry(parent, font=F_TEXTO, bg=BG, fg=BRANCO, insertbackground=BRANCO, bd=0, relief="flat", 
                    highlightthickness=1, highlightbackground=BORDA, highlightcolor=ACCENT, **kw)

def logo(parent=None, bg=None):
    img = ImageTk.PhotoImage(Image.open(CAMINHO_LOGO))
    if parent is None:
        return img
    label = tk.Label(parent, image=img, bg=bg)
    label.image = img
    return label

def separador(parent):
    return tk.Frame(parent, height=1, bg=BORDA)

def carregar_capa(cor_hex="#00ffff", tamanho=(125, 179), pil=False):
    try:
        img = Image.open(CAMINHO_CAPA).convert("RGB")
        img = img.resize(tamanho)
        if pil:
            return img

        r, g, b = ImageColor.getrgb(cor_hex)
        color_layer = Image.new("RGB", img.size, (r, g, b))
        img = ImageChops.multiply(img, color_layer)

        return ImageTk.PhotoImage(img)
    except Exception:
        fallback = Image.new("RGB", tamanho, cor_hex)
        if pil:
            return fallback
        return ImageTk.PhotoImage(fallback)

class NavTopo(tk.Frame):
    def __init__(self, parent, usuario: dict, sair):
        super().__init__(parent, bg=NAV)
        
        self.parent = parent
        
        # barra superior
        barra_sup = tk.Frame(self, bg=NAV)
        barra_sup.pack(fill="x", pady=18)

        ## barra superior, lado esquerdo
        logo(barra_sup, NAV).pack(side="left", padx=20)
        tk.Label(barra_sup, text="Biblioteca Acadêmica", font=F_TITULO, fg=BRANCO, bg=NAV).pack(side="left")

        ## barra superior, lado direito
        btn_sair = botao(barra_sup, bg=DANGER, command=sair, text="Sair")
        btn_sair.pack(side="right", padx=23)

        tk.Label(barra_sup, text=f"({usuario.get("tipo")})", font=F_PEQUENO, fg=APAGADO, bg=NAV).pack(side="right")
        tk.Label(barra_sup, text=usuario.get("nome"), font=F_PEQUENO, fg=APAGADO, bg=NAV).pack(side="right")

        # separador
        separador(self).pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        # barra inferior
        barra_inf = tk.Frame(self, bg=NAV)
        barra_inf.pack(fill="x", pady=(0, 10))

        self.acervo = tk.Button(barra_inf, text="Acervo", font=F_BTN, bg=NAV, fg=APAGADO, bd=0, 
                                cursor="hand2", activebackground=NAV, activeforeground=ACCENT, 
                                command=lambda: (self._abrir_tela(Home), self._set_ativo("acervo")))
        self.acervo.pack(side="left", padx=23)

        self.emprestimo = tk.Button(barra_inf, text="Empréstimos", font=F_BTN, bg=NAV, fg=APAGADO, 
                                    bd=0, cursor="hand2", activebackground=NAV, activeforeground=ACCENT, 
                                    command=lambda: (self._abrir_tela(Emprestimo), self._set_ativo("emprestimo")))
        self.emprestimo.pack(side="left", padx=23)

        self.menu = {
            "acervo": self.acervo,
            "emprestimo": self.emprestimo
        }
        self._set_ativo("acervo")

    def _abrir_tela(self, TelaClasse):
        root = self.winfo_toplevel()

        for widget in root.winfo_children():
            if not isinstance(widget, NavTopo):
                widget.destroy()

        TelaClasse(root).pack(fill="both", expand=True)
    
    def _set_ativo(self, nome):
        for k, btn in self.menu.items():
            btn.config(fg=APAGADO, font=F_BTN)

        self.menu[nome].config(fg=ACCENT, font=F_BTN_ATV)