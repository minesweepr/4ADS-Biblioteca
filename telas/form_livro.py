import tkinter as tk
import estilo as st
from bdd import livro_novo
from bdd import livro_editar

class FormLivro(tk.Frame):
    def __init__(self, master, on_close, livro=None):
        super().__init__(master)

        self.on_close = on_close
        self.livro = livro

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

        title = tk.Label( self.text_frame, text="Informações do Livro", fg=st.BRANCO, bg=st.BG, font=st.F_SUBTITULO )
        title.pack(anchor="w", pady=0)

        # tudo nome
        self.nome_label=st.label_form(self.text_frame, text="Nome*", bg=st.BG)
        self.nome_label.pack(anchor="w")

        self.nome_entry = st.entry_form(self.text_frame)
        self.nome_entry.pack(fill="x", ipady=6, pady=(2, 12))

        # tudo autor
        self.autor_label=st.label_form(self.text_frame, text="Autor*", bg=st.BG)
        self.autor_label.pack(anchor="w")

        self.autor_entry = st.entry_form(self.text_frame)
        self.autor_entry.pack(fill="x", ipady=6, pady=(2, 12))

        # tudo quote
        self.quote_label=st.label_form(self.text_frame, text="Quote", bg=st.BG)
        self.quote_label.pack(anchor="w")

        self.quote_entry = st.entry_form(self.text_frame)
        self.quote_entry.pack(fill="x", ipady=6, pady=(2, 12))

        # preencher se for editar
        if self.livro:
            self.nome_entry.insert(0, self.livro["titulo"])
            self.autor_entry.insert(0, self.livro["autor"])
            self.quote_entry.insert(0, self.livro["quote"] or "")

        # botao adicionar ou editar
        texto_botao = "Salvar" if livro else "Adicionar"
        self.botao = st.botao(self.text_frame, st.ACCENT, self._salvar, texto_botao)
        self.botao.pack( anchor="w", pady=25 )
        
        self.msg = tk.Label(self.text_frame, text="", fg=st.DANGER, bg=st.BG)
        self.msg.pack(anchor="w")

    def _fechar(self):
        self.destroy()
        self.on_close()

    # função salvar e editar 
    def _salvar(self):
        nome = self.nome_entry.get()
        autor = self.autor_entry.get()
        quote = self.quote_entry.get()

        if not nome or not autor:
            self.msg.config(text="Preencha todos os campos obrigatórios.", fg=st.DANGER)
            return
        
        try:
            if self.livro:
                livro_editar(self.livro["id"], nome, autor, quote)
                print("Livro editado")

                self.msg.config(text=f"O livro {nome} foi editado com sucesso!", fg=st.ACCENT)

            else:
                livro_novo(nome, autor, quote)
                print("Livro adicionado")
                self.msg.config(text=f"O livro {nome} foi criado com sucesso!", fg=st.ACCENT)

        except (RuntimeError, ValueError) as exc:
            self.msg_erro.config(text=str(exc))
        

        self.nome_entry.delete(0, tk.END)
        self.autor_entry.delete(0, tk.END)
        self.quote_entry.delete(0, tk.END)
        self._fechar()
