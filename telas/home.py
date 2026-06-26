import tkinter as tk
import estilo as st

from telas.livro_detalhe import LivroDetalhe
from telas.form_livro import FormLivro
from paginacao import *
import bdd

class Home(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.configure(bg=st.BG)

        self.limite = 12
        self.pagina = 0
        self.total = bdd.livro_count()

        self.cards = [] 

        titulo_frame = tk.Frame(self, bg=st.BG)
        titulo_frame.pack(fill="x", pady=20, padx=35)
        titulo_frame.grid_columnconfigure(0, weight=1)
        #titulo_frame.grid_columnconfigure(1, weight=1)
        titulo_frame.grid_columnconfigure(2, weight=1)

        titulo = tk.Label(titulo_frame, text="Todos os livros", font=st.F_SUBTITULO, fg=st.BRANCO, bg=st.BG)
        titulo.grid(row=0, column=0, sticky="w")

        self.paginacao_frame = Paginacao(self, total=self.total, limite=self.limite, pagina=self.pagina, on_change=lambda p: mudar_pagina(self, p))
        self.paginacao_frame.pack(side="bottom", pady=(0, 10))

        if self.master.usuario_logado["tipo"] == "bibliotecario":
            botao = st.botao(titulo_frame, st.ACCENT,
                                    lambda: (
                                        self.destroy(),
                                        FormLivro(self.master, on_close=self.abrir_home).pack(fill="both", expand=True)
                                    ),"Adicionar")
            botao.grid(row=0, column=2, sticky="e")

        # frame dos livros
        self.grid_frame = tk.Frame(self, bg=st.BG)
        self.grid_frame.pack(fill="both", expand=True, padx=40, pady=20)

        self.carregar_dados()

        self.bind("<Configure>", self.on_resize)

    def carregar_dados(self):
        for card in self.cards:
            card.destroy()
        self.cards.clear()

        self.limite = self.calcular_limite()

        offset = self.pagina * self.limite
        self.livros = bdd.livro_listar_paginado(self.limite, offset)

        self.total = bdd.livro_count()

        self.criar_cards()

        atualizar_paginacao(self)

    def criar_cards(self):
        for livro in self.livros:

            card = tk.Frame(self.grid_frame, bg=st.BG, width=125, height=250, cursor="hand2")
            card.grid_propagate(False)

            img = st.carregar_capa(livro["hex"],tamanho=(125, 179))
            capa = tk.Label(card, image=img, bg=st.BG)
            capa.image = img
            capa.grid(row=0, column=0)
            capa.grid_propagate(False)

            nome = tk.Label(card, text=(livro["titulo"][:25] + "...") if len(livro["titulo"]) > 25 else livro["titulo"], fg=st.BRANCO, bg=st.BG, font=st.F_TEXTO, wraplength=120, justify="center", height=2)
            nome.grid(row=1, column=0)

            texto_disponivel = ("Disponível" if livro["disponivel"] else "Indisponível")

            cor_disponivel = (st.SUCCESS if livro["disponivel"] else st.DANGER)

            disponibilidade = tk.Label(card, text=texto_disponivel, fg=cor_disponivel, bg=st.BG, font=st.F_PEQUENO)
            disponibilidade.grid(row=2, column=0)

            for widget in (card, capa, nome, disponibilidade):
                widget.bind("<Button-1>", lambda e, lid=livro["id"]: self.abrir_detalhe(lid))

            self.cards.append(card)

        self.organizar_cards()

    # responsividade 
    def organizar_cards(self):
        col = max(1, self.winfo_width() // 190)

        for i in range(col + 2):
            self.grid_frame.grid_columnconfigure(i, weight=0)

        self.grid_frame.grid_columnconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(col + 1, weight=1)

        for i, card in enumerate(self.cards): card.grid(row=i // col, column=(i % col) + 1, padx=12, pady=10, sticky="n")

    def calcular_limite(self):
        card_w = 190
        card_h = 260

        col = max(1, self.winfo_width() // card_w)
        row = max(1, (self.winfo_height() - 120) // card_h)

        return col * row
    
    def on_resize(self, event):
        novo_limite = self.calcular_limite()
        if novo_limite != self.limite:
            self.pagina = 0
            self.carregar_dados()
        else:
            self.organizar_cards()

    def abrir_detalhe(self, livro_id):
        self.destroy()
        LivroDetalhe(self.master, livro_id, on_close=self.abrir_home).pack(fill="both", expand=True)

    def abrir_home(self):
        self.destroy()
        Home(self.master).pack(fill="both", expand=True)


