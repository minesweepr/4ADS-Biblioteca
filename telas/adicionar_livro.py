import tkinter as tk
import estilo as st
import bdd

class AdicionarLivro(tk.Frame):
    def __init__(self, master, on_close):
        super().__init__(master)

        self.on_close = on_close

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

        title = tk.Label( self.text_frame, text="Informações do Livro", fg=st.BRANCO, bg=st.BG, font=st.F_TITULO )
        title.pack(anchor="w", pady=0)

        # tudo nome
        self.nome_label=st.label_form(self.text_frame, text="Nome*", bg=st.CARD)
        self.nome_label.pack(anchor="w")

        self.nome_entry = st.entry_form(self.text_frame)
        self.nome_entry.pack(fill="x", ipady=6, pady=(2, 12))

        # tudo autor
        self.autor_label=st.label_form(self.text_frame, text="autor*", bg=st.CARD)
        self.autor_label.pack(anchor="w")

        self.autor_entry = st.entry_form(self.text_frame)
        self.autor_entry.pack(fill="x", ipady=6, pady=(2, 12))

        # tudo quote
        self.quote_label=st.label_form(self.text_frame, text="quote", bg=st.CARD)
        self.quote_label.pack(anchor="w")

        self.quote_entry = st.entry_form(self.text_frame)
        self.quote_entry.pack(fill="x", ipady=6, pady=(2, 12))

        # adicionar
        self.botao = st.botao(self.text_frame, st.ACCENT, None, "Adicionar")
        self.botao.pack( anchor="w", pady=25 )
        
        self.msg_erro = tk.Label(self.text_frame, text="", fg="red", bg=st.BG)
        self.msg_erro.pack(anchor="w")

    def fechar(self):
        self.destroy()
        self.on_close()

    