import tkinter as tk
import math
import estilo as st

# funcoes auxiliares
def mudar_pagina(view, pagina):
    view.pagina = pagina
    view.carregar_dados()
    view.paginacao_frame.atualizar(total=view.total, limite=view.limite, pagina=view.pagina)

def atualizar_paginacao(view):
    view.paginacao_frame.atualizar(total=view.total, limite=view.limite, pagina=view.pagina)

# componente
class Paginacao(tk.Frame):
    def __init__(self, master, total, limite, pagina, on_change, bg=None):
        if bg is None:
            bg = st.BG

        super().__init__(master, bg=bg)
        self.total = total
        self.limite = limite
        self.pagina = pagina
        self.on_change = on_change

        self.total_paginas = max(1, math.ceil(total / limite))
        self.render()

    def atualizar(self, total=None, limite=None, pagina=None):
        if total is not None:
            self.total = total
        if limite is not None:
            self.limite = limite
        if pagina is not None:
            self.pagina = pagina

        self.total_paginas = max(1, math.ceil(self.total / self.limite))
        if self.pagina >= self.total_paginas:
            self.pagina = self.total_paginas - 1

        self.render()

    def gerar_paginas(self):
        total = self.total_paginas
        atual = self.pagina
        if total <= 7:
            return list(range(total))
        
        paginas = [0]
        if atual > 3:
            paginas.append("...")

        start = max(1, atual - 1)
        end = min(total - 1, atual + 2)

        for i in range(start, end):
            paginas.append(i)

        if atual < total - 4:
            paginas.append("...")

        paginas.append(total - 1)
        return paginas

    def render(self):
        for w in self.winfo_children(): w.destroy()

        tk.Button(self, text="🡸", font=st.F_PAG, fg=st.ACCENT, bg=self["bg"], bd=0, command=lambda: self.on_change(max(0, self.pagina - 1)) ).pack(side="left", padx=8, pady=4)
        for item in self.gerar_paginas():
            if item == "...":
                tk.Label(self, text="...", fg=st.BORDA, bg=self["bg"], font=st.F_BTN).pack(side="left", padx=6)
                continue
            is_selected = (item == self.pagina)
            tk.Button( self, text=str(item + 1), font=st.F_BTN, fg=(st.ACCENT if is_selected else st.BORDA), bg=self["bg"], bd=0, activebackground=self["bg"], command=lambda p=item: self.on_change(p) ).pack(side="left", padx=8)
        tk.Button( self, text="🡺", font=st.F_PAG, fg=st.ACCENT, bg=self["bg"], bd=0, command=lambda: self.on_change(min(self.total_paginas - 1, self.pagina + 1)) ).pack(side="left", padx=8, pady=4)