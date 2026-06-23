import tkinter as tk
from datetime import datetime

import estilo as st
import bdd

class Emprestimo(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        bdd.emprestimo_atrasado()

        self.configure(bg=st.BG)

        self.usuario = self.master.usuario_logado

        titulo = tk.Label(self, text="Empréstimos Ativos", font=st.F_SUBTITULO, fg=st.BRANCO, bg=st.BG)
        titulo.pack(padx=35, pady=20, anchor="w")

        st.separador(self).pack(fill="x", padx=35)

        self.cards = []

        # pega só emprestimos do usuário logado
        if self.usuario["tipo"] == "bibliotecario":
            ## ATIVOS
            self.emprestimos = bdd.emprestimo_listar_todos_status("ATIVO")

            print([dict(e) for e in self.emprestimos])
            self.livros = bdd.livro_listar_todos()
            self.criar_cards()

            ## ATRASADOS
            tk.Label(self, text="Empréstimos Atrasados", font=st.F_SUBTITULO, fg=st.BRANCO, bg=st.BG).pack(padx=35, pady=20, anchor="w")
            st.separador(self).pack(fill="x", padx=35)
            self.emprestimos = bdd.emprestimo_listar_todos_status("ATRASADO")

            print([dict(e) for e in self.emprestimos])
            self.livros = bdd.livro_listar_todos()
            self.criar_cards()

            ## FINALIZADOS
            tk.Label(self, text="Empréstimos Finalizados", font=st.F_SUBTITULO, fg=st.BRANCO, bg=st.BG).pack(padx=35, pady=20, anchor="w")
            st.separador(self).pack(fill="x", padx=35)
            self.emprestimos = bdd.emprestimo_listar_todos_status("FINALIZADO")
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

            dias_restantes = (data_prevista.date() - datetime.now().date()).days

            card = tk.Frame(self, bg=st.CARD, height=83, cursor="hand2")
            card.pack(fill="x", pady=15,padx=40)

            # lado esquerdo
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
                tk.Label(frame_esquerdo, text=f"Emprestado para {emprestimo['id_aluno']}", fg=st.APAGADO, bg=st.CARD, font=st.F_PEQUENO).pack(side="left") # TODO: mudar esse id pra nome msm

                # lado direito
                frame_direito = tk.Frame(card, bg=st.CARD)
                frame_direito.pack(side="right", padx=15, pady=10, anchor="e")
            
                tk.Label(frame_direito, text=f"Empréstimo: {data_emprestimo.strftime("%d/%m/%Y")}", fg=cor_retorno, bg=st.CARD, font=st.F_PEQUENO).pack(anchor="e")
                tk.Label(frame_direito, text=f"Previsão de retorno: {data_prevista.strftime("%d/%m/%Y")}", fg=cor_retorno, bg=st.CARD, font=st.F_PEQUENO).pack(anchor="e")
                tk.Label(frame_direito, text=texto_retorno, fg=st.ACCENT, bg=st.CARD, font=st.F_PEQUENO).pack(anchor="e")
            else:
                # lado esquerdo
                texto_retorno = f"(Atrasado há {abs(dias_restantes)} dias)" if atrasado else f"(Faltam {dias_restantes} dias)"
                
                tk.Label(frame_esquerdo, text=f"Previsão de retorno: {data_prevista.strftime("%d/%m/%Y")}", fg=st.APAGADO, bg=st.CARD, font=st.F_PEQUENO).pack(side="left")
                tk.Label(frame_esquerdo, text=texto_retorno, fg=cor_retorno, bg=st.CARD, font=st.F_PEQUENO).pack(side="left")
                            
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