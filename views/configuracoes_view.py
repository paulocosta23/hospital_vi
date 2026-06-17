import customtkinter as ctk
from .theme import get_color

# ─────────────────────────────────────────────────────────────────────────────
# BACK-END (comentado – conecte quando quiser)
# from controllers.usuario_controller     import salvar, listar, atualizar, deletar as del_usuario
# from controllers.medico_controller      import salvar, listar, atualizar, deletar as del_medico
# from controllers.plano_controller       import salvar, listar, atualizar, deletar as del_plano
# from controllers.consultorio_controller import salvar, listar, atualizar, deletar as del_cons
# ─────────────────────────────────────────────────────────────────────────────

ESPECIALIDADES = [
    "Clínica Geral", "Cardiologia", "Dermatologia", "Ginecologia",
    "Neurologia", "Oftalmologia", "Ortopedia", "Pediatria",
    "Psiquiatria", "Urologia", "Outra",
]

TIPOS_USUARIO = ["admin", "medico", "recepcionista"]
STATUS_OPTS   = ["Ativo", "Inativo"]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS VISUAIS
# ─────────────────────────────────────────────────────────────────────────────

def _secao(parent, texto: str, muted: str):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=(14, 2))
    ctk.CTkLabel(
        row, text=texto.upper(),
        font=ctk.CTkFont(size=10, weight="bold"),
        text_color=muted,
    ).pack(side="left")
    ctk.CTkFrame(
        row, height=1, fg_color=get_color("border"),
    ).pack(side="left", fill="x", expand=True, padx=(8, 0), pady=6)


def _campo(parent, label: str, placeholder: str = "", muted: str = "#64748B") -> ctk.CTkEntry:
    ctk.CTkLabel(
        parent, text=label,
        font=ctk.CTkFont(size=12),
        text_color=muted, anchor="w",
    ).pack(fill="x", pady=(6, 0))
    e = ctk.CTkEntry(parent, placeholder_text=placeholder, height=36, corner_radius=10)
    e.pack(fill="x", pady=(2, 0))
    return e


def _select(parent, label: str, valores: list, var=None, muted: str = "#64748B", **kw):
    ctk.CTkLabel(
        parent, text=label,
        font=ctk.CTkFont(size=12),
        text_color=muted, anchor="w",
    ).pack(fill="x", pady=(6, 0))
    om = ctk.CTkOptionMenu(
        parent, values=valores, variable=var,
        height=36, corner_radius=10,
        button_color=get_color("accent"),
        button_hover_color=get_color("accent_hover"),
        **kw,
    )
    if var:
        om.configure(variable=var)
    om.pack(fill="x", pady=(2, 0))
    return om


def _confirmar_remocao(master, nome: str, callback, panel: str):
    d = ctk.CTkToplevel(master)
    d.title("Confirmar remoção")
    d.geometry("340x190")
    d.resizable(False, False)
    d.grab_set()
    d.configure(fg_color=panel)

    f = ctk.CTkFrame(d, fg_color="transparent")
    f.pack(fill="both", expand=True, padx=24, pady=20)

    ctk.CTkLabel(
        f, text="Remover registro?",
        font=ctk.CTkFont(size=16, weight="bold"),
    ).pack(pady=(0, 6))
    ctk.CTkLabel(
        f, text=f"'{nome}' será removido permanentemente.",
        font=ctk.CTkFont(size=13),
        text_color=get_color("text_secondary"),
        wraplength=290,
    ).pack()

    row = ctk.CTkFrame(f, fg_color="transparent")
    row.pack(pady=(16, 0))

    ctk.CTkButton(
        row, text="Cancelar", width=120, height=36,
        fg_color="transparent", border_width=1,
        border_color=get_color("border"),
        text_color=get_color("text_secondary"),
        command=d.destroy,
    ).pack(side="left", padx=(0, 8))

    def _ok():
        callback()
        d.destroy()

    ctk.CTkButton(
        row, text="Remover", width=120, height=36,
        fg_color=get_color("danger"),
        font=ctk.CTkFont(weight="bold"),
        command=_ok,
    ).pack(side="left")


# ─────────────────────────────────────────────────────────────────────────────
# CARD BASE
# ─────────────────────────────────────────────────────────────────────────────

class _CardBase(ctk.CTkFrame):
    def __init__(self, parent, on_editar, on_remover, avatar_cor: str, iniciais: str):
        super().__init__(
            parent,
            fg_color=get_color("card"),
            corner_radius=16,
            border_width=1,
            border_color=get_color("border"),
        )
        self.pack(fill="x", pady=8)

        def _enter(e): self.configure(border_color=get_color("accent"))
        def _leave(e): self.configure(border_color=get_color("border"))
        self.bind("<Enter>", _enter)
        self.bind("<Leave>", _leave)

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=12)

        # Avatar circular
        av = ctk.CTkFrame(inner, width=46, height=46, fg_color=avatar_cor, corner_radius=23)
        av.pack(side="left", padx=(0, 14))
        av.pack_propagate(False)
        ctk.CTkLabel(
            av, text=iniciais,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
        ).place(relx=0.5, rely=0.5, anchor="center")

        self._info = ctk.CTkFrame(inner, fg_color="transparent")
        self._info.pack(side="left", fill="x", expand=True)
        self._build_info()

        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            btns, text="Editar", width=80, height=30,
            fg_color=get_color("accent"),
            hover_color=get_color("accent_hover"),
            corner_radius=10, font=ctk.CTkFont(size=12),
            command=on_editar,
        ).pack(pady=(0, 6))

        ctk.CTkButton(
            btns, text="Remover", width=80, height=30,
            fg_color="transparent", border_width=1,
            border_color=get_color("danger"),
            text_color=get_color("danger"),
            hover_color="#FEE2E2",
            corner_radius=10, font=ctk.CTkFont(size=12),
            command=on_remover,
        ).pack()

    def _build_info(self):
        raise NotImplementedError


# ═════════════════════════════════════════════════════════════════════════════
# ABA: USUÁRIOS
# ═════════════════════════════════════════════════════════════════════════════

def _ocultar_cpf(cpf: str) -> str:
    d = "".join(filter(str.isdigit, cpf))
    if len(d) < 11:
        return cpf
    return f"{d[:3]}.***.***.{d[-2:]}"


def _formatar_cpf(texto: str) -> str:
    d = "".join(filter(str.isdigit, texto))[:11]
    if len(d) <= 3:  return d
    if len(d) <= 6:  return f"{d[:3]}.{d[3:]}"
    if len(d) <= 9:  return f"{d[:3]}.{d[3:6]}.{d[6:]}"
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"


class _CardUsuario(_CardBase):
    _CORES_TIPO = {
        "admin":         get_color("purple"),
        "medico":        get_color("success"),
        "recepcionista": get_color("accent"),
    }
    _AVATAR_CORES = {
        "admin":         get_color("purple"),
        "medico":        get_color("success"),
        "recepcionista": get_color("accent"),
    }

    def __init__(self, parent, u: dict, on_editar, on_remover):
        self._u = u
        iniciais = "".join(u["nome"].split()[:2]).upper()[:2]
        av_cor = self._AVATAR_CORES.get(u.get("tipo", ""), get_color("accent"))
        super().__init__(parent, on_editar, on_remover, av_cor, iniciais)

    def _build_info(self):
        u = self._u

        linha1 = ctk.CTkFrame(self._info, fg_color="transparent")
        linha1.pack(anchor="w", fill="x")

        ctk.CTkLabel(
            linha1, text=u["nome"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=get_color("text"),
        ).pack(side="left")

        tipo = u.get("tipo", "")
        badge_cor = self._CORES_TIPO.get(tipo, get_color("accent"))
        badge = ctk.CTkFrame(linha1, fg_color=badge_cor, corner_radius=10)
        badge.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(
            badge, text=f"  {tipo.upper()}  ",
            font=ctk.CTkFont(size=10, weight="bold"), text_color="white",
        ).pack()

        ctk.CTkLabel(
            self._info,
            text=f"CPF: {_ocultar_cpf(u.get('cpf', ''))}   ·   Login: {u.get('login', '—')}",
            font=ctk.CTkFont(size=12),
            text_color=get_color("text_secondary"),
        ).pack(anchor="w", pady=(3, 0))


class AbaUsuarios(ctk.CTkFrame):
    def __init__(self, master, panel: str, muted: str):
        super().__init__(master, fg_color="transparent")
        self._panel = panel
        self._muted = muted
        self.usuarios: list[dict] = []
        self._popup_aberto = False
        self._filtro = ""
        self._build()

    def _build(self):
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 8))

        self._busca = ctk.CTkEntry(
            topo, placeholder_text="🔍  Buscar usuário...",
            height=36, corner_radius=10, font=ctk.CTkFont(size=13),
        )
        self._busca.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._busca.bind("<Return>", lambda e: self._filtrar())

        ctk.CTkButton(
            topo, text="Buscar", width=80, height=36,
            fg_color=get_color("accent"), hover_color=get_color("accent_hover"),
            corner_radius=10, command=self._filtrar,
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            topo, text="Limpar", width=70, height=36,
            fg_color=get_color("text_secondary"), hover_color="#4B5563",
            corner_radius=10, command=self._limpar,
        ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(
            topo, text="＋  Novo Usuário", height=36,
            fg_color=get_color("success"), hover_color=get_color("success_hover"),
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._novo,
        ).pack(side="right")

        self._lbl_cont = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), text_color=self._muted,
        )
        self._lbl_cont.pack(anchor="w", pady=(0, 4))

        self._lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._lista.pack(fill="both", expand=True)

        self._render()
        # ── BACK ──────────────────────────────────────────────────────────
        # self.usuarios = listar(); self._render()

    def _filtrar(self):
        self._filtro = self._busca.get().strip().lower(); self._render()

    def _limpar(self):
        self._filtro = ""; self._busca.delete(0, "end"); self._render()

    def _render(self):
        for w in self._lista.winfo_children():
            w.destroy()

        items = (
            [u for u in self.usuarios if self._filtro in u["nome"].lower()]
            if self._filtro else self.usuarios
        )
        total = len(items)
        self._lbl_cont.configure(
            text=f"{total} usuário{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}"
        )

        if not items:
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="👥", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(f, text="Nenhum usuário cadastrado", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(8, 4))
            ctk.CTkLabel(f, text="Clique em '＋ Novo Usuário' para começar.", font=ctk.CTkFont(size=13), text_color=self._muted).pack()
            return

        for u in items:
            _CardUsuario(
                self._lista, u,
                on_editar=lambda u=u: self._editar(u),
                on_remover=lambda u=u: self._remover(u),
            )

    def _novo(self):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            self.usuarios.append(dados)
            # ── BACK ──────────────────────────────────────────────────────
            # novo = salvar(dados); self.usuarios.append(novo)
            self._render()
        self._abrir_popup(None, salvar)

    def _editar(self, u: dict):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            u.update(dados)
            # ── BACK ──────────────────────────────────────────────────────
            # atualizar(u["id"], dados)
            self._render()
        self._abrir_popup(u, salvar)

    def _remover(self, u: dict):
        def ok():
            self.usuarios.remove(u)
            # ── BACK ──────────────────────────────────────────────────────
            # del_usuario(u["id"])
            self._render()
        _confirmar_remocao(self, u["nome"], ok, self._panel)

    def _abrir_popup(self, usuario, on_salvar):
        popup = ctk.CTkToplevel(self)
        popup.title("Novo Usuário" if not usuario else "Editar Usuário")
        popup.geometry("420x580")
        popup.resizable(False, False)
        popup.grab_set()
        popup.configure(fg_color=self._panel)

        def _fechar():
            self._popup_aberto = False
            popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", _fechar)

        frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            frame,
            text="Novo Usuário" if not usuario else "Editar Usuário",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=get_color("text"),
        ).pack(anchor="w", pady=(0, 12))

        _secao(frame, "Dados Pessoais", self._muted)
        nome_e  = _campo(frame, "Nome completo *", "Ex: Maria Souza", self._muted)
        cpf_e   = _campo(frame, "CPF", "000.000.000-00", self._muted)

        def _mask_cpf(e):
            v = _formatar_cpf(cpf_e.get())
            cpf_e.delete(0, "end"); cpf_e.insert(0, v)
        cpf_e.bind("<KeyRelease>", _mask_cpf)

        _secao(frame, "Acesso", self._muted)
        login_e = _campo(frame, "Login *", "usuario.login", self._muted)
        tipo_var = ctk.StringVar(value=TIPOS_USUARIO[0])
        _select(frame, "Tipo *", TIPOS_USUARIO, tipo_var, self._muted)

        _secao(frame, "Senha", self._muted)
        senha_e    = _campo(frame, "Senha *", "••••••••", self._muted)
        senha_e.configure(show="●")
        confirma_e = _campo(frame, "Confirmar senha *", "••••••••", self._muted)
        confirma_e.configure(show="●")

        if usuario:
            nome_e.insert(0, usuario.get("nome", ""))
            cpf_e.insert(0, usuario.get("cpf", ""))
            login_e.insert(0, usuario.get("login", ""))
            tipo_var.set(usuario.get("tipo", TIPOS_USUARIO[0]))
            senha_e.insert(0, usuario.get("senha", ""))
            confirma_e.insert(0, usuario.get("senha", ""))
            ctk.CTkLabel(
                frame, text="Deixe a senha em branco para manter a atual.",
                font=ctk.CTkFont(size=11), text_color=self._muted,
            ).pack(anchor="w")

        erro = ctk.CTkLabel(frame, text="", text_color=get_color("danger"))
        erro.pack(pady=(8, 0))

        def _salvar():
            nome  = nome_e.get().strip()
            login = login_e.get().strip()
            senha = senha_e.get()
            conf  = confirma_e.get()
            if not nome:  erro.configure(text="⚠  Nome é obrigatório."); return
            if not login: erro.configure(text="⚠  Login é obrigatório."); return
            if not usuario and not senha: erro.configure(text="⚠  Senha é obrigatória."); return
            if senha and senha != conf:   erro.configure(text="⚠  As senhas não coincidem."); return
            dados = {
                "nome":  nome,
                "cpf":   cpf_e.get().strip(),
                "login": login,
                "tipo":  tipo_var.get(),
            }
            if senha:
                dados["senha"] = senha   # hash no back-end
            on_salvar(dados)
            _fechar()

        ctk.CTkButton(
            frame, text="Salvar",
            fg_color=get_color("success"), hover_color=get_color("success_hover"),
            height=40, corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=_salvar,
        ).pack(fill="x", pady=(12, 4))

        ctk.CTkButton(
            frame, text="Cancelar",
            fg_color="transparent", border_width=1,
            border_color=get_color("border"), text_color=self._muted,
            height=36, corner_radius=10, command=_fechar,
        ).pack(fill="x", pady=(0, 8))


# ═════════════════════════════════════════════════════════════════════════════
# ABA: MÉDICOS
# ═════════════════════════════════════════════════════════════════════════════

def _formatar_crm(texto: str) -> str:
    """Mantém só dígitos, aceita letras UF no formato CRM/UF."""
    # Remove tudo exceto dígitos e letras (para suportar CRM/SP, CRM/RJ etc.)
    limpo = "".join(c for c in texto if c.isalnum() or c in "/-")
    return limpo[:10]


class _CardMedico(_CardBase):
    def __init__(self, parent, m: dict, on_editar, on_remover):
        self._m = m
        iniciais = "".join(
            m["nome"].replace("Dr.", "").replace("Dra.", "").split()[:2]
        ).upper()[:2]
        super().__init__(parent, on_editar, on_remover, get_color("success"), iniciais)

    def _build_info(self):
        m = self._m
        linha1 = ctk.CTkFrame(self._info, fg_color="transparent")
        linha1.pack(anchor="w", fill="x")

        ctk.CTkLabel(
            linha1, text=m["nome"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=get_color("text"),
        ).pack(side="left")

        badge = ctk.CTkFrame(linha1, fg_color=get_color("success"), corner_radius=10)
        badge.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(
            badge, text=f"  {m.get('especialidade', '—')}  ",
            font=ctk.CTkFont(size=10, weight="bold"), text_color="white",
        ).pack()

        status = m.get("status", "Ativo")
        s_cor = get_color("success") if status == "Ativo" else "#D97706"
        s_badge = ctk.CTkFrame(linha1, fg_color=s_cor, corner_radius=10)
        s_badge.pack(side="left", padx=(6, 0))
        ctk.CTkLabel(
            s_badge, text=f"  {status}  ",
            font=ctk.CTkFont(size=10, weight="bold"), text_color="white",
        ).pack()

        ctk.CTkLabel(
            self._info,
            text=f"CRM: {m.get('crm', '—')}   ·   Consultório: {m.get('consultorio', '—')}",
            font=ctk.CTkFont(size=12), text_color=get_color("text_secondary"),
        ).pack(anchor="w", pady=(3, 0))


class AbaMedicos(ctk.CTkFrame):
    def __init__(self, master, panel: str, muted: str):
        super().__init__(master, fg_color="transparent")
        self._panel = panel
        self._muted = muted
        self.medicos: list[dict] = []
        self._popup_aberto = False
        self._filtro = ""
        self._build()

    def _build(self):
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 8))

        self._busca = ctk.CTkEntry(
            topo, placeholder_text="🔍  Buscar médico...",
            height=36, corner_radius=10, font=ctk.CTkFont(size=13),
        )
        self._busca.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._busca.bind("<Return>", lambda e: self._filtrar())

        ctk.CTkButton(
            topo, text="Buscar", width=80, height=36,
            fg_color=get_color("accent"), hover_color=get_color("accent_hover"),
            corner_radius=10, command=self._filtrar,
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            topo, text="Limpar", width=70, height=36,
            fg_color=get_color("text_secondary"), hover_color="#4B5563",
            corner_radius=10, command=self._limpar,
        ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(
            topo, text="＋  Novo Médico", height=36,
            fg_color=get_color("success"), hover_color=get_color("success_hover"),
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._novo,
        ).pack(side="right")

        self._lbl_cont = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), text_color=self._muted,
        )
        self._lbl_cont.pack(anchor="w", pady=(0, 4))

        self._lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._lista.pack(fill="both", expand=True)
        self._render()
        # ── BACK ──────────────────────────────────────────────────────────
        # self.medicos = listar(); self._render()

    def _filtrar(self):
        self._filtro = self._busca.get().strip().lower(); self._render()

    def _limpar(self):
        self._filtro = ""; self._busca.delete(0, "end"); self._render()

    def _render(self):
        for w in self._lista.winfo_children():
            w.destroy()
        items = (
            [m for m in self.medicos if self._filtro in m["nome"].lower()]
            if self._filtro else self.medicos
        )
        total = len(items)
        self._lbl_cont.configure(
            text=f"{total} médico{'s' if total != 1 else ''} encontrado{'s' if total != 1 else ''}"
        )
        if not items:
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="👨‍⚕️", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(f, text="Nenhum médico cadastrado", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(8, 4))
            ctk.CTkLabel(f, text="Clique em '＋ Novo Médico' para cadastrar.", font=ctk.CTkFont(size=13), text_color=self._muted).pack()
            return
        for m in items:
            _CardMedico(self._lista, m, lambda m=m: self._editar(m), lambda m=m: self._remover(m))

    def _novo(self):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            self.medicos.append(dados)
            # ── BACK ──────────────────────────────────────────────────────
            # novo = salvar(dados); self.medicos.append(novo)
            self._render()
        self._abrir_popup(None, salvar)

    def _editar(self, m: dict):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            m.update(dados)
            # ── BACK ──────────────────────────────────────────────────────
            # atualizar(m["id"], dados)
            self._render()
        self._abrir_popup(m, salvar)

    def _remover(self, m: dict):
        def ok():
            self.medicos.remove(m)
            # ── BACK ──────────────────────────────────────────────────────
            # del_medico(m["id"])
            self._render()
        _confirmar_remocao(self, m["nome"], ok, self._panel)

    def _abrir_popup(self, medico, on_salvar):
        popup = ctk.CTkToplevel(self)
        popup.title("Novo Médico" if not medico else "Editar Médico")
        popup.geometry("420x540")
        popup.resizable(False, False)
        popup.grab_set()
        popup.configure(fg_color=self._panel)

        def _fechar():
            self._popup_aberto = False; popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", _fechar)

        frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            frame,
            text="Novo Médico" if not medico else "Editar Médico",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=get_color("text"),
        ).pack(anchor="w", pady=(0, 12))

        _secao(frame, "Dados do Médico", self._muted)
        nome_e = _campo(frame, "Nome completo *", "Dr(a). Nome Sobrenome", self._muted)
        esp_var = ctk.StringVar(value=ESPECIALIDADES[0])
        _select(frame, "Especialidade *", ESPECIALIDADES, esp_var, self._muted)

        _secao(frame, "Registro e Localização", self._muted)
        crm_e  = _campo(frame, "CRM *", "000000", self._muted)
        cons_e = _campo(frame, "Número do Consultório *", "Ex: 101", self._muted)

        def _mask_crm(e):
            valor_atual = crm_e.get()
            formatado = _formatar_crm(valor_atual)
            if formatado != valor_atual:
                pos = crm_e.index("insert")
                crm_e.delete(0, "end")
                crm_e.insert(0, formatado)
                crm_e.icursor(min(pos, len(formatado)))
        crm_e.bind("<KeyRelease>", _mask_crm)

        _secao(frame, "Status", self._muted)
        status_var = ctk.StringVar(value="Ativo")
        _select(frame, "Status", STATUS_OPTS, status_var, self._muted)

        if medico:
            nome_e.insert(0, medico.get("nome", ""))
            esp_var.set(medico.get("especialidade", ESPECIALIDADES[0]))
            crm_e.insert(0, medico.get("crm", ""))
            cons_e.insert(0, medico.get("consultorio", ""))
            status_var.set(medico.get("status", "Ativo"))

        erro = ctk.CTkLabel(frame, text="", text_color=get_color("danger"))
        erro.pack(pady=(8, 0))

        def _salvar():
            nome = nome_e.get().strip(); crm = crm_e.get().strip(); cons = cons_e.get().strip()
            if not nome: erro.configure(text="⚠  Nome é obrigatório."); return
            if not crm:  erro.configure(text="⚠  CRM é obrigatório."); return
            if not cons: erro.configure(text="⚠  Consultório é obrigatório."); return
            dados = {
                "nome": nome, "especialidade": esp_var.get(),
                "crm": crm, "consultorio": cons, "status": status_var.get(),
            }
            on_salvar(dados); _fechar()

        ctk.CTkButton(
            frame, text="Salvar",
            fg_color=get_color("success"), hover_color=get_color("success_hover"),
            height=40, corner_radius=10, font=ctk.CTkFont(size=14, weight="bold"),
            command=_salvar,
        ).pack(fill="x", pady=(12, 4))
        ctk.CTkButton(
            frame, text="Cancelar",
            fg_color="transparent", border_width=1,
            border_color=get_color("border"), text_color=self._muted,
            height=36, corner_radius=10, command=_fechar,
        ).pack(fill="x", pady=(0, 8))


# ═════════════════════════════════════════════════════════════════════════════
# ABA: PLANOS
# ═════════════════════════════════════════════════════════════════════════════

class _CardPlano(_CardBase):
    def __init__(self, parent, p: dict, on_editar, on_remover):
        self._p = p
        super().__init__(parent, on_editar, on_remover, "#0891B2", p["nome"][:2].upper())

    def _build_info(self):
        p = self._p
        linha1 = ctk.CTkFrame(self._info, fg_color="transparent")
        linha1.pack(anchor="w", fill="x")
        ctk.CTkLabel(
            linha1, text=p["nome"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=get_color("text"),
        ).pack(side="left")
        status = p.get("status", "Ativo")
        s_cor = get_color("success") if status == "Ativo" else "#D97706"
        badge = ctk.CTkFrame(linha1, fg_color=s_cor, corner_radius=10)
        badge.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(badge, text=f"  {status}  ", font=ctk.CTkFont(size=10, weight="bold"), text_color="white").pack()
        ctk.CTkLabel(
            self._info, text="Plano de saúde conveniado",
            font=ctk.CTkFont(size=12), text_color=get_color("text_secondary"),
        ).pack(anchor="w", pady=(3, 0))


class AbaPlanos(ctk.CTkFrame):
    def __init__(self, master, panel: str, muted: str):
        super().__init__(master, fg_color="transparent")
        self._panel = panel; self._muted = muted
        self.planos: list[dict] = []
        self._popup_aberto = False
        self._build()

    def _build(self):
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 8))
        # spacer à esquerda para o frame ter largura e o botão aparecer à direita
        self._lbl_cont = ctk.CTkLabel(topo, text="", font=ctk.CTkFont(size=12), text_color=self._muted)
        self._lbl_cont.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            topo, text="＋  Novo Plano", height=36,
            fg_color=get_color("success"), hover_color=get_color("success_hover"),
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._novo,
        ).pack(side="right")
        self._lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._lista.pack(fill="both", expand=True)
        self._render()
        # ── BACK ──────────────────────────────────────────────────────────
        # self.planos = listar(); self._render()

    def _render(self):
        for w in self._lista.winfo_children(): w.destroy()
        total = len(self.planos)
        self._lbl_cont.configure(text=f"{total} plano{'s' if total != 1 else ''} cadastrado{'s' if total != 1 else ''}")
        if not self.planos:
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="🏥", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(f, text="Nenhum plano cadastrado", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(8, 4))
            ctk.CTkLabel(f, text="Clique em '＋ Novo Plano' para cadastrar.", font=ctk.CTkFont(size=13), text_color=self._muted).pack()
            return
        for pl in self.planos:
            _CardPlano(self._lista, pl, lambda pl=pl: self._editar(pl), lambda pl=pl: self._remover(pl))

    def _novo(self):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            self.planos.append(dados)
            # ── BACK ──────────────────────────────────────────────────────
            # novo = salvar(dados); self.planos.append(novo)
            self._render()
        self._abrir_popup(None, salvar)

    def _editar(self, pl: dict):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            pl.update(dados)
            # ── BACK ──────────────────────────────────────────────────────
            # atualizar(pl["id"], dados)
            self._render()
        self._abrir_popup(pl, salvar)

    def _remover(self, pl: dict):
        def ok():
            self.planos.remove(pl)
            # ── BACK ──────────────────────────────────────────────────────
            # del_plano(pl["id"])
            self._render()
        _confirmar_remocao(self, pl["nome"], ok, self._panel)

    def _abrir_popup(self, plano, on_salvar):
        popup = ctk.CTkToplevel(self)
        popup.title("Novo Plano" if not plano else "Editar Plano")
        popup.geometry("420x460")
        popup.resizable(False, False); popup.grab_set()
        popup.configure(fg_color=self._panel)

        def _fechar():
            self._popup_aberto = False; popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", _fechar)

        frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            frame, text="Novo Plano" if not plano else "Editar Plano",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=get_color("text"),
        ).pack(anchor="w", pady=(0, 12))

        _secao(frame, "Dados do Plano", self._muted)
        nome_e = _campo(frame, "Nome do plano *", "Ex: Unimed, Bradesco Saúde", self._muted)
        _secao(frame, "Status", self._muted)
        status_var = ctk.StringVar(value="Ativo")
        _select(frame, "Status", STATUS_OPTS, status_var, self._muted)

        if plano:
            nome_e.insert(0, plano.get("nome", ""))
            status_var.set(plano.get("status", "Ativo"))

        erro = ctk.CTkLabel(frame, text="", text_color=get_color("danger"))
        erro.pack(pady=(8, 0))

        def _salvar():
            nome = nome_e.get().strip()
            if not nome: erro.configure(text="⚠  Nome é obrigatório."); return
            on_salvar({"nome": nome, "status": status_var.get()})
            _fechar()

        ctk.CTkButton(frame, text="Salvar", fg_color=get_color("success"), hover_color=get_color("success_hover"), height=40, corner_radius=10, font=ctk.CTkFont(size=14, weight="bold"), command=_salvar).pack(fill="x", pady=(12, 4))
        ctk.CTkButton(frame, text="Cancelar", fg_color="transparent", border_width=1, border_color=get_color("border"), text_color=self._muted, height=36, corner_radius=10, command=_fechar).pack(fill="x", pady=(0, 8))


# ═════════════════════════════════════════════════════════════════════════════
# ABA: CONSULTÓRIOS
# ═════════════════════════════════════════════════════════════════════════════

_STATUS_CONS = ["Disponível", "Ocupado", "Em manutenção"]
_CORES_STATUS_CONS = {
    "Disponível":    get_color("success"),
    "Ocupado":       get_color("accent"),
    "Em manutenção": "#D97706",
}


class _CardConsultorio(_CardBase):
    def __init__(self, parent, c: dict, on_editar, on_remover):
        self._c = c
        super().__init__(parent, on_editar, on_remover, "#0369A1", f"#{c.get('numero', '?')}")

    def _build_info(self):
        c = self._c
        linha1 = ctk.CTkFrame(self._info, fg_color="transparent")
        linha1.pack(anchor="w", fill="x")
        ctk.CTkLabel(
            linha1, text=f"Consultório {c.get('numero', '—')}",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=get_color("text"),
        ).pack(side="left")
        status = c.get("status", "Disponível")
        s_cor = _CORES_STATUS_CONS.get(status, get_color("accent"))
        badge = ctk.CTkFrame(linha1, fg_color=s_cor, corner_radius=10)
        badge.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(badge, text=f"  {status}  ", font=ctk.CTkFont(size=10, weight="bold"), text_color="white").pack()
        ctk.CTkLabel(
            self._info, text=f"📍 {c.get('andar', '—')}",
            font=ctk.CTkFont(size=12), text_color=get_color("text_secondary"),
        ).pack(anchor="w", pady=(3, 0))


class AbaConsultorios(ctk.CTkFrame):
    def __init__(self, master, panel: str, muted: str):
        super().__init__(master, fg_color="transparent")
        self._panel = panel; self._muted = muted
        self.consultorios: list[dict] = []
        self._popup_aberto = False
        self._build()

    def _build(self):
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 8))
        # spacer à esquerda para o frame ter largura e o botão aparecer à direita
        self._lbl_cont = ctk.CTkLabel(topo, text="", font=ctk.CTkFont(size=12), text_color=self._muted)
        self._lbl_cont.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            topo, text="＋  Novo Consultório", height=36,
            fg_color=get_color("success"), hover_color=get_color("success_hover"),
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._novo,
        ).pack(side="right")
        self._lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._lista.pack(fill="both", expand=True)
        self._render()
        # ── BACK ──────────────────────────────────────────────────────────
        # self.consultorios = listar(); self._render()

    def _render(self):
        for w in self._lista.winfo_children(): w.destroy()
        total = len(self.consultorios)
        self._lbl_cont.configure(text=f"{total} consultório{'s' if total != 1 else ''} cadastrado{'s' if total != 1 else ''}")
        if not self.consultorios:
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="🚪", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(f, text="Nenhum consultório cadastrado", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(8, 4))
            ctk.CTkLabel(f, text="Clique em '＋ Novo Consultório' para cadastrar.", font=ctk.CTkFont(size=13), text_color=self._muted).pack()
            return
        for c in self.consultorios:
            _CardConsultorio(self._lista, c, lambda c=c: self._editar(c), lambda c=c: self._remover(c))

    def _novo(self):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            self.consultorios.append(dados)
            # ── BACK ──────────────────────────────────────────────────────
            # novo = salvar(dados); self.consultorios.append(novo)
            
            numero = dados['numero']
            andar = dados['andar']
            #if numero or andar is not int:
            #    return
            _dados = (numero, andar)
            print(_dados)
            print(dados)
            self._render()
        self._abrir_popup(None, salvar)

    def _editar(self, c: dict):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            c.update(dados)
            # ── BACK ──────────────────────────────────────────────────────
            # atualizar(c["id"], dados)
            self._render()
        self._abrir_popup(c, salvar)

    def _remover(self, c: dict):
        def ok():
            self.consultorios.remove(c)
            # ── BACK ──────────────────────────────────────────────────────
            # del_cons(c["id"])
            self._render()
        _confirmar_remocao(self, f"Consultório {c.get('numero', '')}", ok, self._panel)

    def _abrir_popup(self, cons, on_salvar):
        popup = ctk.CTkToplevel(self)
        popup.title("Novo Consultório" if not cons else "Editar Consultório")
        popup.geometry("420x500")
        popup.resizable(False, False); popup.grab_set()
        popup.configure(fg_color=self._panel)

        def _fechar():
            self._popup_aberto = False; popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", _fechar)

        frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            frame, text="Novo Consultório" if not cons else "Editar Consultório",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=get_color("text"),
        ).pack(anchor="w", pady=(0, 12))

        _secao(frame, "Identificação", self._muted)
        num_e   = _campo(frame, "Número do consultório *", "Ex: 101", self._muted)
        andar_e = _campo(frame, "Andar *", "Ex: 1º andar", self._muted)
        _secao(frame, "Status", self._muted)
        status_var = ctk.StringVar(value="Disponível")
        _select(frame, "Status", _STATUS_CONS, status_var, self._muted)

        if cons:
            num_e.insert(0, cons.get("numero", ""))
            andar_e.insert(0, cons.get("andar", ""))
            status_var.set(cons.get("status", "Disponível"))

        erro = ctk.CTkLabel(frame, text="", text_color=get_color("danger"))
        erro.pack(pady=(8, 0))

        def _salvar():
            try:
                num = int(num_e.get().strip()); andar = int(andar_e.get().strip())
            except Exception as e:
                erro.configure(text="Andar ou número de consultório inválidos.")
                return
            if not num:   erro.configure(text="⚠  Número é obrigatório."); return
            if not andar: erro.configure(text="⚠  Andar é obrigatório."); return
            on_salvar({"numero": num, "andar": andar, "status": status_var.get()})
            _fechar()

        ctk.CTkButton(frame, text="Salvar", fg_color=get_color("success"), hover_color=get_color("success_hover"), height=40, corner_radius=10, font=ctk.CTkFont(size=14, weight="bold"), command=_salvar).pack(fill="x", pady=(12, 4))
        ctk.CTkButton(frame, text="Cancelar", fg_color="transparent", border_width=1, border_color=get_color("border"), text_color=self._muted, height=36, corner_radius=10, command=_fechar).pack(fill="x", pady=(0, 8))


# ═════════════════════════════════════════════════════════════════════════════
# VIEW PRINCIPAL – CONFIGURAÇÕES
# ═════════════════════════════════════════════════════════════════════════════

_ABAS = [
    ("👥",     "Usuários"),
    ("👨‍⚕️",   "Médicos"),
    ("🏥",     "Planos"),
    ("🚪",     "Consultórios"),
]


class ConfiguracoesView(ctk.CTkFrame):
    """
    Substitui o UsersView original.
    Mantém o mesmo padrão visual (get_color / theme) e adiciona
    abas para Médicos, Planos e Consultórios.

    Uso:  ConfiguracoesView(master)  — igual ao UsersView anterior.
    """

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.bg    = get_color("bg")
        self.panel = get_color("panel")
        self.text  = get_color("text")
        self.muted = get_color("text_secondary")

        self.configure(fg_color=self.bg)
        self._aba_ativa = 0
        self._build()

    def _build(self):
        # ── Cabeçalho (mesmo estilo do UsersView original) ──────────────────
        header = ctk.CTkFrame(self, fg_color=self.panel, corner_radius=18, height=70)
        header.pack(fill="x", padx=18, pady=(18, 10))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="⚙️  Configurações",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.text,
        ).place(x=20, y=14)

        ctk.CTkLabel(
            header,
            text="Gerencie usuários, médicos, planos e consultórios",
            font=ctk.CTkFont(size=12),
            text_color=self.muted,
        ).place(x=20, y=42)

        # ── Abas ─────────────────────────────────────────────────────────────
        abas_row = ctk.CTkFrame(self, fg_color="transparent")
        abas_row.pack(fill="x", padx=18, pady=(0, 6))

        self._btns_aba: list[ctk.CTkButton] = []
        for i, (icone, nome) in enumerate(_ABAS):
            ativo = i == 0
            btn = ctk.CTkButton(
                abas_row,
                text=f"{icone}  {nome}",
                height=34, corner_radius=10,
                font=ctk.CTkFont(size=13),
                fg_color=get_color("accent") if ativo else "transparent",
                hover_color=get_color("accent_hover") if ativo else get_color("panel"),
                text_color="white" if ativo else self.muted,
                command=lambda i=i: self._trocar_aba(i),
            )
            btn.pack(side="left", padx=(0, 6))
            self._btns_aba.append(btn)

        # Divisor
        ctk.CTkFrame(self, height=1, fg_color=get_color("border")).pack(
            fill="x", padx=18, pady=(0, 8)
        )

        # ── Conteúdo ──────────────────────────────────────────────────────────
        conteudo = ctk.CTkFrame(self, fg_color="transparent")
        conteudo.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        self._abas_frames: dict[int, ctk.CTkFrame] = {
            0: AbaUsuarios(conteudo, self.panel, self.muted),
            1: AbaMedicos(conteudo, self.panel, self.muted),
            2: AbaPlanos(conteudo, self.panel, self.muted),
            3: AbaConsultorios(conteudo, self.panel, self.muted),
        }

        for i, frame in self._abas_frames.items():
            if i == 0:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def _trocar_aba(self, idx: int):
        if idx == self._aba_ativa:
            return
        for i, btn in enumerate(self._btns_aba):
            ativo = i == idx
            btn.configure(
                fg_color=get_color("accent") if ativo else "transparent",
                hover_color=get_color("accent_hover") if ativo else get_color("panel"),
                text_color="white" if ativo else self.muted,
            )
        self._abas_frames[self._aba_ativa].pack_forget()
        self._abas_frames[idx].pack(fill="both", expand=True)
        self._aba_ativa = idx