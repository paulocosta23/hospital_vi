import customtkinter as ctk
from .theme import get_color
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
        self.modo = "Dark"

        # Cores iniciais (podem ser atualizadas em tempo de execução)
        # Observação: usamos `get_color` para obter cores atuais do tema
        self.bg = get_color("bg")
        self.sidebar_bg = get_color("sidebar")
        self.topbar_bg = get_color("topbar")
        self.accent = get_color("accent")
        self.card_bg = get_color("card")

        self.configure(fg_color=self.bg)

        self.topbar = ctk.CTkFrame(
            self,
            height=40,
            fg_color=self.topbar_bg,
            corner_radius=0,
        )

        self.topbar.pack(fill="x", side="top")

        container = ctk.CTkFrame(self, fg_color=self.bg, corner_radius=0)
        container.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(
            container,
            width=250,
            fg_color=self.sidebar_bg,
            corner_radius=0,
        )

        sidebar.pack(side="left", fill="y")
        self.sidebar = sidebar

        self.content = ctk.CTkFrame(
            container,
            fg_color=self.bg,
            corner_radius=0,
        )
        self.content.pack(side="left", fill="both", expand=True)

        # Armazenar referências dos labels da sidebar para atualizações posteriores
        # Não recriamos esses labels ao trocar tema; usamos configure()
        self.lbl_logo = ctk.CTkLabel(
            sidebar,
            text="🏥",
            font=ctk.CTkFont(size=50),
            text_color=get_color("accent"),
        )
        self.lbl_logo.pack(pady=(35, 5))

        self.lbl_titulo = ctk.CTkLabel(
            sidebar,
            text="Clínica Médica",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=get_color("accent"),
        )
        self.lbl_titulo.pack()

        self.lbl_subtitulo = ctk.CTkLabel(
            sidebar,
            text="Sistema de gestão",
            text_color=get_color("text_secondary"),
            font=ctk.CTkFont(size=12),
        )
        self.lbl_subtitulo.pack(pady=(0, 30))

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
        else:
            menu_items = [
                ("📅 Agenda", self.show_agenda),
                ("👥 Pacientes", self.show_pacientes),
                ("🩺 Atendimentos", self.show_atendimentos),
                ("📊 Relatórios", self.show_relatorios),
                ("👤 Usuários", self.show_users),
                ("🚪 Sair", master.show_login),
            ]

        # Criar botões do menu usando get_color() para garantir cores corretas
        self.botoes_menu = []

        for text, command in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                height=45,
                corner_radius=12,
                fg_color=get_color("sidebar"),
                hover_color=get_color("accent_hover"),
                text_color=get_color("menu_text"),
                anchor="w",
                border_width=0,
            )
            btn.pack(fill="x", padx=15, pady=4)
            btn.configure(command=lambda c=command, b=btn: self.handle_click(c, b))
            self.botoes_menu.append(btn)

        # Botão para alternar o tema. Usa get_color() para manter em sincronia
        self.btn_tema = ctk.CTkButton(
            sidebar,
            text="🌙 Modo escuro",
            height=45,
            corner_radius=12,
            fg_color=get_color("sidebar"),
            hover_color=get_color("accent_hover"),
            text_color=get_color("menu_text"),
            command=self.toggle_theme,
        )
        self.btn_tema.pack(fill="x", padx=15, pady=(20, 10))

        # Label do usuário na parte inferior da sidebar (referência salva)
        self.lbl_usuario = ctk.CTkLabel(
            sidebar,
            text=self.usuario["nome"],
            text_color=get_color("text_secondary"),
            font=ctk.CTkFont(size=13),
        )
        self.lbl_usuario.pack(side="bottom", pady=25)

        self.show_welcome()

    def toggle_theme(self):
        # Alterna o modo utilizando o estado real do CTk (get_appearance_mode)
        # Isso evita divergência entre self.modo e o estado real do widget
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.modo = "Light"
            self.btn_tema.configure(text="🌙 Modo escuro")
        else:
            ctk.set_appearance_mode("Dark")
            self.modo = "Dark"
            self.btn_tema.configure(text="☀️ Modo claro")

        # Após alternar o modo, atualizar cores de todos os widgets existentes
        self.atualizar_cores()

    def handle_click(self, func, botao):
        # Atualiza visual dos botões do menu ao clicar
        for b in self.botoes_menu:
            b.configure(fg_color=get_color("sidebar"), text_color=get_color("text"))

        botao.configure(fg_color=get_color("accent"), text_color=get_color("bg"))

        self.botao_ativo = botao
        func()

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear()

        # Ao criar novos widgets, usar get_color() para cores atuais do tema
        card = ctk.CTkFrame(
            self.content,
            fg_color=get_color("accent"),
            corner_radius=25,
        )
        card.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.7, anchor="center")

        conteudo = ctk.CTkFrame(card, fg_color="transparent")
        conteudo.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            conteudo,
            text=f"Bem-vindo, {self.usuario['nome']}",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color=get_color("text"),
        ).pack(pady=(0, 15))

        ctk.CTkLabel(
            conteudo,
            text="Selecione uma opção no menu lateral",
            font=ctk.CTkFont(size=20),
            text_color=get_color("text_secondary"),
        ).pack()

        linha = ctk.CTkFrame(
            conteudo,
            width=120,
            height=4,
            fg_color=get_color("accent"),
        )
        linha.pack(pady=(20, 0))

    def show_agenda(self):
        self.clear()
        # Views criadas devem obter cores por get_color internamente
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

    def atualizar_cores(self):
        """
        Atualiza as cores de todos os widgets existentes sem recriá-los.
        Chamado após trocar o tema para refletir mudanças em tempo real.
        """
        # Atualiza variáveis de cor locais
        self.bg = get_color("bg")
        self.sidebar_bg = get_color("sidebar")
        self.topbar_bg = get_color("topbar")
        self.accent = get_color("accent")
        self.card_bg = get_color("card")

        # Atualiza frames principais
        self.configure(fg_color=self.bg)
        self.topbar.configure(fg_color=self.topbar_bg)
        self.sidebar.configure(fg_color=self.sidebar_bg)
        self.content.configure(fg_color=self.bg)

        # Atualiza botões do menu
        for b in self.botoes_menu:
            if b is self.botao_ativo:
                b.configure(fg_color=self.accent, text_color=get_color("bg"))
            else:
                b.configure(
                    fg_color=self.sidebar_bg,
                    hover_color=get_color("accent_hover"),
                    text_color=get_color("menu_text"),
                )

        # Atualiza botão de tema
        self.btn_tema.configure(
            fg_color=self.sidebar_bg,
            hover_color=get_color("accent_hover"),
            text_color=get_color("menu_text"),
        )

        # Atualiza labels da sidebar (referências previamente salvas)
        try:
            self.lbl_logo.configure(text_color=get_color("accent"))
            self.lbl_titulo.configure(text_color=get_color("accent"))
            self.lbl_subtitulo.configure(text_color=get_color("text_secondary"))
            self.lbl_usuario.configure(text_color=get_color("text_secondary"))
        except AttributeError:
            # Em caso de alguma referência não existir, ignoramos (defensivo)
            pass
        