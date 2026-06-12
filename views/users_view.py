import customtkinter as ctk
from .theme import get_color


class UsersView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.bg = get_color("bg")
        self.panel = get_color("panel")
        self.card_color = get_color("card")
        self.primary = get_color("accent")
        self.green = get_color("success")
        self.text = get_color("text")
        self.muted = get_color("text_secondary")

        self.configure(fg_color=self.bg)

        self.usuarios = []

        header = ctk.CTkFrame(self, fg_color=self.panel, corner_radius=18, height=70)
        header.pack(fill="x", padx=18, pady=(18, 10))

        ctk.CTkLabel(
            header,
            text="👤 Gestão de Usuários",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.text,
        ).place(x=20, y=18)

        ctk.CTkLabel(
            header,
            text="Controle de acessos do sistema",
            font=ctk.CTkFont(size=12),
            text_color=self.muted,
        ).place(x=20, y=42)

        ctk.CTkButton(
            header,
            text="+ Novo usuário",
            fg_color=self.green,
            hover_color=get_color("success_hover"),
            corner_radius=12,
            command=lambda: self.popup(),
        ).pack(side="right", padx=15, pady=18)

        self.lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.lista.pack(fill="both", expand=True, padx=18, pady=10)

        self.render()

    def formatar_cpf(self, texto):
        nums = "".join(filter(str.isdigit, texto))[:11]
        if len(nums) <= 3:
            return nums
        elif len(nums) <= 6:
            return f"{nums[:3]}.{nums[3:]}"
        elif len(nums) <= 9:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:]}"
        else:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"

    def ocultar_cpf(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))  # remove formatação anterior
        return f"{cpf[:3]}.***.***.{cpf[-2:]}"

    def render(self):
        for w in self.lista.winfo_children():
            w.destroy()

        if not self.usuarios:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum usuário cadastrado",
                text_color=self.muted,
            ).pack(pady=60)
            return

        for u in self.usuarios:
            self.card(u)

    def card(self, u):
        card = ctk.CTkFrame(
            self.lista,
            fg_color=self.card_color,
            corner_radius=16,
            border_width=1,
            border_color=get_color("border"),
        )
        card.pack(fill="x", pady=8)

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=12)

        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(
            info,
            text=u["nome"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.text,
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"CPF: {self.ocultar_cpf(u['cpf'])}",
            text_color=self.muted,
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Login: {u['login']}",
            text_color=get_color("text_secondary"),
        ).pack(anchor="w")

        role_color = self.primary
        if u["tipo"] == "admin":
            role_color = get_color("purple")
        elif u["tipo"] == "medico":
            role_color = self.green

        ctk.CTkLabel(
            container,
            text=u["tipo"].upper(),
            text_color=role_color,
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(side="right", padx=10)

        ctk.CTkButton(
            container,
            text="Editar",
            width=80,
            height=30,
            fg_color=self.primary,
            hover_color=get_color("accent_hover"),
            corner_radius=10,
            command=lambda u=u: self.popup(u),
        ).pack(side="right")

    def popup(self, usuario=None):
        popup = ctk.CTkToplevel(self)
        popup.geometry("420x560")
        popup.grab_set()
        popup.configure(fg_color=self.panel)

        frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            frame,
            text="Usuário",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.text,
        ).pack(pady=10)

        nome = ctk.CTkEntry(frame, placeholder_text="Nome")
        nome.pack(fill="x", pady=6)

        self.cpf = ctk.CTkEntry(frame, placeholder_text="CPF")
        self.cpf.pack(fill="x", pady=6)

        login = ctk.CTkEntry(frame, placeholder_text="Login")
        login.pack(fill="x", pady=6)

        senha = ctk.CTkEntry(frame, placeholder_text="Senha", show="●")
        senha.pack(fill="x", pady=6)

        confirmar = ctk.CTkEntry(frame, placeholder_text="Confirmar senha", show="●")
        confirmar.pack(fill="x", pady=6)

        tipo = ctk.CTkOptionMenu(frame, values=["admin", "medico", "recepcionista"])
        tipo.pack(fill="x", pady=6)

        def mascara(event):
            valor = self.formatar_cpf(self.cpf.get())
            self.cpf.delete(0, "end")
            self.cpf.insert(0, valor)

        self.cpf.bind("<KeyRelease>", mascara)


        if usuario:
            nome.insert(0, usuario["nome"])
            self.cpf.insert(0, usuario["cpf"])
            login.insert(0, usuario["login"])
            senha.insert(0, usuario["senha"])
            confirmar.insert(0, usuario["senha"])
            tipo.set(usuario["tipo"])

        erro = ctk.CTkLabel(frame, text="", text_color=get_color("danger"))
        erro.pack()

        def salvar():
            if senha.get() != confirmar.get():
                erro.configure(text="Senhas não coincidem")
                return

            dados = {
                "nome": nome.get(),
                "cpf": self.cpf.get(),
                "login": login.get(),
                "senha": senha.get(),
                "tipo": tipo.get(),
            }

            if usuario:
                usuario.update(dados)
            else:
                self.usuarios.append(dados)

            self.render()
            popup.destroy()

        ctk.CTkButton(
            frame,
            text="Salvar",
            fg_color=self.green,
            hover_color=get_color("success_hover"),
            command=salvar,
        ).pack(pady=15)