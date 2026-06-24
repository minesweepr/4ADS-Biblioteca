import tkinter as tk
import autenticacao
import estilo as st

class TelaLogin(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, bg=st.BG)
        self.on_success = on_success
        self._modo = "login"
        self._build()
    
    def _build(self):
        wrapper = tk.Frame(self, bg=st.BG, width=350, height=600)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")
        wrapper.pack_propagate(False)

        st.logo(wrapper, st.BG).pack()
        tk.Label(wrapper, text="Biblioteca Acadêmica", font=st.F_TITULO, fg=st.BRANCO, bg=st.BG).pack(pady=(25, 38))

        # parte interna card
        card = tk.Frame(wrapper, bg=st.CARD, padx=40, pady=35)
        card.pack(fill="x",)
        
        self.modo_titulo = tk.Label(card, text="Login", font=st.F_SUBTITULO, fg=st.BRANCO, bg=st.CARD)
        self.modo_titulo.pack(pady=(0, 25))
        
        # tudo nome (cadastro)
        self.nome_label=st.label_form(card, text="Nome", bg=st.CARD)
        self.nome_entry = st.entry_form(card)
        
        # tudo email
        self.email_label=st.label_form(card, text="E-mail", bg=st.CARD)
        self.email_label.pack(anchor="w")

        self.email_entry = st.entry_form(card)
        self.email_entry.pack(fill="x", ipady=6, pady=(2, 12))

        # tudo senha
        self.senha_label=st.label_form(card, text="Senha", bg=st.CARD)
        self.senha_label.pack(anchor="w")

        self.senha_entry = st.entry_form(card, show="●")
        self.senha_entry.pack(fill="x", ipady=6, pady=(2, 0))

        # btn entrar
        self.btn_entrar = st.botao(card, bg=st.ACCENT, command=self._autenticar, text="Entrar")
        self.btn_entrar.pack(fill="x", pady=(20, 0))

        # erros
        self.msg = tk.Label(card, text="", font=st.F_PEQUENO, fg=st.DANGER, bg=st.CARD)
        self.msg.pack(pady=(10, 0))

        # cadastro
        self.modo_redirect = tk.Button(card, text="Não tem uma conta? Cadastre-se.", 
                                       font=st.F_PEQUENO, fg=st.ACCENT, bg=st.CARD, bd=0, 
                                       activebackground=st.CARD, activeforeground=st.ACCENT,
                                       command=self._modo_troca, cursor="hand2")
        self.modo_redirect.pack()

    def _modo_troca(self):
        self._modo = "cadastro" if self._modo == "login" else "login"
        self.msg.config(text="")

        if self._modo == "cadastro":
            self.modo_titulo.config(text="Cadastro")
            self.btn_entrar.config(text="Criar conta")
            self.modo_redirect.config(text="Já tem uma conta? Entre.")
            self.nome_label.pack(anchor="w", before=self.email_label)
            self.nome_entry.pack(fill="x", ipady=6, pady=(2, 12), before=self.email_label)
        else:
            self.modo_titulo.config(text="Login")
            self.btn_entrar.config(text="Entrar")
            self.modo_redirect.config(text="Não tem uma conta? Cadastre-se.")
            self.nome_label.pack_forget()
            self.nome_entry.pack_forget()


    def _autenticar(self):
        self.msg.config(text="")
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get()

        if not email or not senha:
            self.msg.config(text="Preencha todos os campos.")
            return
        
        if self._modo == "cadastro":
            nome = self.nome_entry.get()
            if not nome:
                self.msg.config(text="Preencha todos os campos.")
                return
            
            try:
                autenticacao.cadastro(nome, email, senha)
                self.msg.config(text="Conta criada com sucesso!", fg=st.SUCCESS)

                self.nome_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.senha_entry.delete(0, tk.END) 
            except RuntimeError as exc:
                self.msg.config(text=str(exc))
                return
            except ValueError as exc:
                self.msg.config(text=str(exc))
                return

        else:
            try:
                usuario_logado = autenticacao.login(email, senha)
            except RuntimeError as exc:
                self.msg.config(text=str(exc))
                return
            except ValueError as exc:
                self.msg.config(text=str(exc))
                return

            if usuario_logado is None:
                self.msg.config(text="Usuário não cadastrado.")
                return
        
            self.on_success(usuario_logado)