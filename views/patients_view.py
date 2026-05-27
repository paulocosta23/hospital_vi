import customtkinter as ctk


class PatientsView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=("white", "#1F2937")
)

        self.pacientes = []
        self.filtro_nome = ""  # ✅ ADICIONADO

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
        else:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"

    # ================= UI =================
    def render(self):
        for w in self.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(
            header,
            text="Pacientes",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Novo paciente",
            fg_color="#2563EB",
            command=self.popup
        ).pack(side="right")

        # ✅ CAMPO DE BUSCA (ADICIONADO)
        busca_frame = ctk.CTkFrame(self, fg_color="transparent")
        busca_frame.pack(fill="x", padx=30, pady=(0, 10))

        self.input_busca = ctk.CTkEntry(
            busca_frame,
            placeholder_text="Buscar paciente pelo nome"
        )
        self.input_busca.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkButton(
            busca_frame,
            text="Buscar",
            command=self.buscar
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            busca_frame,
            text="Limpar",
            fg_color="#9CA3AF",
            command=self.limpar_busca
        ).pack(side="left", padx=5)

        self.lista = ctk.CTkScrollableFrame(self)
        self.lista.pack(fill="both", expand=True, padx=30, pady=10)

        self.render_lista()

    # ================= BUSCA =================
    def buscar(self):
        self.filtro_nome = self.input_busca.get().lower()
        self.render_lista()

    def limpar_busca(self):
        self.filtro_nome = ""
        self.input_busca.delete(0, "end")
        self.render_lista()

    # ================= LISTA =================
    def render_lista(self):
        for w in self.lista.winfo_children():
            w.destroy()

        pacientes = self.pacientes

        # ✅ APLICA FILTRO (ADICIONADO)
        if self.filtro_nome:
            pacientes = [
                p for p in pacientes
                if self.filtro_nome in p["nome"].lower()
            ]

        if not pacientes:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum paciente cadastrado",
                text_color="#6B7280"
            ).pack(pady=40)
            return

        for p in pacientes:
            self.card(p)

    # ================= CARD =================
    def card(self, p):
        card = ctk.CTkFrame(self.lista, fg_color="#FFFFFF", corner_radius=12)
        card.pack(fill="x", pady=8)

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=10)

        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(info, text=p["nome"],
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"CPF: {p['cpf']} | Tel: {p['telefone']}",
            text_color="#6B7280"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Tipo: {p['tipo']} | Plano: {p['plano']}",
            text_color="#6B7280"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Cart.: {p.get('carteirinha','-')} | Nasc: {p.get('nascimento','-')}",
            text_color="#6B7280"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Endereço: {p.get('endereco','-')}",
            text_color="#9CA3AF",
            wraplength=450
        ).pack(anchor="w")

        ctk.CTkButton(
            container,
            text="Editar",
            width=90,
            fg_color="#9CA3AF",
            command=lambda p=p: self.popup(p)
        ).pack(side="right")

    # ================= POPUP =================
    def popup(self, paciente=None):
        popup = ctk.CTkToplevel(self)
        popup.geometry("400x600")
        popup.grab_set()

        frame = ctk.CTkFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="Paciente",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        nome = ctk.CTkEntry(frame, placeholder_text="Nome")
        nome.pack(fill="x", pady=6)

        cpf = ctk.CTkEntry(frame, placeholder_text="CPF")
        cpf.pack(fill="x", pady=6)

        def mascara(event):
            valor = self.formatar_cpf(cpf.get())
            cpf.delete(0, "end")
            cpf.insert(0, valor)

        cpf.bind("<KeyRelease>", mascara)

        telefone = ctk.CTkEntry(frame, placeholder_text="Telefone")
        telefone.pack(fill="x", pady=6)

        nascimento = ctk.CTkEntry(frame, placeholder_text="Data nascimento")
        nascimento.pack(fill="x", pady=6)

        tipo = ctk.CTkOptionMenu(frame, values=["Particular", "Convênio"])
        tipo.pack(fill="x", pady=6)

        plano = ctk.CTkEntry(frame, placeholder_text="Plano")
        plano.pack(fill="x", pady=6)

        carteirinha = ctk.CTkEntry(frame, placeholder_text="Carteirinha")
        carteirinha.pack(fill="x", pady=6)

        endereco = ctk.CTkEntry(frame, placeholder_text="Endereço")
        endereco.pack(fill="x", pady=6)

        if paciente:
            nome.insert(0, paciente["nome"])
            cpf.insert(0, paciente["cpf"])
            telefone.insert(0, paciente["telefone"])
            nascimento.insert(0, paciente.get("nascimento", ""))
            tipo.set(paciente["tipo"])
            plano.insert(0, paciente["plano"])
            carteirinha.insert(0, paciente.get("carteirinha", ""))
            endereco.insert(0, paciente.get("endereco", ""))

        erro = ctk.CTkLabel(frame, text="", text_color="#DC2626")
        erro.pack()

        def salvar():
            if not nome.get():
                erro.configure(text="Nome obrigatório")
                return

            dados = {
                "nome": nome.get(),
                "cpf": cpf.get(),
                "telefone": telefone.get(),
                "nascimento": nascimento.get(),
                "tipo": tipo.get(),
                "plano": plano.get(),
                "carteirinha": carteirinha.get(),
                "endereco": endereco.get()
            }

            if paciente:
                paciente.update(dados)
            else:
                self.pacientes.append(dados)

            self.render_lista()
            popup.destroy()

        ctk.CTkButton(
            frame,
            text="Salvar",
            fg_color="#2563EB",
            command=salvar
        ).pack(pady=15)