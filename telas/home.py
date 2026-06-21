import tkinter as tk

import estilo as st
from telas.livro_detalhe import LivroDetalhe
from telas.adicionar_livro import AdicionarLivro
import bdd

class Home(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        print(self.master.usuario_logado)
        
        self.configure(bg=st.BG)

        self.cards = []

        self.titulo_frame = tk.Frame(self, bg=st.BG)
        self.titulo_frame.pack(fill="both", pady=20, padx=35)

        titulo = tk.Label( self.titulo_frame, text="Todos os livros", font=st.F_SUBTITULO, fg=st.BRANCO, bg=st.BG )
        titulo.pack(side="left")

        if self.master.usuario_logado["tipo"]=="bibliotecario":
            self.botao = st.botao(self.titulo_frame, st.ACCENT, self.cadastrar_livro, "Adicionar")
            self.botao.pack(side="right")

        self.grid_frame = tk.Frame(self, bg=st.BG)
        self.grid_frame.pack(fill="both", expand=True, padx=40)

        self.livros = bdd.livro_listar_todos()

        self.criar_cards()

        self.bind("<Configure>", self.on_resize)

    def criar_cards(self):
        for livro in self.livros:

            card = tk.Frame( self.grid_frame, bg=st.BG, width=125, height=240, cursor="hand2" )
            card.grid_propagate(False)

            capa = tk.Frame( card, width=125, height=179, bg="#D9D9D9" )
            capa.grid(row=0, column=0)
            capa.grid_propagate(False)

            nome = tk.Label( card, text=livro["titulo"], fg=st.BRANCO, bg=st.BG, font=st.F_TEXTO )
            nome.grid(row=1, column=0)

            texto_disponivel = ( "Disponível" if livro["disponivel"] else "Indisponível" )

            cor_disponivel = ( st.SUCCESS if livro["disponivel"] else st.DANGER )

            disponibilidade = tk.Label( card, text=texto_disponivel, fg=cor_disponivel, bg=st.BG, font=st.F_PEQUENO )
            disponibilidade.grid(row=2, column=0)

            self.bind_card_click(card, livro["id"])
            self.bind_card_click(capa, livro["id"])
            self.bind_card_click(nome, livro["id"])
            self.bind_card_click(disponibilidade, livro["id"])

            self.cards.append(card)

        self.organizar_cards()

    def organizar_cards(self):
        col = max(1, self.winfo_width() // 190)

        for i, card in enumerate(self.cards):
            card.grid( row=i // col, column=i % col, padx=15, pady=15 )

    def on_resize(self, event):
        self.organizar_cards()
    
    def abrir_detalhe(self, livro_id):
        self.destroy()
        LivroDetalhe(self.master, livro_id, on_close=self.abrir_home).pack(fill="both", expand=True)

    def bind_card_click(self, widget, livro_id):
        widget.bind( "<Button-1>", lambda e, lid=livro_id: self.abrir_detalhe(lid))

    def cadastrar_livro(self):
        self.destroy()
        AdicionarLivro(self.master, on_close=self.abrir_home).pack(fill="both", expand=True)

    def abrir_home(self):
        self.destroy()
        Home(self.master).pack(fill="both", expand=True)
