import tkinter as tk
from datetime import datetime, timedelta

import estilo as st
import bdd

from telas.emprestimo import Emprestimo
from telas.form_livro import FormLivro

class LivroDetalhe(tk.Frame):
    def __init__(self, master, livro_id, on_close):
        super().__init__(master)

        self.on_close = on_close

        self.livro = bdd.livro_listar_um(livro_id)

        self.configure(bg=st.BG)

        self.botao_voltar = tk.Button( self, text="🡰 Voltar", bg=st.BG, fg=st.BRANCO, bd=0, activebackground=st.BG, activeforeground=st.BRANCO, font=st.F_SUBTITULO, command=self._fechar, cursor="hand2" )
        self.botao_voltar.pack( padx=35, pady=32, anchor="w" )

        self.main_frame = tk.Frame( self, bg=st.BG )
        self.main_frame.pack( fill="both", expand=True, padx=(65, 165) )

        card = tk.Frame( self.main_frame, width=223, height=290, bg="#D9D9D9" )
        card.pack( side="left", anchor="n", padx=(0, 30) )
        card.pack_propagate(False)

        # Textos da direita
        self.text_frame = tk.Frame( self.main_frame, bg=st.BG )
        self.text_frame.pack( side="left", anchor="n", fill="both", expand=True )

        texto_disponivel = ( "Disponível" if self.livro["disponivel"] else "Indisponível" )

        cor_disponivel = ( st.SUCCESS if self.livro["disponivel"] else st.DANGER )

        disponibilidade = tk.Label( self.text_frame, text=texto_disponivel, fg=cor_disponivel, bg=st.BG, font=st.F_PEQUENO )
        disponibilidade.pack(anchor="w")

        nome = tk.Label( self.text_frame, text=self.livro["titulo"], fg=st.BRANCO, bg=st.BG, font=st.F_SUBTITULO )
        nome.pack(anchor="w", pady=9)

        subtitulo = tk.Label( self.text_frame, text=f'Feito por {self.livro["autor"]}', fg=st.BRANCO, bg=st.BG, font=st.F_PEQUENO )
        subtitulo.pack(anchor="w")

        descricao_frame = tk.Frame( self.text_frame, bg=st.CARD )
        descricao_frame.pack( fill="x", pady=18 )

        descricao = tk.Label( descricao_frame, text=f'"{self.livro["quote"]}"', fg=st.APAGADO, bg=st.CARD, font=st.F_QUOTE, justify="left", anchor="w" )
        descricao.pack( fill="x", padx=12, pady=10 )
        
        if self.master.usuario_logado["tipo"]=="aluno":
            self.botao_alugar = st.botao(self.text_frame, st.ACCENT, self._alugar, "Alugar")
            self.botao_alugar.pack( anchor="w", pady=25 )
            self.msg_erro = tk.Label(self.text_frame, text="", fg=st.DANGER, bg=st.BG)
            self.msg_erro.pack(anchor="w")
        elif self.master.usuario_logado["tipo"]=="bibliotecario":
            self.btn_frame = tk.Frame( self.text_frame, bg=st.BG )
            self.btn_frame.pack(pady=18)

            self.botao_editar = st.botao(self.btn_frame, st.ACCENT, self._editar, "Editar")
            self.botao_editar.pack(side="left", anchor="n", pady=25, padx=15)

            self.botao_deletar = st.botao(self.btn_frame, st.DANGER, self._deletar, "Deletar")
            self.botao_deletar.pack(side="left", anchor="n", pady=25, padx=15 )
        
    def _fechar(self):
        self.destroy()
        self.on_close()

    def _alugar(self):
        try:
            id_aluno = self.master.usuario_logado["id"]
            id_livro = self.livro["id"]
            data_prevista = ( datetime.now() + timedelta(days=7) ).isoformat()

            alugado = bdd.emprestimo_novo( id_livro, id_aluno, data_prevista )
            print("Empréstimo realizado")
            print(alugado)

            self.destroy()
            Emprestimo(self.master).pack(fill="both", expand=True)

        except (RuntimeError, ValueError) as exc:
            self.msg_erro.config(text=str(exc), fg=st.DANGER)

    def _editar(self):
        self.destroy()
        FormLivro(self.master, on_close=self.on_close, livro=self.livro ).pack(fill="both", expand=True)
    
    # função deletar simples
    def _deletar(self):
        try:
            bdd.livro_deletar(self.livro["id"])
            print("Livro deletado")

            self._fechar()

        except (RuntimeError, ValueError) as exc:
            self.msg_erro.config(text=str(exc))