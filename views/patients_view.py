import customtkinter as ctk
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# BACK-END (comentado – conecte quando quiser)
from controllers.paciente_controller import salvar as salvar_paciente
from controllers.paciente_controller import listar as listar_pacientes
# from controllers.paciente_controller import atualizar as atualizar_paciente
# from controllers.paciente_controller import deletar as deletar_paciente
# ─────────────────────────────────────────────────────────────────────────────

# ── Paleta ──────────────────────────────────────────────────────────────────
COR_AZUL        = "#2563EB"
COR_AZUL_HOVER  = "#1D4ED8"
COR_CINZA_BTN   = "#6B7280"
COR_VERMELHO    = "#DC2626"
COR_FUNDO_CARD  = "#F8FAFC"
COR_BORDA_CARD  = "#E2E8F0"
COR_TEXTO_MUTED = "#64748B"
COR_BADGE_P     = "#DBEAFE"   # azul-claro (particular)
COR_BADGE_P_TXT = "#1E40AF"
COR_BADGE_C     = "#D1FAE5"   # verde-claro (convênio)
COR_BADGE_C_TXT = "#065F46"
# ────────────────────────────────────────────────────────────────────────────


class PatientsView(ctk.CTkFrame):
    """Tela de gerenciamento de pacientes."""

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=("white", "#111827"))

        self.pacientes: list[dict] = []   # ← será substituído por listar_pacientes()
        self.filtro_nome: str = ""
        self._popup_aberto = False

        self.render()

    # ═════════════════════════════════════════════════════════════════════════
    # MÁSCARAS
    # ═════════════════════════════════════════════════════════════════════════
    @staticmethod
    def _mask_cpf(texto: str) -> str:
        d = "".join(filter(str.isdigit, texto))[:11]
        if len(d) <= 3:   return d
        if len(d) <= 6:   return f"{d[:3]}.{d[3:]}"
        if len(d) <= 9:   return f"{d[:3]}.{d[3:6]}.{d[6:]}"
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

    @staticmethod
    def _mask_telefone(texto: str) -> str:
        d = "".join(filter(str.isdigit, texto))[:11]
        if len(d) <= 2:   return f"({d}"
        if len(d) <= 7:   return f"({d[:2]}) {d[2:]}"
        if len(d) <= 10:  return f"({d[:2]}) {d[2:6]}-{d[6:]}"
        return f"({d[:2]}) {d[2:7]}-{d[7:]}"

    @staticmethod
    def _mask_data(texto: str) -> str:
        d = "".join(filter(str.isdigit, texto))[:8]
        if len(d) <= 2:  return d
        if len(d) <= 4:  return f"{d[:2]}/{d[2:]}"
        return f"{d[:2]}/{d[2:4]}/{d[4:]}"

    # ═════════════════════════════════════════════════════════════════════════
    # RENDER PRINCIPAL
    # ═════════════════════════════════════════════════════════════════════════
    def render(self):
        for w in self.winfo_children():
            w.destroy()

        # ── Cabeçalho ──────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(24, 0))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(
            left, text="Pacientes",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold")
        ).pack(anchor="w")
        ctk.CTkLabel(
            left, text="Cadastro e gerenciamento de pacientes",
            font=ctk.CTkFont(size=13), text_color=COR_TEXTO_MUTED
        ).pack(anchor="w")

        ctk.CTkButton(
            header, text="＋  Novo Paciente",
            fg_color=COR_AZUL, hover_color=COR_AZUL_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8, height=38,
            command=self._popup
        ).pack(side="right")

        # ── Divisor ────────────────────────────────────────────────────────
        div = ctk.CTkFrame(self, height=1, fg_color=COR_BORDA_CARD)
        div.pack(fill="x", padx=32, pady=16)

        # ── Barra de busca ─────────────────────────────────────────────────
        busca_wrap = ctk.CTkFrame(self, fg_color="transparent")
        busca_wrap.pack(fill="x", padx=32, pady=(0, 12))

        self.input_busca = ctk.CTkEntry(
            busca_wrap,
            placeholder_text="🔍  Buscar por nome...",
            height=38, corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        self.input_busca.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.input_busca.bind("<Return>", lambda e: self._buscar())

        ctk.CTkButton(
            busca_wrap, text="Buscar", width=90, height=38,
            fg_color=COR_AZUL, hover_color=COR_AZUL_HOVER,
            corner_radius=8, font=ctk.CTkFont(size=13),
            command=self._buscar
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            busca_wrap, text="Limpar", width=80, height=38,
            fg_color=COR_CINZA_BTN, hover_color="#4B5563",
            corner_radius=8, font=ctk.CTkFont(size=13),
            command=self._limpar_busca
        ).pack(side="left")

        # ── Contador ───────────────────────────────────────────────────────
        self.lbl_contagem = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_MUTED
        )
        self.lbl_contagem.pack(anchor="w", padx=32, pady=(0, 4))

        # ── Lista ─────────────────────────────────────────────────────────
        self.lista = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COR_BORDA_CARD
        )
        self.lista.pack(fill="both", expand=True, padx=32, pady=(0, 16))

        self._render_lista()

        # ── BACK (descomente para carregar do banco) ───────────────────────
        # self.pacientes = listar_pacientes()
        # self._render_lista()

    # ═════════════════════════════════════════════════════════════════════════
    # BUSCA
    # ═════════════════════════════════════════════════════════════════════════
    def _buscar(self):
        self.filtro_nome = self.input_busca.get().strip().lower()
        self._render_lista()

    def _limpar_busca(self):
        self.filtro_nome = ""
        self.input_busca.delete(0, "end")
        self._render_lista()

    # ═════════════════════════════════════════════════════════════════════════
    # LISTA DE PACIENTES
    # ═════════════════════════════════════════════════════════════════════════
    def _render_lista(self):
        for w in self.lista.winfo_children():
            w.destroy()

        pacientes = self.pacientes
        if self.filtro_nome:
            pacientes = [
                p for p in pacientes
                if self.filtro_nome in p["nome"].lower()
            ]

        total = len(pacientes)
        sufixo = "paciente" if total == 1 else "pacientes"
        self.lbl_contagem.configure(
            text=f"{total} {sufixo} encontrado{'s' if total != 1 else ''}"
        )

        if not pacientes:
            empty = ctk.CTkFrame(self.lista, fg_color="transparent")
            empty.pack(pady=60)
            ctk.CTkLabel(
                empty, text="👤",
                font=ctk.CTkFont(size=40)
            ).pack()
            ctk.CTkLabel(
                empty,
                text="Nenhum paciente encontrado",
                font=ctk.CTkFont(size=15, weight="bold")
            ).pack(pady=(8, 4))
            ctk.CTkLabel(
                empty,
                text="Clique em '＋ Novo Paciente' para cadastrar.",
                font=ctk.CTkFont(size=13),
                text_color=COR_TEXTO_MUTED
            ).pack()
            return

        for p in pacientes:
            self._card(p)

    # ═════════════════════════════════════════════════════════════════════════
    # CARD
    # ═════════════════════════════════════════════════════════════════════════
    def _card(self, p: dict):
        card = ctk.CTkFrame(
            self.lista,
            fg_color=(COR_FUNDO_CARD, "#1E293B"),
            corner_radius=12,
            border_width=1,
            border_color=COR_BORDA_CARD
        )
        card.pack(fill="x", pady=5)

        # Efeito hover
        def on_enter(e):
            card.configure(border_color=COR_AZUL)
        def on_leave(e):
            card.configure(border_color=COR_BORDA_CARD)
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        # ── Avatar com iniciais ────────────────────────────────────────────
        iniciais = "".join(p["nome"].split()[:2]).upper()[:2]
        avatar = ctk.CTkFrame(
            inner, width=46, height=46,
            fg_color=COR_AZUL, corner_radius=23
        )
        avatar.pack(side="left", padx=(0, 14))
        avatar.pack_propagate(False)
        ctk.CTkLabel(
            avatar, text=iniciais,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # ── Informações ───────────────────────────────────────────────────
        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        # Linha 1 – nome + badge tipo
        linha1 = ctk.CTkFrame(info, fg_color="transparent")
        linha1.pack(anchor="w", fill="x")

        ctk.CTkLabel(
            linha1, text=p["nome"],
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")

        tipo = p.get("tipo", "Particular")
        badge_bg  = COR_BADGE_C if tipo == "Convênio" else COR_BADGE_P
        badge_txt = COR_BADGE_C_TXT if tipo == "Convênio" else COR_BADGE_P_TXT
        badge = ctk.CTkFrame(
            linha1, fg_color=badge_bg, corner_radius=10
        )
        badge.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(
            badge, text=f"  {tipo}  ",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=badge_txt
        ).pack()

        # Linha 2 – CPF | Telefone | Nascimento
        ctk.CTkLabel(
            info,
            text=f"CPF: {p.get('cpf', '—')}   ·   Tel: {p.get('telefone', '—')}   ·   Nasc: {p.get('nascimento', '—')}",
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_MUTED
        ).pack(anchor="w", pady=(2, 1))

        # Linha 3 – Plano / Carteirinha
        if tipo == "Convênio":
            plano_txt = (
                f"Plano: {p.get('plano', '—')}   ·   "
                f"Carteirinha: {p.get('carteirinha', '—')}"
            )
        else:
            plano_txt = "Atendimento particular"
        ctk.CTkLabel(
            info, text=plano_txt,
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_MUTED
        ).pack(anchor="w", pady=(1, 0))

        # Linha 4 – Endereço
        ctk.CTkLabel(
            info,
            text=f"📍 {p.get('endereco', '—')}",
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_MUTED
        ).pack(anchor="w", pady=(1, 0))

        # ── Botões ────────────────────────────────────────────────────────
        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.pack(side="right", padx=(12, 0))

        ctk.CTkButton(
            btns, text="Editar", width=80, height=32,
            fg_color="transparent", border_width=1,
            border_color=COR_AZUL, text_color=COR_AZUL,
            hover_color=COR_BADGE_P,
            corner_radius=8, font=ctk.CTkFont(size=12),
            command=lambda p=p: self._popup(p)
        ).pack(pady=(0, 6))

        ctk.CTkButton(
            btns, text="Remover", width=80, height=32,
            fg_color="transparent", border_width=1,
            border_color=COR_VERMELHO, text_color=COR_VERMELHO,
            hover_color="#FEE2E2",
            corner_radius=8, font=ctk.CTkFont(size=12),
            command=lambda p=p: self._remover(p)
        ).pack()

    # ═════════════════════════════════════════════════════════════════════════
    # POPUP – Cadastro / Edição
    # ═════════════════════════════════════════════════════════════════════════
    def _popup(self, paciente: dict | None = None):
        if self._popup_aberto:
            return
        self._popup_aberto = True

        popup = ctk.CTkToplevel(self)
        popup.title("Novo Paciente" if not paciente else "Editar Paciente")
        popup.geometry("460x680")
        popup.resizable(False, False)
        popup.grab_set()

        def on_close():
            self._popup_aberto = False
            popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", on_close)

        # ── Scroll interno ────────────────────────────────────────────────
        scroll = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        frame = ctk.CTkFrame(scroll, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=8)

        # Título
        titulo_txt = "Novo Paciente" if not paciente else "Editar Paciente"
        ctk.CTkLabel(
            frame, text=titulo_txt,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", pady=(8, 16))

        # ── Helper para seção ─────────────────────────────────────────────
        def secao(texto: str):
            s = ctk.CTkFrame(frame, fg_color="transparent")
            s.pack(fill="x", pady=(12, 4))
            ctk.CTkLabel(
                s, text=texto.upper(),
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=COR_TEXTO_MUTED
            ).pack(side="left")
            ctk.CTkFrame(s, height=1, fg_color=COR_BORDA_CARD).pack(
                side="left", fill="x", expand=True, padx=(8, 0), pady=7
            )

        # ── Helper para campo ─────────────────────────────────────────────
        def campo(label: str, placeholder: str = "") -> ctk.CTkEntry:
            ctk.CTkLabel(
                frame, text=label,
                font=ctk.CTkFont(size=12),
                text_color=COR_TEXTO_MUTED,
                anchor="w"
            ).pack(fill="x", pady=(4, 0))
            e = ctk.CTkEntry(
                frame, placeholder_text=placeholder,
                height=36, corner_radius=8
            )
            e.pack(fill="x", pady=(2, 0))
            return e

        # ─── Seção: Dados Pessoais ─────────────────────────────────────────
        secao("Dados Pessoais")

        nome_e = campo("Nome completo *", "Ex: João da Silva")

        # Nascimento
        nasc_e = campo("Data de nascimento", "DD/MM/AAAA")

        def mask_nasc(e):
            v = self._mask_data(nasc_e.get())
            nasc_e.delete(0, "end"); nasc_e.insert(0, v)
        nasc_e.bind("<KeyRelease>", mask_nasc)

        # CPF
        cpf_e = campo("CPF", "000.000.000-00")

        def mask_cpf(e):
            v = self._mask_cpf(cpf_e.get())
            cpf_e.delete(0, "end"); cpf_e.insert(0, v)
        cpf_e.bind("<KeyRelease>", mask_cpf)

        # Telefone
        tel_e = campo("Telefone", "(00) 00000-0000")

        def mask_tel(e):
            v = self._mask_telefone(tel_e.get())
            tel_e.delete(0, "end"); tel_e.insert(0, v)
        tel_e.bind("<KeyRelease>", mask_tel)

        # ─── Seção: Endereço ───────────────────────────────────────────────
        secao("Endereço")
        end_e = campo("Endereço completo", "Rua, número, bairro, cidade")

        # ─── Seção: Tipo de Atendimento ───────────────────────────────────
        secao("Tipo de Atendimento")

        ctk.CTkLabel(
            frame, text="Tipo *",
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(4, 0))

        tipo_var = ctk.StringVar(value="Particular")
        tipo_menu = ctk.CTkOptionMenu(
            frame,
            values=["Particular", "Convênio"],
            variable=tipo_var,
            height=36, corner_radius=8,
            fg_color=("#F1F5F9", "#1E293B"),
            button_color=COR_AZUL, button_hover_color=COR_AZUL_HOVER,
            command=lambda v: _toggle_convenio(v)
        )
        tipo_menu.pack(fill="x", pady=(2, 0))

        # Campos de convênio (aparecem/somem conforme tipo)
        convenio_frame = ctk.CTkFrame(frame, fg_color="transparent")

        ctk.CTkLabel(
            convenio_frame, text="Nome do Plano",
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_MUTED, anchor="w"
        ).pack(fill="x", pady=(4, 0))
        plano_e = ctk.CTkEntry(
            convenio_frame, placeholder_text="Ex: Unimed, Bradesco Saúde",
            height=36, corner_radius=8
        )
        plano_e.pack(fill="x", pady=(2, 0))

        ctk.CTkLabel(
            convenio_frame, text="Número da Carteirinha",
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_MUTED, anchor="w"
        ).pack(fill="x", pady=(8, 0))
        cart_e = ctk.CTkEntry(
            convenio_frame, placeholder_text="Número da carteirinha",
            height=36, corner_radius=8
        )
        cart_e.pack(fill="x", pady=(2, 0))

        def _toggle_convenio(valor: str):
            if valor == "Convênio":
                convenio_frame.pack(fill="x", pady=(0, 4))
            else:
                convenio_frame.pack_forget()

        # Estado inicial
        if paciente and paciente.get("tipo") == "Convênio":
            convenio_frame.pack(fill="x", pady=(0, 4))

        # ─── Preencher campos se for edição ───────────────────────────────
        if paciente:
            nome_e.insert(0, paciente.get("nome", ""))
            nasc_e.insert(0, paciente.get("nascimento", ""))
            cpf_e.insert(0, paciente.get("cpf", ""))
            tel_e.insert(0, paciente.get("telefone", ""))
            end_e.insert(0, paciente.get("endereco", ""))
            tipo_var.set(paciente.get("tipo", "Particular"))
            plano_e.insert(0, paciente.get("plano", ""))
            cart_e.insert(0, paciente.get("carteirinha", ""))

        # ─── Validação / Mensagem de erro ─────────────────────────────────
        msg_erro = ctk.CTkLabel(
            frame, text="",
            text_color=COR_VERMELHO,
            font=ctk.CTkFont(size=12)
        )
        msg_erro.pack(pady=(10, 0))

        # ─── Salvar ───────────────────────────────────────────────────────
        def _salvar():
            nome_val = nome_e.get().strip()
            if not nome_val:
                msg_erro.configure(text="⚠  Nome é obrigatório.")
                return

            tipo_val = tipo_var.get()
            if tipo_val == "Convênio" and not plano_e.get().strip():
                msg_erro.configure(text="⚠  Informe o nome do plano.")
                return

            dados = {
                "nome":        nome_val,
                "nascimento":  nasc_e.get().strip(),
                "endereco":    end_e.get().strip(),
                "cpf":         cpf_e.get().strip(),
                "telefone":    tel_e.get().strip(),
                "carteirinha": cart_e.get().strip() if tipo_val == "Convênio" else "",
                "tipo":        tipo_val,
                "plano":       plano_e.get().strip() if tipo_val == "Convênio" else "",
            }

            nome = dados["nome"]
            data_nascimento = dados["nascimento"]
            endereco = dados["endereco"]
            cpf = dados["cpf"]
            telefone = dados["telefone"]
            carteirinha = dados["carteirinha"]
            data_formatada = datetime.strptime(data_nascimento, "%d/%m/%Y").strftime("%Y-%m-%d")
            _dados = (nome, data_formatada, endereco, cpf, telefone, carteirinha)
            if paciente:
                paciente.update(dados)
                # ── BACK ─────────────────────────────────────────────────
                # atualizar_paciente(paciente["id"], dados)
            else:
                salvar_paciente(_dados)
                self.pacientes.append(dados)


                d = listar_pacientes()
                print(d)
                # ── BACK ─────────────────────────────────────────────────
                # novo = salvar_paciente(dados)
                # self.pacientes.append(novo)

            self._render_lista()
            on_close()

        ctk.CTkButton(
            frame, text="Salvar",
            fg_color=COR_AZUL, hover_color=COR_AZUL_HOVER,
            height=42, corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=_salvar
        ).pack(fill="x", pady=(12, 4))

        ctk.CTkButton(
            frame, text="Cancelar",
            fg_color="transparent", border_width=1,
            border_color=COR_BORDA_CARD,
            text_color=COR_TEXTO_MUTED,
            hover_color=("#F1F5F9", "#1E293B"),
            height=38, corner_radius=8,
            font=ctk.CTkFont(size=13),
            command=on_close
        ).pack(fill="x", pady=(0, 16))

    # ═════════════════════════════════════════════════════════════════════════
    # REMOVER
    # ═════════════════════════════════════════════════════════════════════════
    def _remover(self, paciente: dict):
        """Confirmação simples antes de remover o paciente da lista."""
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirmar remoção")
        confirm.geometry("340x180")
        confirm.resizable(False, False)
        confirm.grab_set()

        f = ctk.CTkFrame(confirm, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=24, pady=20)

        ctk.CTkLabel(
            f, text="Remover paciente?",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(0, 6))
        ctk.CTkLabel(
            f, text=f"'{paciente['nome']}' será removido da lista.",
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_MUTED,
            wraplength=290
        ).pack()

        btns = ctk.CTkFrame(f, fg_color="transparent")
        btns.pack(pady=(16, 0))

        ctk.CTkButton(
            btns, text="Cancelar", width=120, height=36,
            fg_color="transparent", border_width=1,
            border_color=COR_BORDA_CARD,
            text_color=COR_TEXTO_MUTED,
            command=confirm.destroy
        ).pack(side="left", padx=(0, 8))

        def _confirmar():
            self.pacientes.remove(paciente)
            # ── BACK ─────────────────────────────────────────────────────
            # deletar_paciente(paciente["id"])
            self._render_lista()
            confirm.destroy()

        ctk.CTkButton(
            btns, text="Remover", width=120, height=36,
            fg_color=COR_VERMELHO, hover_color="#B91C1C",
            font=ctk.CTkFont(weight="bold"),
            command=_confirmar
        ).pack(side="left")