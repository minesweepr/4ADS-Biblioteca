import tkinter as tk
from datetime import datetime

import estilo as st
import bdd

class Emprestimo(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg=st.BG)

        self.usuario = self.master.usuario_logado

        titulo = tk.Label(self, text="Empréstimos Ativos", font=st.F_SUBTITULO, fg=st.BRANCO, bg=st.BG)
        titulo.pack(padx=35, pady=20, anchor="w")

        linha = tk.Frame(self, bg=st.BORDA, height=1)
        linha.pack(fill="x", padx=35)

        self.cards = []

        # pega só emprestimos do usuário logado
        if self.usuario["tipo"] == "bibliotecario":
            self.emprestimos = bdd.emprestimo_listar_todos()
        else:
            self.emprestimos = bdd.emprestimo_listar_por_usuario(self.usuario["id"])
            
        print([dict(e) for e in self.emprestimos])

        self.livros = bdd.livro_listar_todos()

        self.criar_cards()

    def criar_cards(self):
        for emprestimo in self.emprestimos:

            livro = next(
                (l for l in self.livros if l["id"] == emprestimo["id_livro"]),
                None
            )

            nome = livro["titulo"] if livro else "Livro não encontrado"

            data_prevista = datetime.fromisoformat(emprestimo["data_previsao_retorno"])

            dias_restantes = (data_prevista - datetime.now()).days

            card = tk.Frame(self, bg=st.CARD, height=83, cursor="hand2")
            card.pack(fill="x", pady=15,padx=40)

            # lado esquerdo
            esquerdo = tk.Frame(card, bg=st.CARD)
            esquerdo.pack(pady=10, padx=10, anchor="w", side="left")

            nome_livro = tk.Label(esquerdo, text=nome, fg=st.BRANCO, bg=st.CARD, font=st.F_TEXTO)
            nome_livro.pack(anchor="w")

            previsao_frame = tk.Frame(esquerdo, bg=st.CARD)
            previsao_frame.pack(anchor="w")

            data = tk.Label(previsao_frame, text="Previsão de retorno: ", fg=st.ACCENT, bg=st.CARD, font=st.F_PEQUENO)
            data.pack(side="left")

            dias = tk.Label(previsao_frame, text=f"(Faltam {dias_restantes} dias)", fg=st.ACCENT, bg=st.CARD, font=st.F_PEQUENO)
            dias.pack(side="left")

            # lado direito
            self.botao = st.botao(card, st.ACCENT, lambda eid=emprestimo["id"]: self.devolucao_livro(eid), "Retornar")
            self.botao.pack(side="right", padx=10)

            self.cards.append(card)

    def devolucao_livro(self, id_emprestimo):
        try:
            bdd.emprestimo_devolver(id_emprestimo)
            print(f"Empréstimo {id_emprestimo} devolvido")

            for c in self.cards:
                c.destroy()

            self.cards.clear()
            self.emprestimos = bdd.emprestimo_listar_por_usuario(self.usuario["id"])
            self.criar_cards()

        except Exception as e:
            print(f"Erro ao devolver empréstimo {id_emprestimo}: {e}")