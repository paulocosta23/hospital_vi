import customtkinter as ctk


class UsersView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=("white", "#1F2937")
)

        self.usuarios = []

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(
            header,
            text="Usuários",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Novo usuário",
            fg_color="#2563EB",
            command=lambda: self.popup()
        ).pack(side="right")

        self.lista = ctk.CTkScrollableFrame(self)
        self.lista.pack(fill="both", expand=True, padx=30, pady=10)

        self.render()

    # ================= CPF =================
    def formatar_cpf(self, texto):
        nums = ''.join(filter(str.isdigit, texto))[:11]

        if len(nums) <= 3:
            return nums
        elif len(nums) <= 6:
            return f"{nums[:3]}.{nums[3:]}"
        elif len(nums) <= 9:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:]}"
        return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"

    def ocultar_cpf(self, cpf):
        nums = ''.join(filter(str.isdigit, cpf))
        if len(nums) < 11:
            return cpf
        return f"{nums[:3]}.***.***-{nums[-2:]}"

    # ================= LISTA =================
    def render(self):
        for w in self.lista.winfo_children():
            w.destroy()

        if not self.usuarios:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum usuário cadastrado",
                text_color="#6B7280"
            ).pack(pady=40)
            return

        for u in self.usuarios:
            self.card(u)

    # ================= CARD =================
    def card(self, u):
        card = ctk.CTkFrame(self.lista, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8)

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=12)

        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(info, text=u["nome"],
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        ctk.CTkLabel(info,
                     text=f"CPF: {self.ocultar_cpf(u['cpf'])}",
                     text_color="#6B7280").pack(anchor="w")

        ctk.CTkLabel(info,
                     text=f"Login: {u['login']}",
                     text_color="#374151").pack(anchor="w")

        ctk.CTkLabel(info,
                     text=f"Tipo: {u['tipo']}",
                     text_color="#2563EB").pack(anchor="w")

        ctk.CTkButton(
            container,
            text="Editar",
            width=90,
            fg_color="#9CA3AF",
            command=lambda u=u: self.popup(u)
        ).pack(side="right")

    # ================= POPUP =================
    def popup(self, usuario=None):
        popup = ctk.CTkToplevel(self)
        popup.geometry("420x560")
        popup.grab_set()

        frame = ctk.CTkFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="Usuário",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        nome = ctk.CTkEntry(frame, placeholder_text="Nome")
        nome.pack(fill="x", pady=6)

        cpf = ctk.CTkEntry(frame, placeholder_text="CPF")
        cpf.pack(fill="x", pady=6)

        login = ctk.CTkEntry(frame, placeholder_text="Login")
        login.pack(fill="x", pady=6)

        # ===== SENHA =====
        senha = ctk.CTkEntry(frame, placeholder_text="Senha", show="●")
        senha.pack(fill="x", pady=6)

        eye1 = ctk.CTkLabel(
            senha,
            text="👁",
            cursor="hand2",
            fg_color="transparent",
            font=ctk.CTkFont(size=11)
        )
        eye1.place(relx=0.94, rely=0.5, anchor="e", relheight=0.6)

        # ===== CONFIRMAR =====
        confirmar = ctk.CTkEntry(frame, placeholder_text="Confirmar senha", show="●")
        confirmar.pack(fill="x", pady=6)

        eye2 = ctk.CTkLabel(
            confirmar,
            text="👁",
            cursor="hand2",
            fg_color="transparent",
            font=ctk.CTkFont(size=11)
        )
        eye2.place(relx=0.94, rely=0.5, anchor="e", relheight=0.6)

        # TOGGLE
        def toggle(entry):
            if entry.cget("show") == "":
                entry.configure(show="●")
            else:
                entry.configure(show="")

        eye1.bind("<Button-1>", lambda e: toggle(senha))
        eye2.bind("<Button-1>", lambda e: toggle(confirmar))

        tipo = ctk.CTkOptionMenu(
            frame,
            values=["admin", "medico", "recepcionista"]
        )
        tipo.pack(fill="x", pady=6)

        def mascara(event):
            valor = self.formatar_cpf(cpf.get())
            cpf.delete(0, "end")
            cpf.insert(0, valor)

        cpf.bind("<KeyRelease>", mascara)

        if usuario:
            nome.insert(0, usuario["nome"])
            cpf.insert(0, usuario["cpf"])
            login.insert(0, usuario["login"])
            senha.insert(0, usuario["senha"])
            confirmar.insert(0, usuario["senha"])
            tipo.set(usuario["tipo"])

        erro = ctk.CTkLabel(frame, text="", text_color="#DC2626")
        erro.pack()

        def salvar():
            if senha.get() != confirmar.get():
                erro.configure(text="As senhas não coincidem")
                return

            dados = {
                "nome": nome.get(),
                "cpf": cpf.get(),
                "login": login.get(),
                "senha": senha.get(),
                "tipo": tipo.get()
            }

            if usuario:
                usuario.update(dados)
            else:
                self.usuarios.append(dados)

            self.render()
            popup.destroy()

        ctk.CTkButton(frame, text="Salvar", command=salvar).pack(pady=15)