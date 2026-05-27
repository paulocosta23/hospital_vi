import customtkinter as ctk


class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_login = on_login
        self.show_password = False

        # ===== FUNDO =====
        self.configure(fg_color=("white", "#1F2937")
)

        # ===== CONTAINER =====
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # ========= ESQUERDA =========
        left = ctk.CTkFrame(container, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)

        left_inner = ctk.CTkFrame(left, fg_color="transparent")
        left_inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            left_inner,
            text="✚",
            font=ctk.CTkFont(size=60, weight="bold"),
            text_color="#2563EB"
        ).pack(pady=(0, 12))

        ctk.CTkLabel(
            left_inner,
            text="Clínica Médica",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#111827"
        ).pack()

        ctk.CTkLabel(
            left_inner,
            text="Sistema de gestão do consultório",
            font=ctk.CTkFont(size=14),
            text_color="#6B7280"
        ).pack(pady=(8, 0))

        # ========= LINHA DIVISÓRIA =========
        divider = ctk.CTkFrame(
            container,
            width=2,              # linha visível
            fg_color="#E5E7EB"
        )
        divider.pack(side="left", fill="y")

        # ========= DIREITA =========
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        right_inner = ctk.CTkFrame(right, fg_color="transparent")
        right_inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            right_inner,
            text="Acessar sistema",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#111827"
        ).pack(pady=(0, 30))

        self.entry_user = ctk.CTkEntry(
            right_inner,
            placeholder_text="Usuário",
            width=320,
            height=48,
            fg_color="white",
            border_color="#E5E7EB",
            corner_radius=12
        )
        self.entry_user.pack(pady=12)

        password_frame = ctk.CTkFrame(
            right_inner,
            fg_color="white",
            corner_radius=12,
            height=48
        )
        password_frame.pack(pady=12, fill="x")
        password_frame.pack_propagate(False)

        self.entry_password = ctk.CTkEntry(
            password_frame,
            placeholder_text="Senha",
            show="●",
            fg_color="transparent",
            border_width=0
        )
        self.entry_password.pack(side="left", padx=12, expand=True, fill="both")

        self.eye = ctk.CTkLabel(
            password_frame,
            text="👁",
            text_color="#6B7280",
            cursor="hand2"
        )
        self.eye.pack(side="right", padx=12)
        self.eye.bind("<Button-1>", self.toggle_password)

        ctk.CTkButton(
            right_inner,
            text="Entrar",
            width=320,
            height=48,
            fg_color="#2563EB",
            hover_color="#1E3A8A",
            corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.login
        ).pack(pady=28)

    def toggle_password(self, event=None):
        self.show_password = not self.show_password
        self.entry_password.configure(show="" if self.show_password else "●")

    def login(self):
        self.on_login()