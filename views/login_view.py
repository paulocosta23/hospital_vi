import tkinter as tk
from tkinter import messagebox
from controllers.usuario_controller import login
from views.dashboard import Dashboard
from tkinter import messagebox
from controllers.usuario_controller import login
from views.dashboard import Dashboard
from views.cores import C

class LoginView:
    def __init__(self, root):
        self.root = root
        

       # self._mostrar_senha = False
    # Criando com self.
        

        self.root.title("Login")
        self.root.geometry("1100x680")
        self.root.configure(bg=C["bg_deep"])

        #self._build()

        

    # ─────────────────────────────────────────────
    # UI PRINCIPAL
    # ─────────────────────────────────────────────
    #def _build(self):
        self.raiz = tk.Frame(self.root, bg=C["bg_deep"])
        self.raiz.pack(fill=tk.BOTH, expand=True)


        # ESQUERDA
        esq = tk.Frame(self.raiz, bg=C["bg_panel"])
        esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        centro = tk.Frame(esq, bg=C["bg_panel"])
        centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(centro, text="Sistema de Gestão",
                 font=("Georgia", 28, "bold"),
                 bg=C["bg_panel"], fg=C["text_hi"]).pack()

        tk.Label(centro, text="Hospital VIP",
                 font=("Georgia", 28, "bold"),
                 bg=C["bg_panel"], fg=C["accent"]).pack()

        tk.Frame(centro, bg=C["accent"], height=2, width=160).pack(pady=20)

        tk.Label(
            centro,
            text=" ",
            font=("Helvetica", 12),
            bg=C["bg_panel"],
            fg=C["text_mid"],
            justify=tk.CENTER
        ).pack(pady=(0, 24))

        # DIREITA
        dir_ = tk.Frame(self.raiz, bg=C["bg_deep"], width=440)
        dir_.pack(side=tk.RIGHT, fill=tk.BOTH)
        dir_.pack_propagate(False)

        form = tk.Frame(dir_, bg=C["bg_deep"])
        form.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=340)

        tk.Label(form, text="Bem-vindo de volta",
                 font=("Georgia", 22, "bold"),
                 bg=C["bg_deep"], fg=C["text_hi"]).pack(anchor="w")

        tk.Label(form, text="Entre com suas credenciais.",
                 font=("Helvetica", 11),
                 bg=C["bg_deep"], fg=C["text_mid"]).pack(anchor="w", pady=(4, 24))

        # ── USUÁRIO ──
        tk.Label(form, text="USUÁRIO",
                 font=("Helvetica", 9, "bold"),
                 bg=C["bg_deep"], fg=C["text_mid"]).pack(anchor="w")

        self.usuario = tk.Entry(
            form,
            bg=C["bg_card"],
            fg=C["text_hi"],
            insertbackground=C["accent"],
            relief=tk.FLAT
        )
        self.usuario.pack(fill=tk.X, pady=(4, 10), ipady=6)

        # ── SENHA ──
        tk.Label(form, text="SENHA",
                 font=("Helvetica", 9, "bold"),
                 bg=C["bg_deep"], fg=C["text_mid"]).pack(anchor="w")

        senha_frame = tk.Frame(
            form,
            bg=C["bg_card"],
            highlightthickness=1,
            highlightbackground=C["border"]
        )
        senha_frame.pack(fill=tk.X, pady=(4, 10))

        self.senha = tk.Entry(
            senha_frame,
            bg=C["bg_card"],
            fg=C["text_hi"],
            insertbackground=C["accent"],
            relief=tk.FLAT,
            show="*"
        )
        self.senha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=6)

        btn_toggle = tk.Button(
            senha_frame,
            text="◎",
            font=("Helvetica", 12),
            bg=C["bg_card"],
            fg=C["text_lo"],  # mais suave
            activebackground=C["bg_card"],
            activeforeground=C["accent"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._toggle_senha
            )
        btn_toggle.pack(side=tk.RIGHT, padx=6)

    # Hover bem sutil
        btn_toggle.bind("<Enter>", lambda e: btn_toggle.config(fg=C["text_mid"]))
        btn_toggle.bind("<Leave>", lambda e: btn_toggle.config(fg=C["text_lo"]))
                    # BOTÃO (igual seu original estilizado)
        btn = tk.Button(
            form,
            text="Entrar  →",
            font=("Helvetica", 12, "bold"),
            bg=C["accent_dim"],
            fg=C["white"],
            activebackground=C["accent_dim"],  # evita “flash bruto”
            activeforeground=C["white"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.fazer_login
            )
        btn.pack(fill=tk.X, pady=20, ipady=10)

        # Hover suave (igual seu sistema original)
        btn.bind("<Enter>", lambda e: btn.config(bg=C["accent"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=C["accent_dim"]))

        self.status = tk.Label(
            form,
            text="",
            bg=C["bg_deep"],
            fg=C["danger"]
        )
        self.status.pack()

    def _toggle_senha(self):
    # Verifica se a senha está oculta (usando *) ou visível ("")
        if self.senha.cget('show') == '*':
            self.senha.config(show='')
            # Opcional: mudar o texto do botão para "Ocultar"
        else:
            self.senha.config(show='*')
            # Opcional: mudar o texto do botão para "Mostrar"


    def fazer_login(self):
        try:
            username = self.usuario.get().strip()
            senha = self.senha.get().strip()
            
            # Campos vazios
            if not username or not senha:
                messagebox.showwarning("Atenção", "Preencha usuário e senha")
                return
            
            usuario = login(username, senha)
            # Usuário não existe
            if usuario == "usuario_nao_existe":
                messagebox.showerror("Erro", "Usuário não encontrado")
                self.usuario.focus()

            # Senha incorreta 
            elif usuario == "Senha_incorreta":
                messagebox.showerror("Erro", "Senha incorreta")
                self.senha.delete(0, tk.END0)
                self.senha.focus()

            # Login correto
            elif usuario:
                self.raiz.destroy()
                Dashboard(self.root, usuario[1])

            # fallback (segurança extra)
            else:
                messagebox.showerror("Erro", "Erro inesperado do login")

        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", "Erro interno do sistema")