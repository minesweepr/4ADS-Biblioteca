import tkinter as tk
import autenticacao
import estilo
from tkinter import ttk

class TelaLogin(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, bg=estilo.BG)
        self.on_success = on_success
        self._build()
    
    def _build(self):
        wrapper = tk.Frame(self, bg=estilo.BG, width=350, height=500)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")
        wrapper.pack_propagate(False)

        # TODO: logo aq, igual no figma

        tk.Label(wrapper, text="Biblioteca Acadêmica", font=estilo.F_TITULO, fg=estilo.BRANCO, bg=estilo.BG).pack(pady=28)

        # parte interna card
        card = tk.Frame(wrapper, bg=estilo.CARD, padx=40, pady=35)
        card.pack(fill="x",)
        
        tk.Label(card, text="Login", font=estilo.F_SUBTITULO, fg=estilo.BRANCO, bg=estilo.CARD).pack(pady=(0, 25))
        
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
        self.btn_entrar = estilo.botao(card, bg=estilo.ACCENT, command=self._entrar, text="Entrar")
        self.btn_entrar.pack(fill="x", pady=(20, 0))

        # erros
        self.msg_erro = tk.Label(card, text="", font=estilo.F_PEQUENO, fg=estilo.DANGER, bg=estilo.CARD)
        self.msg_erro.pack(pady=(10, 0))

        # cadastro
        ## TODO: redirect funcional
        self.redirect_cadastro = tk.Label(card, text="Não tem uma conta? Cadastre-se.", font=estilo.F_PEQUENO, fg=estilo.ACCENT, bg=estilo.CARD)
        self.redirect_cadastro.pack()

    def _entrar(self):
        self.msg_erro.config(text="")
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get()

        if not email or not senha:
            self.msg_erro.config(text="Preencha todos os campos.")
            return
        try:
            usuario_logado = autenticacao.login(email, senha)
        except RuntimeError as exc:
                self.msg_erro.config(text=str(exc))
                return
        except ValueError as exc:
                self.msg_erro.config(text=str(exc))
                return

        if usuario_logado is None:
            self.msg_erro.config(text="Usuário não cadastrado.")
            return
        
        self.on_success(usuario_logado)