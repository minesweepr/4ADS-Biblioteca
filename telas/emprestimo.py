import tkinter as tk
from datetime import datetime

import estilo as st
import bdd
from paginacao import *

class Emprestimo(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        bdd.emprestimo_atrasado()
        self.configure(bg=st.BG)
        self.usuario = self.master.usuario_logado

        self.cards = []

        self.pagina = 0
        self.limite = 10
        self.total = 0

        self.status_filtro = tk.StringVar()
        self.status_filtro.set("ATIVO")

        titulo_frame = tk.Frame(self, bg=st.BG)
        titulo_frame.pack(fill="x", padx=35, pady=20)
        titulo_frame.grid_columnconfigure(0, weight=1)
        titulo_frame.grid_columnconfigure(1, weight=1)
        titulo_frame.grid_columnconfigure(2, weight=1)

        self.titulo_label = tk.Label(titulo_frame, text="Empréstimos Ativos", font=st.F_SUBTITULO, fg=st.BRANCO, bg=st.BG)
        self.titulo_label.grid(row=0, column=0, sticky="w")

        self.paginacao_frame = Paginacao(titulo_frame, total=self.total, limite=self.limite, pagina=self.pagina, on_change=lambda p: mudar_pagina(self, p))
        self.paginacao_frame.grid(row=0, column=1)

        if self.usuario["tipo"] == "bibliotecario":
            opcoes = ["ATIVO","ATRASADO","FINALIZADO"]

            filtro = tk.OptionMenu(titulo_frame, self.status_filtro, *opcoes, command=self.atualizar_lista)
            filtro.config(bg=st.CARD, fg=st.BRANCO, activebackground=st.BG, activeforeground=st.APAGADO, highlightthickness=1, highlightbackground=st.BORDA, bd=2, relief="raised", font=st.F_TEXTO, cursor="hand2")
            filtro["menu"].config(bg=st.CARD, fg=st.BRANCO, activebackground=st.BORDA)
            filtro.grid(row=0, column=2, sticky="e")

        st.separador(self).pack(fill="x", padx=35)

        self.carregar_dados()

        self.bind("<Configure>", self.atualizar_lista)

    def carregar_emprestimos(self):
        status = self.status_filtro.get()
        if self.usuario["tipo"] == "bibliotecario":
            self.emprestimos = bdd.emprestimo_listar_todos_status(status)

            textos = {
                "ATIVO": "Empréstimos Ativos",
                "ATRASADO": "Empréstimos Atrasados",
                "FINALIZADO": "Empréstimos Finalizados"
            }
            self.titulo_label.config(text=textos.get(status, "Empréstimos"))
        else:
            self.emprestimos = bdd.emprestimo_listar_por_usuario(self.usuario["id"])
        self.livros = bdd.livro_listar_todos()

    def criar_cards(self):
        for emprestimo in self.emprestimos:

            livro = next((l for l in self.livros if l["id"] == emprestimo["id_livro"]), None)

            nome = livro["titulo"] if livro else "Livro não encontrado"

            data_prevista = datetime.fromisoformat(emprestimo["data_previsao_retorno"])

            dias_restantes = (data_prevista.date() - datetime.now().date()).days

            card = tk.Frame(self, bg=st.CARD, height=83, cursor="hand2")
            card.pack(fill="x", pady=15, padx=40)

            esquerdo = tk.Frame(card, bg=st.CARD)
            esquerdo.pack(pady=10, padx=10, anchor="w", side="left")

            nome_livro = tk.Label(esquerdo, text=nome, fg=st.BRANCO, bg=st.CARD, font=st.F_TEXTO)
            nome_livro.pack(anchor="w")

            frame_esquerdo = tk.Frame(esquerdo, bg=st.CARD)
            frame_esquerdo.pack(anchor="w")

            atrasado = emprestimo["status"] == "ATRASADO"
            cor_retorno = st.DANGER if atrasado else st.ACCENT

            if self.usuario["tipo"] == "bibliotecario":
                data_emprestimo = datetime.fromisoformat(emprestimo["data_emprestimo"])

                texto_retorno = f"Devolvido em: {datetime.fromisoformat(emprestimo['data_retorno']).strftime('%d/%m/%Y')}" if emprestimo["data_retorno"] else ""
                tk.Label(frame_esquerdo, text=f"Emprestado para {emprestimo['id_aluno']}", fg=st.APAGADO, bg=st.CARD, font=st.F_PEQUENO).pack(side="left")

                frame_direito = tk.Frame(card, bg=st.CARD)
                frame_direito.pack(side="right", padx=15, pady=10, anchor="e")

                tk.Label(frame_direito, text=f"Empréstimo: {data_emprestimo.strftime('%d/%m/%Y')}", fg=cor_retorno, bg=st.CARD, font=st.F_PEQUENO).pack(anchor="e")
                tk.Label(frame_direito, text=f"Previsão de retorno: {data_prevista.strftime('%d/%m/%Y')}", fg=cor_retorno, bg=st.CARD, font=st.F_PEQUENO).pack(anchor="e")
                tk.Label(frame_direito, text=texto_retorno, fg=st.ACCENT, bg=st.CARD, font=st.F_PEQUENO).pack(anchor="e")
            else:
                texto_retorno = f"(Atrasado há {abs(dias_restantes)} dias)" if atrasado else f"(Faltam {dias_restantes} dias)"

                tk.Label(frame_esquerdo, text=f"Previsão de retorno: {data_prevista.strftime('%d/%m/%Y')}", fg=st.APAGADO, bg=st.CARD, font=st.F_PEQUENO).pack(side="left")
                tk.Label(frame_esquerdo, text=texto_retorno, fg=cor_retorno, bg=st.CARD, font=st.F_PEQUENO).pack(side="left")

                botao = st.botao(card, st.ACCENT, lambda eid=emprestimo["id"]: self.devolucao_livro(eid), "Retornar")
                botao.pack(side="right", padx=10)

            self.cards.append(card)

    def devolucao_livro(self, id_emprestimo):
        try:
            bdd.emprestimo_devolver(id_emprestimo)
            print(f"Empréstimo {id_emprestimo} devolvido")

            for c in self.cards:
                c.destroy()

            self.cards.clear()
            self.carregar_dados()

        except Exception as e:
            print(f"Erro ao devolver empréstimo {id_emprestimo}: {e}")

    def carregar_dados(self):
        self.carregar_emprestimos()

        self.total = len(self.emprestimos)

        inicio = self.pagina * self.limite
        fim = inicio + self.limite

        self.emprestimos = self.emprestimos[inicio:fim]

        for c in self.cards:
            c.destroy()

        self.cards.clear()

        self.criar_cards()

        atualizar_paginacao(self)

    def atualizar_lista(self, *_):
        novo_limite = self.calcular_limite()

        if novo_limite != self.limite:
            self.limite = novo_limite

        self.pagina = 0
        self.carregar_dados()

    def calcular_limite(self):
        altura_card = 90
        linhas = max(1, (self.winfo_height() - 150) // altura_card)

        return linhas