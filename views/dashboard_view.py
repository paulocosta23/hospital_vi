import customtkinter as ctk
from .theme import get_color
from views.agenda_view import AgendaView
from views.patients_view import PatientsView
from views.doctor_view import DoctorView
from views.configuracoes_view import ConfiguracoesView
from views.reports_view import ReportsView


# Rótulos de cargo exibidos abaixo do nome do usuário, conforme o tipo salvo no banco
CARGOS = {
    "admin": "ADMINISTRADOR",
    "atendente": "ATENDENTE",
    "medico": "MÉDICO",
}


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.usuario = usuario
        self.botao_ativo = None
        self.modo = "Dark"
        self.btn_sair = None  # referência separada pois tem estilo próprio (danger)

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
            width=270,
            fg_color=self.sidebar_bg,
            corner_radius=0,
        )

        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self.sidebar = sidebar

        self.content = ctk.CTkFrame(
            container,
            fg_color=self.bg,
            corner_radius=0,
        )
        self.content.pack(side="left", fill="both", expand=True)

        # ----- Cabeçalho da sidebar (logo + título) -----
        cabecalho = ctk.CTkFrame(sidebar, fg_color="transparent")
        cabecalho.pack(fill="x", pady=(30, 20))
        self.cabecalho = cabecalho

        self.logo_box = ctk.CTkFrame(
            cabecalho,
            width=56,
            height=56,
            corner_radius=16,
            fg_color=get_color("accent"),
        )
        self.logo_box.pack(pady=(0, 12))
        self.logo_box.pack_propagate(False)

        self.lbl_logo = ctk.CTkLabel(
            self.logo_box,
            text="+",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF",
        )
        self.lbl_logo.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_titulo = ctk.CTkLabel(
            cabecalho,
            text="Clínica Médica",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=get_color("text"),
        )
        self.lbl_titulo.pack()

        self.lbl_subtitulo = ctk.CTkLabel(
            cabecalho,
            text="SISTEMA DE GESTÃO",
            text_color=get_color("accent"),
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.lbl_subtitulo.pack(pady=(2, 0))

        # Linha divisória abaixo do cabeçalho
        self.divisor_topo = ctk.CTkFrame(sidebar, height=1, fg_color=get_color("border"))
        self.divisor_topo.pack(fill="x", padx=20, pady=(20, 15))

        tipo = self.usuario[0]

        if tipo == "atendente":
            menu_items = [
                ("📅", "Agenda", self.show_agenda),
                ("👥", "Pacientes", self.show_pacientes),
            ]
        elif tipo == "medico":
            menu_items = [
                ("📅", "Minha agenda", self.show_agenda),
                ("🩺", "Atendimentos", self.show_atendimentos),
                ("📊", "Relatórios", self.show_relatorios),
            ]
        else:
            menu_items = [
                ("📅", "Agenda", self.show_agenda),
                ("👥", "Pacientes", self.show_pacientes),
                ("🩺", "Atendimentos", self.show_atendimentos),
                ("📊", "Relatórios", self.show_relatorios),
                ("⚙️", "Configurações", self.show_configuracoes),
            ]

        # Área de menu (não cresce; fica logo abaixo do cabeçalho)
        menu_area = ctk.CTkFrame(sidebar, fg_color="transparent")
        menu_area.pack(fill="x")

        # Criar botões do menu usando get_color() para garantir cores corretas
        self.botoes_menu = []

        for icone, texto, command in menu_items:
            btn = ctk.CTkButton(
                menu_area,
                text=f"  {icone}   {texto}",
                height=45,
                corner_radius=10,
                fg_color=get_color("sidebar"),
                hover_color=get_color("accent_hover"),
                text_color=get_color("menu_text"),
                font=ctk.CTkFont(size=14),
                anchor="w",
                border_width=0,
            )
            btn.pack(fill="x", padx=15, pady=4)
            btn.configure(command=lambda c=command, b=btn: self.handle_click(c, b))
            self.botoes_menu.append(btn)

        # Espaço flexível para empurrar o rodapé até o fim da sidebar
        espacador = ctk.CTkFrame(sidebar, fg_color="transparent")
        espacador.pack(fill="both", expand=True)

        # ----- Rodapé da sidebar: tema, sair e usuário -----
        rodape = ctk.CTkFrame(sidebar, fg_color="transparent")
        rodape.pack(side="bottom", fill="x")
        self.rodape = rodape

        self.divisor_rodape = ctk.CTkFrame(rodape, height=1, fg_color=get_color("border"))
        self.divisor_rodape.pack(fill="x", padx=20, pady=(0, 15))

        # Switch para alternar tema (substitui o antigo botão)
        tema_frame = ctk.CTkFrame(rodape, fg_color="transparent")
        tema_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.tema_frame = tema_frame

        self.lbl_tema = ctk.CTkLabel(
            tema_frame,
            text="🌙  Modo escuro",
            text_color=get_color("text"),
            font=ctk.CTkFont(size=13),
        )
        self.lbl_tema.pack(side="left")

        self.switch_var = ctk.StringVar(value="on")
        self.switch_tema = ctk.CTkSwitch(
            tema_frame,
            text="",
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
            progress_color=get_color("accent"),
            command=self.toggle_theme,
            width=40,
        )
        self.switch_tema.pack(side="right")
        # Estado inicial do switch reflete o modo padrão (Dark)
        self.switch_tema.select()

        # Botão "Sair" com destaque vermelho (danger), abaixo do switch de tema
        self.btn_sair = ctk.CTkButton(
            rodape,
            text="  ⏻   Sair",
            height=45,
            corner_radius=10,
            fg_color="transparent",
            hover_color=get_color("danger"),
            text_color=get_color("danger"),
            font=ctk.CTkFont(size=14),
            anchor="w",
            border_width=0,
            command=master.show_login,
        )
        self.btn_sair.pack(fill="x", padx=15, pady=(0, 15))

        # Cartão do usuário no rodapé (avatar + nome + cargo)
        usuario_card = ctk.CTkFrame(rodape, fg_color="transparent")
        usuario_card.pack(fill="x", padx=15, pady=(5, 20))
        self.usuario_card = usuario_card

        inicial = self.usuario[1][0].upper() if self.usuario[1] else "?"

        self.avatar = ctk.CTkFrame(
            usuario_card,
            width=40,
            height=40,
            corner_radius=20,
            fg_color=get_color("accent"),
        )
        self.avatar.pack(side="left")
        self.avatar.pack_propagate(False)

        self.lbl_avatar = ctk.CTkLabel(
            self.avatar,
            text=inicial,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#FFFFFF",
        )
        self.lbl_avatar.place(relx=0.5, rely=0.5, anchor="center")

        textos_usuario = ctk.CTkFrame(usuario_card, fg_color="transparent")
        textos_usuario.pack(side="left", padx=(10, 0), fill="x", expand=True)

        self.lbl_usuario = ctk.CTkLabel(
            textos_usuario,
            text=self.usuario[1],
            text_color=get_color("text"),
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.lbl_usuario.pack(fill="x")

        self.lbl_cargo = ctk.CTkLabel(
            textos_usuario,
            text=CARGOS.get(tipo, tipo.upper()),
            text_color=get_color("text_secondary"),
            font=ctk.CTkFont(size=10),
            anchor="w",
        )
        self.lbl_cargo.pack(fill="x")

        self.show_welcome()

    def toggle_theme(self):
        # Alterna o modo utilizando o estado real do CTk (get_appearance_mode)
        # Isso evita divergência entre self.modo e o estado real do widget
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.modo = "Light"
            self.lbl_tema.configure(text="🌙  Modo escuro")
        else:
            ctk.set_appearance_mode("Dark")
            self.modo = "Dark"
            self.lbl_tema.configure(text="☀️  Modo claro")

        # Mantém o switch sincronizado com o modo atual
        if self.modo == "Dark":
            self.switch_tema.select()
        else:
            self.switch_tema.deselect()

        # Após alternar o modo, atualizar cores de todos os widgets existentes
        self.atualizar_cores()

    def handle_click(self, func, botao):
        # Atualiza visual dos botões do menu ao clicar
        for b in self.botoes_menu:
            b.configure(fg_color=get_color("sidebar"), text_color=get_color("text"))

        botao.configure(fg_color=get_color("accent"), text_color="#FFFFFF")

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
            fg_color=get_color("card"),
            corner_radius=25,
            border_width=1,
            border_color=get_color("border"),
        )
        card.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.7, anchor="center")

        conteudo = ctk.CTkFrame(card, fg_color="transparent")
        conteudo.place(relx=0.5, rely=0.5, anchor="center")

        icone_box = ctk.CTkFrame(
            conteudo,
            width=90,
            height=90,
            corner_radius=24,
            fg_color=get_color("accent"),
            border_width=2,
            border_color=get_color("accent_hover"),
        )
        icone_box.pack(pady=(0, 25))
        icone_box.pack_propagate(False)
        self.icone_box = icone_box

        ctk.CTkLabel(
            icone_box,
            text="✨",
            font=ctk.CTkFont(size=38),
            text_color="#FFFFFF",
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            conteudo,
            text="Bem-vindo,",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color=get_color("text"),
        ).pack()

        ctk.CTkLabel(
            conteudo,
            text=self.usuario[1],
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color=get_color("accent"),
        ).pack(pady=(0, 15))

        ctk.CTkLabel(
            conteudo,
            text="Selecione uma opção no menu lateral\npara gerenciar seus atendimentos e pacientes.",
            font=ctk.CTkFont(size=15),
            text_color=get_color("text_secondary"),
            justify="center",
        ).pack()

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

    def show_configuracoes(self):
        self.clear()
        ConfiguracoesView(self.content)

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

        # Atualiza cabeçalho (logo + título)
        self.logo_box.configure(fg_color=self.accent)
        self.lbl_titulo.configure(text_color=get_color("text"))
        self.lbl_subtitulo.configure(text_color=self.accent)

        # Atualiza divisores
        self.divisor_topo.configure(fg_color=get_color("border"))
        self.divisor_rodape.configure(fg_color=get_color("border"))

        # Atualiza botões do menu
        for b in self.botoes_menu:
            if b is self.botao_ativo:
                b.configure(fg_color=self.accent, text_color="#FFFFFF")
            else:
                b.configure(
                    fg_color=self.sidebar_bg,
                    hover_color=get_color("accent_hover"),
                    text_color=get_color("menu_text"),
                )

        # Atualiza botão "Sair" (mantém destaque vermelho sempre)
        self.btn_sair.configure(
            hover_color=get_color("danger"),
            text_color=get_color("danger"),
        )

        # Atualiza switch e label de tema
        self.lbl_tema.configure(text_color=get_color("text"))
        self.switch_tema.configure(progress_color=self.accent)

        # Atualiza cartão do usuário
        self.avatar.configure(fg_color=self.accent)
        self.lbl_usuario.configure(text_color=get_color("text"))
        self.lbl_cargo.configure(text_color=get_color("text_secondary"))