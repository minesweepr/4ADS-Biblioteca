import tkinter as tk
from tkinter import ttk

# root do estilo
## cores
BG = "#181B1E"
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