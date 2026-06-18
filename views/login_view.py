import customtkinter as ctk
from controllers.usuario_controller import login
from tkinter import messagebox
from .theme import get_color


class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_login = on_login
        self.show_password = False

        self.configure(fg_color=get_color("login_bg"))

        self.bg_circle1 = ctk.CTkFrame(
            self,
            width=300,
            height=300,
            fg_color=get_color("login_circle1"),
            corner_radius=150,
        )
        self.bg_circle1.place(x=-100, y=-100)

        self.bg_circle2 = ctk.CTkFrame(
            self,
            width=200,
            height=200,
            fg_color=get_color("login_circle2"),
            corner_radius=100,
        )
        self.bg_circle2.place(relx=1, rely=1, x=-200, y=-200)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=40)

        left = ctk.CTkFrame(container, fg_color=get_color("login_left"))
        left.pack(side="left", fill="both", expand=True)

        left_inner = ctk.CTkFrame(
            left,
            fg_color=get_color("login_left_inner"),
            corner_radius=20,
        )
        left_inner.place(relx=0.5, rely=0.5, anchor="center")

        content = ctk.CTkFrame(left_inner, fg_color="transparent")
        content.pack(padx=40, pady=40)

        # glow = ctk.CTkLabel(
        #     content,
        #     text="●",
        #     font=ctk.CTkFont(size=200),
        #     text_color=get_color("info"),
        # )
        # glow.place(relx=0.5, rely=0.2, anchor="center")

        logo = Image.open("assets/modo_escuro.png")
        logo_image = ctk.CTkImage(dark_image=logo, size=(750, 300))

        ctk.CTkLabel(content, text="" ,image=logo_image).pack(pady=(5, 5))

        divider = ctk.CTkFrame(
            content,
            height=2,
            width=120,
            fg_color=get_color("login_divider"),
        )
        divider.pack(pady=(10, 15))

        ctk.CTkLabel(
            content,
            text="Sistema inteligente para gestão\nrápida e eficiente",
            font=ctk.CTkFont(size=14),
            text_color=get_color("login_subtitle"),
            justify="center",
            wraplength=280,
        ).pack()

        right = ctk.CTkFrame(container, fg_color=get_color("login_right"))
        right.pack(side="right", fill="both", expand=True)

        decor_top = ctk.CTkFrame(
            right,
            width=200,
            height=200,
            fg_color=get_color("login_decor_top"),
            corner_radius=100,
        )
        decor_top.place(x=450, y=-80)

        decor_bottom = ctk.CTkFrame(
            right,
            width=250,
            height=250,
            fg_color=get_color("login_decor_bottom"),
            corner_radius=140,
        )
        decor_bottom.place(x=350, y=500)

        card = ctk.CTkFrame(
            right,
            width=420,
            height=450,
            fg_color=get_color("login_card"),
            corner_radius=20,
            border_width=2,
            border_color=get_color("border"),
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        right_inner = ctk.CTkFrame(card, fg_color="transparent")
        right_inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            right_inner,
            text="Acessar Sistema",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=get_color("login_card_text"),
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            right_inner,
            text="Entre com suas credenciais",
            font=ctk.CTkFont(size=14),
            text_color=get_color("login_card_subtitle"),
        ).pack(pady=(0, 20))

        self.entry_user = ctk.CTkEntry(
            right_inner,
            placeholder_text="👤 Usuário",
            width=300,
            height=45,
            fg_color=get_color("surface"),
            border_color=get_color("border"),
            corner_radius=10,
        )
        self.entry_user.pack(pady=8)

        password_frame = ctk.CTkFrame(
            right_inner,
            fg_color=get_color("surface"),
            corner_radius=10,
            height=45,
        )
        password_frame.pack(pady=8, fill="x")
        password_frame.pack_propagate(False)

        self.entry_password = ctk.CTkEntry(
            password_frame,
            placeholder_text="🔒 Senha",
            show="●",
            fg_color="transparent",
            border_width=0,
        )
        self.entry_password.pack(side="left", padx=10, expand=True, fill="both")

        self.eye = ctk.CTkLabel(password_frame, text="👁", cursor="hand2")
        self.eye.pack(side="right", padx=10)
        self.eye.bind("<Button-1>", self.toggle_password)

        ctk.CTkButton(
            right_inner,
            text="Entrar",
            width=300,
            height=45,
            fg_color=get_color("button"),
            hover_color=get_color("button_hover"),
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.login,
        ).pack(pady=(15, 10))

    def toggle_password(self, event=None):
        self.show_password = not self.show_password
        self.entry_password.configure(show="" if self.show_password else "●")

    def login(self):
        try:
            username = self.entry_user.get().strip()
            senha = self.entry_password.get().strip()
            
            # Campos vazios
            if not username or not senha:
                messagebox.showwarning("Atenção", "Preencha usuário e senha")
                return
            
            usuario = login(username, senha)
            # Usuário não existe
            if usuario == "usuario_nao_existe":
                messagebox.showerror("Erro", "Usuário não encontrado")
                self.entry_user.focus()

            # Senha incorreta 
            elif usuario == "Senha_incorreta":
                messagebox.showerror("Erro", "Senha incorreta")
                self.entry_password.focus()

            # Login correto
            elif usuario:
                self.usuario = (usuario[1], usuario[2])
                print(self.usuario)

                self.on_login(self.usuario)
               

            # fallback (segurança extra)
            else:
                messagebox.showerror("Erro", "Erro inesperado do login")

        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", "Erro interno do sistema")