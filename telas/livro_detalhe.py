import tkinter as tk
import estilo as st
import bdd



class LivroDetalhe(tk.Frame):
    def __init__(self, master, livro_id, on_close):
        super().__init__(master)

        self.on_close = on_close

        livro = bdd.livro_listar_um(livro_id)

        self.configure(bg=st.BG)

        # Navbar
        self.navbar = st.nav(self)

        self.botao_voltar = tk.Button( self, text="< Voltar", bg=st.BG, fg=st.BRANCO, bd=0, activebackground=st.BG, activeforeground=st.BRANCO, font=st.F_TITULO, command=self.fechar, cursor="hand2" )
        self.botao_voltar.pack( padx=35, pady=32, anchor="w" )

        self.main_frame = tk.Frame( self, bg=st.BG )
        self.main_frame.pack( fill="both", expand=True, padx=(65, 165) )

        card = tk.Frame( self.main_frame, width=223, height=290, bg="#D9D9D9" )
        card.pack( side="left", anchor="n", padx=(0, 30) )
        card.pack_propagate(False)

        # Textos da direita
        self.text_frame = tk.Frame( self.main_frame, bg=st.BG )
        self.text_frame.pack( side="left", anchor="n", fill="both", expand=True )

        texto_disponivel = ( "Disponível" if livro["disponivel"] else "Indisponível" )

        cor_disponivel = ( st.SUCCESS if livro["disponivel"] else st.DANGER )

        disponibilidade = tk.Label( self.text_frame, text=texto_disponivel, fg=cor_disponivel, bg=st.BG, font=st.F_PEQUENO )
        disponibilidade.pack(anchor="w")

        nome = tk.Label( self.text_frame, text=livro["titulo"], fg=st.BRANCO, bg=st.BG, font=st.F_TITULO )
        nome.pack(anchor="w", pady=9)

        subtitulo = tk.Label( self.text_frame, text=f'Feito por {livro["autor"]}', fg=st.APAGADO, bg=st.BG, font=st.F_PEQUENO )
        subtitulo.pack(anchor="w")

        descricao_frame = tk.Frame( self.text_frame, bg=st.APAGADO )
        descricao_frame.pack( fill="x", pady=18 )

        descricao = tk.Label( descricao_frame, text=f'"{livro["quote"]}"', fg=st.BRANCO, bg=st.APAGADO, font=("Arial", 12, "italic"), justify="left", anchor="w" )
        descricao.pack( fill="x", padx=12, pady=10 )
        
        if self.master.usuario_logado["tipo"]=="aluno":
            self.botao_alugar = st.botao(self.text_frame, st.ACCENT, None, "Alugar")
            self.botao_alugar.pack( anchor="w", pady=25 )
        elif self.master.usuario_logado["tipo"]=="bibliotecario":
            self.btn_frame = tk.Frame( self.text_frame, bg=st.BG )
            self.btn_frame.pack(pady=18)

            self.botao_editar = st.botao(self.btn_frame, st.ACCENT, None, "Editar")
            self.botao_editar.pack(side="left", anchor="n", pady=25, padx=15)

            self.botao_deletar = st.botao(self.btn_frame, st.DANGER, None, "Deletar")
            self.botao_deletar.pack(side="left", anchor="n", pady=25, padx=15 )
        
    def fechar(self):
        self.destroy()
        self.on_close()