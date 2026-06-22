import customtkinter as ctk
from controllers.usuario_controller import login
from PIL import Image
from tkinter import messagebox
from .theme import get_color


class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_login = on_login
        self.show_password = False

        self.configure(fg_color=get_color("login_bg"))

        # ── Painel esquerdo (brand) ─────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color=get_color("login_left"), corner_radius=0)
        left.place(relx=0, rely=0, relwidth=0.46, relheight=1)

        # Círculo decorativo superior-esquerdo
        ctk.CTkFrame(
            left, width=320, height=320,
            fg_color=get_color("login_circle1"), corner_radius=160,
        ).place(x=-120, y=-120)

        # Círculo decorativo inferior-direito
        ctk.CTkFrame(
            left, width=180, height=180,
            fg_color=get_color("login_circle2"), corner_radius=90,
        ).place(relx=1, rely=1, x=-60, y=-60)

        # Conteúdo centralizado — limpo e minimalista
        brand_frame = ctk.CTkFrame(left, fg_color="transparent")
        brand_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo ou nome
        try:
            logo = Image.open("assets/modo_escuro.png")
            logo_image = ctk.CTkImage(dark_image=logo, size=(500, 206))
            ctk.CTkLabel(brand_frame, text="", image=logo_image).pack(pady=(0, 20))
        except Exception:
            ctk.CTkLabel(
                brand_frame, text="Clínica Médica",
                font=ctk.CTkFont(size=52, weight="bold"),
                text_color="#FFFFFF",
            ).pack(pady=(0, 12))

        # Traço azul divisor
        ctk.CTkFrame(
            brand_frame, height=2, width=40,
            fg_color=get_color("login_divider"), corner_radius=1,
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            brand_frame, text="SISTEMA DE GESTÃO",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#4A7FD4",
        ).pack()

        # ── Linha vertical divisória ────────────────────────────────────────
        ctk.CTkFrame(self, width=1, fg_color=get_color("border")).place(
            relx=0.46, rely=0.1, relheight=0.8
        )

        # ── Painel direito (formulário) ─────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=get_color("login_right"), corner_radius=0)
        right.place(relx=0.46, rely=0, relwidth=0.54, relheight=1)

        # Card de login
        card = ctk.CTkFrame(
            right, width=400, height=480,
            fg_color=get_color("login_card"),
            corner_radius=18,
            border_width=1,
            border_color=get_color("border"),
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Barra de topo azul
        ctk.CTkFrame(card, height=4, fg_color="#2D5FA8", corner_radius=0).pack(fill="x")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.52, anchor="center")

        # Cabeçalho
        ctk.CTkLabel(
            inner, text="Acessar Sistema",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=get_color("login_card_text"),
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            inner, text="Entre com suas credenciais",
            font=ctk.CTkFont(size=12),
            text_color=get_color("login_card_subtitle"),
        ).pack(pady=(0, 28))

        # ── Campo: Usuário ──────────────────────────────────────────────────
        self._field_label(inner, "Usuário")

        self.entry_user = ctk.CTkEntry(
            inner,
            placeholder_text="Digite seu usuário",
            width=320, height=46,
            fg_color=get_color("surface"),
            border_color=get_color("border"),
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
        )
        self.entry_user.pack(pady=(0, 16))

        # ── Campo: Senha ────────────────────────────────────────────────────
        self._field_label(inner, "Senha")

        password_frame = ctk.CTkFrame(
            inner,
            fg_color=get_color("surface"),
            corner_radius=10,
            height=46, width=320,
            border_width=1,
            border_color=get_color("border"),
        )
        password_frame.pack(pady=(0, 28))
        password_frame.pack_propagate(False)

        self.entry_password = ctk.CTkEntry(
            password_frame,
            placeholder_text="Digite sua senha",
            show="●",
            fg_color="transparent",
            border_width=0,
            font=ctk.CTkFont(size=13),
        )
        self.entry_password.pack(side="left", padx=(12, 0), expand=True, fill="both")

        self.eye = ctk.CTkLabel(
            password_frame, text="👁",
            cursor="hand2",
            font=ctk.CTkFont(size=16),
        )
        self.eye.pack(side="right", padx=12)
        self.eye.bind("<Button-1>", self.toggle_password)

        # Bind Enter
        self.entry_user.bind("<Return>", lambda e: self.login())
        self.entry_password.bind("<Return>", lambda e: self.login())

        # ── Botão Entrar ────────────────────────────────────────────────────
        ctk.CTkButton(
            inner,
            text="Entrar",
            width=320, height=48,
            fg_color=get_color("button"),
            hover_color=get_color("button_hover"),
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.login,
        ).pack()

    # ── Helpers ────────────────────────────────────────────────────────────

    def _field_label(self, parent, text: str):
        lbl_frame = ctk.CTkFrame(parent, fg_color="transparent", width=320)
        lbl_frame.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(
            lbl_frame, text=text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=get_color("login_card_subtitle"),
        ).pack(anchor="w")

    def toggle_password(self, event=None):
        self.show_password = not self.show_password
        self.entry_password.configure(show="" if self.show_password else "●")

    def login(self):
        try:
            username = self.entry_user.get().strip()
            senha    = self.entry_password.get().strip()

            if not username or not senha:
                messagebox.showwarning("Atenção", "Preencha usuário e senha")
                return

            usuario = login(username, senha)

            if usuario == "usuario_nao_existe":
                messagebox.showerror("Erro", "Usuário não encontrado")
                self.entry_user.focus()

            elif usuario == "Senha_incorreta":
                messagebox.showerror("Erro", "Senha incorreta")
                self.entry_password.focus()

            elif usuario:
                self.usuario = (usuario[1], usuario[2])
                self.on_login(self.usuario)

            else:
                messagebox.showerror("Erro", "Erro inesperado no login")

        except Exception:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", "Erro interno do sistema")