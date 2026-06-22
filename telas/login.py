import tkinter as tk
import autenticacao
import estilo
from tkinter import ttk

class TelaLogin(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, bg=estilo.BG)
        self.on_success = on_success
        self._modo = "login"
        self._build()
    
    def _build(self):
        wrapper = tk.Frame(self, bg=estilo.BG, width=350, height=600)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")
        wrapper.pack_propagate(False)

        # TODO: logo aq, igual no figma

        tk.Label(wrapper, text="Biblioteca Acadêmica", font=estilo.F_TITULO, fg=estilo.BRANCO, bg=estilo.BG).pack(pady=28)

        # parte interna card
        card = tk.Frame(wrapper, bg=estilo.CARD, padx=40, pady=35)
        card.pack(fill="x",)
        
        self.modo_titulo = tk.Label(card, text="Login", font=estilo.F_SUBTITULO, fg=estilo.BRANCO, bg=estilo.CARD)
        self.modo_titulo.pack(pady=(0, 25))
        
        # tudo nome (cadastro)
        self.nome_label=estilo.label_form(card, text="Nome", bg=estilo.CARD)
        #self.nome_label.pack(anchor="w")

        self.nome_entry = estilo.entry_form(card)
        #self.nome_entry.pack(fill="x", ipady=6, pady=(2, 12))
        
        # tudo email
        self.email_label=estilo.label_form(card, text="E-mail", bg=estilo.CARD)
        self.email_label.pack(anchor="w")

        self.email_entry = estilo.entry_form(card)
        self.email_entry.pack(fill="x", ipady=6, pady=(2, 12))

        # tudo senha
        self.senha_label=estilo.label_form(card, text="Senha", bg=estilo.CARD)
        self.senha_label.pack(anchor="w")

        self.senha_entry = estilo.entry_form(card, show="●")
        self.senha_entry.pack(fill="x", ipady=6, pady=(2, 0))

        # btn entrar
        self.btn_entrar = estilo.botao(card, bg=estilo.ACCENT, command=self._autenticar, text="Entrar")
        self.btn_entrar.pack(fill="x", pady=(20, 0))

        # erros
        self.msg = tk.Label(card, text="", font=estilo.F_PEQUENO, fg=estilo.DANGER, bg=estilo.CARD)
        self.msg.pack(pady=(10, 0))

        # cadastro
        self.modo_redirect = tk.Button(card, text="Não tem uma conta? Cadastre-se.", 
                                       font=estilo.F_PEQUENO, fg=estilo.ACCENT, bg=estilo.CARD, bd=0, 
                                       activebackground=estilo.CARD, activeforeground=estilo.ACCENT,
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
                self.msg.config(text="Conta criada com sucesso!", fg=estilo.SUCCESS)

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