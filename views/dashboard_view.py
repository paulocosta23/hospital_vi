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

        self.configure(fg_color=("#F7F9FC", "#111827"))

        # ✅ ALTERADO (antes era transparent)
        container = ctk.CTkFrame(self, fg_color=("#F7F9FC", "#111827"))
        container.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(container, width=230, fg_color=("white", "#1F2937"))
        sidebar.pack(side="left", fill="y")

        divider = ctk.CTkFrame(container, width=2, fg_color=("#E5E7EB", "#374151"))
        divider.pack(side="left", fill="y")

        # ✅ ALTERADO (antes era transparent)
        self.content = ctk.CTkFrame(container, fg_color=("#F7F9FC", "#111827"))
        self.content.pack(side="left", fill="both", expand=True)

        self.sidebar = sidebar

        ctk.CTkLabel(
            sidebar,
            text="Clínica",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#111827", "#E5E7EB")
        ).pack(pady=(25, 20))

        tipo = self.usuario["tipo"]

        if tipo == "recepcionista":
            menu_items = [
                ("📅 Agenda", self.show_agenda),
                ("👥 Pacientes", self.show_pacientes),
                ("Sair", master.show_login),
            ]

        elif tipo == "medico":
            menu_items = [
                ("📅 Minha agenda", self.show_agenda),
                ("🩺 Atendimentos", self.show_atendimentos),
                ("📊 Relatórios", self.show_relatorios),
                ("Sair", master.show_login),
            ]

        elif tipo == "admin":
            menu_items = [
                ("📅 Agenda", self.show_agenda),
                ("👥 Pacientes", self.show_pacientes),
                ("🩺 Atendimentos", self.show_atendimentos),
                ("📊 Relatórios", self.show_relatorios),
                ("👤 Usuários", self.show_users),
                ("Sair", master.show_login),
            ]

        self.botoes_menu = []

        for text, command in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                height=42,
                fg_color="transparent",
                text_color=("#374151", "#D1D5DB"),
                hover_color=("#F3F4F6", "#374151"),
                anchor="w",
                command=lambda c=command, b=None: None
            )
            btn.pack(fill="x", padx=15, pady=4)

            btn.configure(command=lambda c=command, b=btn: self.handle_click(c, b))

            self.botoes_menu.append(btn)

        self.btn_tema = ctk.CTkButton(
            sidebar,
            text="🌙 Modo escuro",
            fg_color="transparent",
            text_color=("#374151", "#D1D5DB"),
            hover_color=("#F3F4F6", "#374151"),
            command=self.toggle_theme
        )
        self.btn_tema.pack(fill="x", padx=15, pady=(20, 5))

        ctk.CTkLabel(
            sidebar,
            text=f"{self.usuario['nome']}",
            text_color=("#6B7280", "#9CA3AF")
        ).pack(side="bottom", pady=20)

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
            b.configure(fg_color="transparent")

        botao.configure(fg_color=("#F3F4F6", "#374151"))

        self.botao_ativo = botao
        func()

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear()

        ctk.CTkLabel(
            self.content,
            text=f"Bem-vindo, {self.usuario['nome']}",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=("#111827", "#E5E7EB")
        ).pack(anchor="w", padx=40, pady=40)

        ctk.CTkLabel(
            self.content,
            text="Selecione uma opção no menu",
            font=ctk.CTkFont(size=14),
            text_color=("#6B7280", "#9CA3AF")
        ).pack(anchor="w", padx=40)

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