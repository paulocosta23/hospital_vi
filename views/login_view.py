import customtkinter as ctk


class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_login = on_login
        self.show_password = False

      # ===== FUNDO =====
        self.configure(fg_color="#1E3A8A")



 # ===== CAMADA DECORATIVA =====
        self.bg_circle1 = ctk.CTkFrame(self, width=300, height=300,
                                       fg_color="#3B82F6", corner_radius=150)
        self.bg_circle1.place(x=-100, y=-100)

        self.bg_circle2 = ctk.CTkFrame(self, width=200, height=200,
                                       fg_color="#2563EB", corner_radius=100)
        self.bg_circle2.place(relx=1, rely=1, x=-200, y=-200)

     
        # ===== NTAICONER =====
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=40)

       
  # ========= ESQUERDA =========
        left = ctk.CTkFrame(container, fg_color="#0F172A")  # fundo escuro bonito
        left.pack(side="left", fill="both", expand=True)

        left_inner = ctk.CTkFrame(
            left,
            fg_color="#111827",        # efeito de card
            corner_radius=20
        )
        left_inner.place(relx=0.5, rely=0.5, anchor="center")

# Ajuste interno do card
        content = ctk.CTkFrame(left_inner, fg_color="transparent")
        content.pack(padx=40, pady=40)

# "Glow" atrás do ícone (forma decorativa)
        glow = ctk.CTkLabel(
            content,
            text="●",
            font=ctk.CTkFont(size=200),
            text_color="#0EA5E9"
        )
        glow.place(relx=0.5, rely=0.2, anchor="center")

# Ícone principal
        ctk.CTkLabel(
            content,
            text="✚",
            font=ctk.CTkFont(size=130, weight="bold"),
            text_color="#22D3EE"
        ).pack(pady=(10, 20))

# Título
        ctk.CTkLabel(
                content,
                text="Clínica Médica",
                font=ctk.CTkFont(size=30, weight="bold"),
                text_color="white"
                ).pack(pady=(5, 5))

# Linha decorativa
        divider = ctk.CTkFrame(content, height=2, width=120, fg_color="#22D3EE")
        divider.pack(pady=(10, 15))

# Subtítulo
        ctk.CTkLabel(
            content,
            text="Sistema inteligente para gestão\nrápida e eficiente",
            font=ctk.CTkFont(size=14),
            text_color="#BAE6FD",
            justify="center",
            wraplength=280
            ).pack()

# ========= DIVISÃO =========
        divider = ctk.CTkFrame(container, width=1, fg_color="#93C5FD")
        divider.pack(side="left", fill="y", padx=20)

        
# ========= DIREITA =========
        right = ctk.CTkFrame(
                    container,
                    fg_color="#114B7B",
                    corner_radius=20, 
                    width= 600, 
                    height= 800
                )
        right.pack(side="right")

        right_inner = ctk.CTkFrame(right, fg_color="transparent")
        right_inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
                    right_inner,
                    text="Acessar sistema",
            font=ctk.CTkFont(size=35, weight="bold"),
                    text_color="#000000"
                ).pack(pady=(0, 30))

        self.entry_user = ctk.CTkEntry(
                    right_inner,
                    placeholder_text="Usuário",
                    width=320,
                    height=48,
                    fg_color="white",
                    border_color="#000000",
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