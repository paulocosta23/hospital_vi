import customtkinter as ctk

from views.agenda_view import AgendaView
from views.patients_view import PatientsView
from views.doctor_view import DoctorView
from views.users_view import UsersView
from views.reports_view import ReportsView



class DashboardView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.usuario = usuario
        self.botao_ativo = None
        self.modo = "Light"

        # CORES
        self.bg = "#123E6D"
        self.sidebar_bg = "#081B49"
        self.topbar_bg = "#243F91"
        self.accent = "#2EC7E6"
        self.card_bg = "#F8F9FA"

        self.configure(fg_color=self.bg)

        # BARRA SUPERIOR
        self.topbar = ctk.CTkFrame(
            self,
            height=40,
            fg_color=self.topbar_bg,
            corner_radius=0
        )
        self.topbar.pack(fill="x", side="top")

        # CONTAINER
        container = ctk.CTkFrame(
            self,
            fg_color=self.bg,
            corner_radius=0
        )
        container.pack(fill="both", expand=True)

        # SIDEBAR
        sidebar = ctk.CTkFrame(
            container,
            width=250,
            fg_color=self.sidebar_bg,
            corner_radius=0
        )
        sidebar.pack(side="left", fill="y")

        self.sidebar = sidebar

        # CONTEÚDO
        self.content = ctk.CTkFrame(
            container,
            fg_color=self.bg,
            corner_radius=0
        )
        self.content.pack(side="left", fill="both", expand=True)

        # LOGO/TÍTULO
        ctk.CTkLabel(
            sidebar,
            text="🏥",
            font=ctk.CTkFont(size=50)
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            sidebar,
            text="Clínica Médica",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.accent
        ).pack()

        ctk.CTkLabel(
            sidebar,
            text="Sistema de gestão",
            text_color="#D1D5DB",
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 30))

        tipo = self.usuario["tipo"]

        if tipo == "recepcionista":
            menu_items = [
                ("📅 Agenda", self.show_agenda),
                ("👥 Pacientes", self.show_pacientes),
                ("🚪 Sair", master.show_login),
            ]

        elif tipo == "medico":
            menu_items = [
                ("📅 Minha agenda", self.show_agenda),
                ("🩺 Atendimentos", self.show_atendimentos),
                ("📊 Relatórios", self.show_relatorios),
                ("🚪 Sair", master.show_login),
            ]

        elif tipo == "admin":
            menu_items = [
                ("📅 Agenda", self.show_agenda),
                ("👥 Pacientes", self.show_pacientes),
                ("🩺 Atendimentos", self.show_atendimentos),
                ("📊 Relatórios", self.show_relatorios),
                ("👤 Usuários", self.show_users),
                ("🚪 Sair", master.show_login),
            ]

        self.botoes_menu = []

        for text, command in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                height=45,
                corner_radius=12,
                fg_color=self.sidebar_bg,
                hover_color="#184E91",
                text_color="white",
                anchor="w",
                border_width=0
            )

            btn.pack(fill="x", padx=15, pady=4)

            btn.configure(
                command=lambda c=command, b=btn: self.handle_click(c, b)
            )

            self.botoes_menu.append(btn)

        self.btn_tema = ctk.CTkButton(
            sidebar,
            text="🌙 Modo escuro",
            height=45,
            corner_radius=12,
            fg_color=self.sidebar_bg,
            hover_color="#184E91",
            text_color="white",
            command=self.toggle_theme
        )

        self.btn_tema.pack(
            fill="x",
            padx=15,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            sidebar,
            text=self.usuario["nome"],
            text_color="#9CA3AF",
            font=ctk.CTkFont(size=13)
        ).pack(side="bottom", pady=25)

        self.show_welcome()

    def toggle_theme(self):
        if self.modo == "Light":
            self.modo = "Dark"
            ctk.set_appearance_mode("Dark")
            self.btn_tema.configure(text="☀️ Modo claro")
        else:
            self.modo = "Light"
            ctk.set_appearance_mode("Light")
            self.btn_tema.configure(text="🌙 Modo escuro")

    def handle_click(self, func, botao):

        for b in self.botoes_menu:
            b.configure(
                fg_color=self.sidebar_bg,
                text_color="white"
            )

        botao.configure(
            fg_color=self.accent,
            text_color="#081B49"
        )

        self.botao_ativo = botao
        func()

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear()

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_bg,
            corner_radius=25
        )

        card.place(
            relx=0.5,
            rely=0.5,
            relwidth = 0.5,
            relheight=0.5,
            anchor="center"
        )

        ctk.CTkLabel(
            card,
            text=f"Bem-vindo, {self.usuario['nome']}",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color="#0F172A"
        ).pack(pady=(80, 20))

        ctk.CTkLabel(
            card,
            text="Selecione uma opção no menu lateral",
            font=ctk.CTkFont(size=15),
            text_color="#64748B"
        ).pack()

        linha = ctk.CTkFrame(
            card,
            width=120,
            height=4,
            fg_color=self.accent
        )

        linha.pack(pady=20)

    def show_agenda(self):
        self.clear()
        AgendaView(self.content)

    def show_pacientes(self):
        self.clear()
        PatientsView(self.content)

    def show_atendimentos(self):
        self.clear()
        DoctorView(self.content)

    def show_relatorios(self):
        self.clear()
        ReportsView(self.content)

    def show_users(self):
        self.clear()
        UsersView(self.content)