import customtkinter as ctk
from .theme import get_color
from controllers.medico_controller import buscar_por_usuario
from views.agenda_view import AgendaView
from views.patients_view import PatientsView
from views.doctor_view import DoctorView
from views.configuracoes_view import ConfiguracoesView
from views.reports_view import ReportsView

# Rótulos de cargo exibidos abaixo do nome do usuário
CARGOS = {
    "admin": "ADMINISTRADOR",
    "atendente": "ATENDENTE",
    "medico": "MÉDICO",
}

# Breakpoints de largura (px) para comportamento responsivo
BP_SMALL  = 700   # abaixo disso: sidebar recolhida (só ícones)
BP_MEDIUM = 1000  # abaixo disso: sidebar estreita (sem rótulo de texto longo)


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.usuario    = usuario
        self.botao_ativo = None
        self.modo       = "Dark"
        self.btn_sair   = None
        print(self.usuario)
        # Estado da sidebar: "full" | "compact" | "mini"
        self._sidebar_state = "full"

        # Dimensões da sidebar para cada estado
        self.SIDEBAR_FULL    = 230
        self.SIDEBAR_COMPACT = 160
        self.SIDEBAR_MINI    = 64

        # ------------------------------------------------------------------
        # Guarda qual método (show_agenda, show_atendimentos, etc) abriu a
        # tela de conteúdo atualmente visível. Usado em atualizar_cores()
        # para recarregar a MESMA tela após uma troca de tema, em vez de
        # só recarregar a tela de welcome quando nenhum botão está ativo.
        # Cada show_* abaixo atualiza este atributo antes de montar a tela.
        # ------------------------------------------------------------------
        self.tela_atual_callback = None

        self._build_ui()

        # Monitora redimensionamento da janela raiz
        self.master.bind("<Configure>", self._on_resize, add="+")

    # ──────────────────────────────────────────────
    #  Construção da UI
    # ──────────────────────────────────────────────
    def _build_ui(self):
        self.bg         = get_color("bg")
        self.sidebar_bg = get_color("sidebar")
        self.topbar_bg  = get_color("topbar")
        self.accent     = get_color("accent")
        self.card_bg    = get_color("card")

        self.configure(fg_color=self.bg)

        # ── Topbar ──────────────────────────────────
        self.topbar = ctk.CTkFrame(self, height=40, fg_color=self.topbar_bg, corner_radius=0)
        self.topbar.pack(fill="x", side="top")

        # ── Corpo principal ──────────────────────────
        container = ctk.CTkFrame(self, fg_color=self.bg, corner_radius=0)
        container.pack(fill="both", expand=True)

        # ── Sidebar ──────────────────────────────────
        self.sidebar = ctk.CTkFrame(
            container,
            width=self.SIDEBAR_FULL,
            fg_color=self.sidebar_bg,
            corner_radius=0,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ── Área de conteúdo ─────────────────────────
        self.content = ctk.CTkFrame(container, fg_color=self.bg, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self._build_sidebar()
        self.show_welcome()

    def _build_sidebar(self):
        """Popula (ou re-popula) a sidebar inteira."""
        for w in self.sidebar.winfo_children():
            w.destroy()

        tipo = self.usuario[0]
        state = self._sidebar_state
        mini  = (state == "mini")

        # ── Cabeçalho / logo ─────────────────────────
        cabecalho = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        cabecalho.pack(fill="x", pady=(24, 16))
        self.cabecalho = cabecalho

        logo_size   = 48 if not mini else 40
        logo_radius = 14 if not mini else 12

        self.logo_box = ctk.CTkFrame(
            cabecalho,
            width=logo_size,
            height=logo_size,
            corner_radius=logo_radius,
            fg_color=self.accent,
        )
        self.logo_box.pack(pady=(0, 8 if not mini else 0))
        self.logo_box.pack_propagate(False)

        self.lbl_logo = ctk.CTkLabel(
            self.logo_box,
            text="+",
            font=ctk.CTkFont(size=24 if not mini else 20, weight="bold"),
            text_color="#FFFFFF",
        )
        self.lbl_logo.place(relx=0.5, rely=0.5, anchor="center")

        if not mini:
            self.lbl_titulo = ctk.CTkLabel(
                cabecalho,
                text="Clínica Médica",
                font=ctk.CTkFont(size=16 if state == "compact" else 19, weight="bold"),
                text_color=get_color("text"),
            )
            self.lbl_titulo.pack()

            self.lbl_subtitulo = ctk.CTkLabel(
                cabecalho,
                text="SISTEMA DE GESTÃO",
                text_color=self.accent,
                font=ctk.CTkFont(size=9 if state == "compact" else 11, weight="bold"),
            )
            self.lbl_subtitulo.pack(pady=(2, 0))

        # ── Divisor topo ──────────────────────────────
        self.divisor_topo = ctk.CTkFrame(self.sidebar, height=1, fg_color=get_color("border"))
        self.divisor_topo.pack(fill="x", padx=12, pady=(12, 10))

        id_usuario = self.usuario[2]
        print(id_usuario)
        # ── Itens de menu ────────────────────────────
        if tipo == "atendente":
            menu_items = [
                ("📅", "Agenda",        self.show_agenda),
                ("👥", "Pacientes",     self.show_pacientes),
            ]
        elif tipo == "medico":

            menu_items = [
                ("📅", "Minha agenda",  self.show_agenda),
                ("🩺", "Atendimentos",  self.show_atendimentos),
                ("📊", "Relatórios",    self.show_relatorios),
            ]
            dados_medico_logado = buscar_por_usuario(id_usuario=id_usuario)
            print(dados_medico_logado)
            self.id_medico_logado = dados_medico_logado[0]
            self.nome_medico_logado = dados_medico_logado[1]
        else:
            menu_items = [
                ("📅", "Agenda",        self.show_agenda),
                ("👥", "Pacientes",     self.show_pacientes),
                ("🩺", "Atendimentos",  self.show_atendimentos),
                ("📊", "Relatórios",    self.show_relatorios),
                ("⚙️", "Configurações", self.show_configuracoes),
            ]

        menu_area = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        menu_area.pack(fill="x")

        self.botoes_menu = []
        padx = 8 if mini else 12

        for icone, texto, command in menu_items:
            label = icone if mini else f"  {icone}   {texto}"
            btn = ctk.CTkButton(
                menu_area,
                text=label,
                height=42,
                corner_radius=10,
                fg_color=self.sidebar_bg,
                hover_color=get_color("accent_hover"),
                text_color=get_color("menu_text"),
                font=ctk.CTkFont(size=13 if state == "compact" else 14),
                anchor="center" if mini else "w",
                border_width=0,
            )
            btn.pack(fill="x", padx=padx, pady=3)
            btn.configure(command=lambda c=command, b=btn: self.handle_click(c, b))
            self.botoes_menu.append(btn)

        # Restaura botão ativo (se houver)
        if self.botao_ativo is not None:
            idx = getattr(self, "_botao_ativo_idx", None)
            if idx is not None and idx < len(self.botoes_menu):
                self.botoes_menu[idx].configure(fg_color=self.accent, text_color="#FFFFFF")
                self.botao_ativo = self.botoes_menu[idx]

        # ── Espaçador ────────────────────────────────
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        # ── Rodapé ───────────────────────────────────
        rodape = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        rodape.pack(side="bottom", fill="x")
        self.rodape = rodape

        self.divisor_rodape = ctk.CTkFrame(rodape, height=1, fg_color=get_color("border"))
        self.divisor_rodape.pack(fill="x", padx=12, pady=(0, 12))

        # Switch de tema (oculto no modo mini)
        if not mini:
            tema_frame = ctk.CTkFrame(rodape, fg_color="transparent")
            tema_frame.pack(fill="x", padx=12, pady=(0, 10))
            self.tema_frame = tema_frame

            self.lbl_tema = ctk.CTkLabel(
                tema_frame,
                text="🌙  Modo escuro",
                text_color=get_color("text"),
                font=ctk.CTkFont(size=12),
            )
            self.lbl_tema.pack(side="left")

            self.switch_var = ctk.StringVar(value="on")
            self.switch_tema = ctk.CTkSwitch(
                tema_frame,
                text="",
                variable=self.switch_var,
                onvalue="on",
                offvalue="off",
                progress_color=self.accent,
                command=self.toggle_theme,
                width=38,
            )
            self.switch_tema.pack(side="right")
            if self.modo == "Dark":
                self.switch_tema.select()
            else:
                self.switch_tema.deselect()
        else:
            # Botão compacto de tema no modo mini
            btn_tema = ctk.CTkButton(
                rodape,
                text="🌙" if self.modo == "Dark" else "☀️",
                width=40,
                height=36,
                corner_radius=10,
                fg_color="transparent",
                hover_color=get_color("accent_hover"),
                text_color=get_color("text"),
                font=ctk.CTkFont(size=16),
                command=self.toggle_theme,
            )
            btn_tema.pack(padx=padx, pady=(0, 6))
            self._btn_tema_mini = btn_tema

        # Botão Sair
        sair_text  = "⏻" if mini else "  ⏻   Sair"
        sair_anchor = "center" if mini else "w"

        self.btn_sair = ctk.CTkButton(
            rodape,
            text=sair_text,
            height=42,
            corner_radius=10,
            fg_color="transparent",
            hover_color=get_color("danger"),
            text_color=get_color("danger"),
            font=ctk.CTkFont(size=14),
            anchor=sair_anchor,
            border_width=0,
            command=self.master.show_login,
        )
        self.btn_sair.pack(fill="x", padx=padx, pady=(0, 12))

        # Cartão do usuário (oculto no modo mini)
        if not mini:
            usuario_card = ctk.CTkFrame(rodape, fg_color="transparent")
            usuario_card.pack(fill="x", padx=padx, pady=(4, 16))
            self.usuario_card = usuario_card

            inicial = self.usuario[1][0].upper() if self.usuario[1] else "?"

            self.avatar = ctk.CTkFrame(
                usuario_card, width=36, height=36, corner_radius=18, fg_color=self.accent,
            )
            self.avatar.pack(side="left")
            self.avatar.pack_propagate(False)

            self.lbl_avatar = ctk.CTkLabel(
                self.avatar,
                text=inicial,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#FFFFFF",
            )
            self.lbl_avatar.place(relx=0.5, rely=0.5, anchor="center")

            textos = ctk.CTkFrame(usuario_card, fg_color="transparent")
            textos.pack(side="left", padx=(8, 0), fill="x", expand=True)

            ctk.CTkLabel(
                textos,
                text=self.usuario[1],
                text_color=get_color("text"),
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                textos,
                text=CARGOS.get(tipo, tipo.upper()),
                text_color=get_color("text_secondary"),
                font=ctk.CTkFont(size=9),
                anchor="w",
            ).pack(fill="x")
        else:
            # Avatar compacto centrado
            inicial = self.usuario[1][0].upper() if self.usuario[1] else "?"
            self.avatar = ctk.CTkFrame(
                rodape, width=36, height=36, corner_radius=18, fg_color=self.accent,
            )
            self.avatar.pack(pady=(0, 16))
            self.avatar.pack_propagate(False)
            ctk.CTkLabel(
                self.avatar,
                text=inicial,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#FFFFFF",
            ).place(relx=0.5, rely=0.5, anchor="center")

    # ──────────────────────────────────────────────
    #  Responsividade
    # ──────────────────────────────────────────────
    def _on_resize(self, event=None):
        """Recalcula o estado da sidebar conforme a largura da janela."""
        try:
            width = self.master.winfo_width()
        except Exception:
            return

        if width < BP_SMALL:
            new_state = "mini"
        elif width < BP_MEDIUM:
            new_state = "compact"
        else:
            new_state = "full"

        if new_state != self._sidebar_state:
            self._sidebar_state = new_state
            target_width = {
                "full":    self.SIDEBAR_FULL,
                "compact": self.SIDEBAR_COMPACT,
                "mini":    self.SIDEBAR_MINI,
            }[new_state]
            self.sidebar.configure(width=target_width)
            self._build_sidebar()

    # ──────────────────────────────────────────────
    #  Alternância de tema
    # ──────────────────────────────────────────────
    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.modo = "Light"
        else:
            ctk.set_appearance_mode("Dark")
            self.modo = "Dark"

        self.atualizar_cores()

    # ──────────────────────────────────────────────
    #  Navegação
    # ──────────────────────────────────────────────
    def handle_click(self, func, botao):
        for i, b in enumerate(self.botoes_menu):
            b.configure(fg_color=self.sidebar_bg, text_color=get_color("menu_text"))
            if b is botao:
                self._botao_ativo_idx = i

        botao.configure(fg_color=self.accent, text_color="#FFFFFF")
        self.botao_ativo = botao
        func()

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.tela_atual_callback = self.show_welcome
        self.clear()

        card = ctk.CTkFrame(
            self.content,
            fg_color=get_color("card"),
            corner_radius=20,
            border_width=1,
            border_color=get_color("border"),
        )
        # Responsivo: usa place com rel* para centrar e escalar
        card.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.65, anchor="center")

        # Conteúdo interno centralizado
        conteudo = ctk.CTkFrame(card, fg_color="transparent")
        conteudo.place(relx=0.5, rely=0.5, anchor="center")

        icone_box = ctk.CTkFrame(
            conteudo, width=80, height=80, corner_radius=20,
            fg_color=self.accent, border_width=2,
            border_color=get_color("accent_hover"),
        )
        icone_box.pack(pady=(0, 20))
        icone_box.pack_propagate(False)

        ctk.CTkLabel(
            icone_box, text="✨",
            font=ctk.CTkFont(size=34), text_color="#FFFFFF",
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            conteudo, text="Bem-vindo,",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=get_color("text"),
        ).pack()

        ctk.CTkLabel(
            conteudo, text=self.usuario[1],
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.accent,
        ).pack(pady=(0, 12))

        ctk.CTkLabel(
            conteudo,
            text="Selecione uma opção no menu lateral\npara gerenciar seus atendimentos e pacientes.",
            font=ctk.CTkFont(size=14),
            text_color=get_color("text_secondary"),
            justify="center",
        ).pack()

    def show_agenda(self):
        self.tela_atual_callback = self.show_agenda
        self.clear()
        AgendaView(self.content)

    def show_pacientes(self):
        self.tela_atual_callback = self.show_pacientes
        self.clear()
        PatientsView(self.content)

    def show_atendimentos(self):
        self.tela_atual_callback = self.show_atendimentos
        self.clear()
        DoctorView(self.content, id_medico=self.id_medico_logado,nome_medico=self.nome_medico_logado)

    def show_relatorios(self):
        self.tela_atual_callback = self.show_relatorios
        self.clear()
        ReportsView(self.content)

    def show_configuracoes(self):
        self.tela_atual_callback = self.show_configuracoes
        self.clear()
        ConfiguracoesView(self.content)

    # ──────────────────────────────────────────────
    #  Atualização de cores (pós-troca de tema)
    # ──────────────────────────────────────────────
    def atualizar_cores(self):
        self.bg         = get_color("bg")
        self.sidebar_bg = get_color("sidebar")
        self.topbar_bg  = get_color("topbar")
        self.accent     = get_color("accent")
        self.card_bg    = get_color("card")

        self.configure(fg_color=self.bg)
        self.topbar.configure(fg_color=self.topbar_bg)
        self.sidebar.configure(fg_color=self.sidebar_bg)
        self.content.configure(fg_color=self.bg)

        # Reconstrói sidebar para refletir novas cores
        self._build_sidebar()

        # ------------------------------------------------------------------
        # ANTES: só recarregava a tela de welcome quando self.botao_ativo
        # era None — ou seja, qualquer outra tela aberta (Agenda, Doctor,
        # etc) nunca era recarregada após a troca de tema, ficando com
        # cores antigas até o usuário trocar de tela manualmente.
        #
        # AGORA: chama de volta o mesmo método que abriu a tela atual
        # (guardado em self.tela_atual_callback por cada show_*), igual
        # ao que já acontece quando o usuário clica manualmente no menu.
        # Fallback para show_welcome caso, por algum motivo, nenhuma tela
        # tenha sido aberta ainda.
        # ------------------------------------------------------------------
        if self.tela_atual_callback:
            self.tela_atual_callback()
        else:
            self.show_welcome()