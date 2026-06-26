import customtkinter as ctk
from .theme import get_color
from .loading_overlay import LoadingOverlay

# ─────────────────────────────────────────────────────────────────────────────
# BACK-END 
from controllers.usuario_controller     import adicionar as salvar_usuario, listar as listar_usuarios, editar as editar_usuario, remover as remover_usuario
from controllers.medico_controller import salvar as salvar_medico, listar as listar_medico, lista_consultorios, atualizar as atualizar_medico, remover as remover_medico, vincular_medico_usuario
from controllers.plano_controller       import adicionar as salvar_plano, listar as listar_planos, editar as editar_planos, remover as remover_plano
from controllers.consultorio_controller import salvar as salvar_consultorio, listar as listar_consultorios, atualizar as editar_consutorio, remover as remover_consultorio
# ─────────────────────────────────────────────────────────────────────────────

ESPECIALIDADES = [
    "Clínica Geral", "Cardiologia", "Dermatologia", "Ginecologia",
    "Neurologia", "Oftalmologia", "Ortopedia", "Pediatria",
    "Psiquiatria", "Urologia", "Outra",
]

TIPOS_USUARIO = ["admin", "medico", "atendente"]
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

        # Overlay de loading desta aba. Cada aba tem sua própria instância
        # porque cada uma é um CTkFrame independente — o overlay precisa
        # cobrir a área da aba ativa, não a ConfiguracoesView inteira.
        self.loading = LoadingOverlay(self)

        self._render()

    def _filtrar(self):
        self._filtro = self._busca.get().strip().lower(); self._render()

    def _limpar(self):
        self._filtro = ""; self._busca.delete(0, "end"); self._render()

    def _render(self):
        for w in self._lista.winfo_children():
            w.destroy()

        # ------------------------------------------------------------------
        # ANTES: "self.usuarios = listar_usuarios()" rodava direto aqui,
        # travando a tela até o MySQL na nuvem responder.
        #
        # AGORA: mesma chamada, em thread separada via run_async. O
        # filtro por nome e a montagem dos cards continuam idênticos,
        # só que dentro de _ao_concluir.
        # ------------------------------------------------------------------
        def _ao_concluir(usuarios):
            self.usuarios = usuarios

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

        def _ao_erro(erro):
            self._lbl_cont.configure(text="Erro ao carregar usuários")
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="⚠️", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(
                f, text=f"Não foi possível carregar os usuários.\n{erro}",
                font=ctk.CTkFont(size=13), text_color=get_color("danger"),
            ).pack(pady=(8, 4))

        self.loading.run_async(
            tarefa=listar_usuarios,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando usuários...",
        )

    def _novo(self):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):

            # ── BACK ──────────────────────────────────────────────────────
            nome = dados['nome']
            cpf = dados['cpf']
            login = dados['login']
            tipo = dados['tipo']
            senha = dados['senha']
            id_medico_selecionado = dados.get('id_medico_selecionado')
            _dados = (nome, cpf, login, tipo, senha)

            # ------------------------------------------------------------
            # Salva o usuário e, se for do tipo "medico" com um médico
            # selecionado, encadeia o vínculo na mesma operação assíncrona:
            # salvar_usuario precisa RETORNAR o id_usuario recém-criado
            # para que vincular_medico_usuario(id_medico, id_usuario)
            # saiba a quem vincular. As duas chamadas rodam na mesma
            # thread em segundo plano — só uma exibição de loading do
            # início ao fim das duas.
            # ------------------------------------------------------------
            def _tarefa():
                novo_id_usuario = salvar_usuario(_dados)
                print("DEBUG -> novo_id_usuario:", novo_id_usuario, "| id_medico_selecionado:", id_medico_selecionado)
                if id_medico_selecionado is not None:
                    vincular_medico_usuario(id_medico=id_medico_selecionado, id_usuario=novo_id_usuario)
                    print("DEBUG -> vincular_medico_usuario executado SEM erro")
                return novo_id_usuario

            def _ao_erro(erro):
                print("Erro ao salvar usuário:", erro)

            self.loading.run_async(
                tarefa=_tarefa,
                ao_concluir=lambda resultado: self._render(),
                ao_erro=_ao_erro,
                mensagem="Salvando usuário...",
            )
        self._abrir_popup(None, salvar)

    def _editar(self, u: dict):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            u.update(dados)
            # ── BACK ──────────────────────────────────────────────────────
            id_usuario = u["id_usuario"]
            nome = dados['nome']
            cpf = dados['cpf']
            login = dados['login']
            tipo = dados['tipo']
            senha = dados['senha']
            id_medico_selecionado = dados.get('id_medico_selecionado')
            _dados = (nome, cpf, login, tipo, senha)

            # Edição: id_usuario já existe, então o vínculo (se aplicável)
            # roda na sequência, sem precisar de retorno do editar_usuario.
            def _tarefa():
                resultado = editar_usuario(id_usuario, _dados)
                if id_medico_selecionado is not None:
                    vincular_medico_usuario(id_medico_selecionado, id_usuario)
                return resultado

            def _ao_erro(erro):
                print("Erro ao editar usuário:", erro)

            self.loading.run_async(
                tarefa=_tarefa,
                ao_concluir=lambda resultado: self._render(),
                ao_erro=_ao_erro,
                mensagem="Salvando usuário...",
            )
        self._abrir_popup(u, salvar)

    def _remover(self, u: dict):
        def ok():
            # ── BACK ──────────────────────────────────────────────────────
            id_usuario = u["id_usuario"]

            def _ao_erro(erro):
                print("Erro ao remover usuário:", erro)

            self.loading.run_async(
                tarefa=lambda: remover_usuario(id_usuario),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=_ao_erro,
                mensagem="Removendo usuário...",
            )
        _confirmar_remocao(self, u["nome"], ok, self._panel)

    def _abrir_popup(self, usuario, on_salvar):
        popup = ctk.CTkToplevel(self)
        popup.title("Novo Usuário" if not usuario else "Editar Usuário")
        popup.geometry("420x640")
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

        # Se o usuário editado já é do tipo "medico", o campo Tipo fica
        # travado — não dá pra trocar o tipo de um médico já vinculado
        # por aqui, pra não deixar um médico "pendurado" sem login ou um
        # vínculo apontando para um tipo que não existe mais. A única
        # forma de mudar isso seria uma ação administrativa separada,
        # fora desta tela.
        tipo_ja_e_medico = bool(usuario) and usuario.get("tipo") == "medico"

        tipo_var = ctk.StringVar(value=TIPOS_USUARIO[0])
        tipo_menu = _select(frame, "Tipo *", TIPOS_USUARIO, tipo_var, self._muted)
        if tipo_ja_e_medico:
            tipo_menu.configure(state="disabled")
            ctk.CTkLabel(
                frame, text="Tipo 'medico' não pode ser alterado por aqui.",
                font=ctk.CTkFont(size=11), text_color=self._muted,
            ).pack(anchor="w")

        # ---- Vínculo com médico (aparece só quando Tipo = medico) ----------
        secao_medico_frame = ctk.CTkFrame(frame, fg_color="transparent")
        medico_var = ctk.StringVar(value="")
        medico_menu = None
        label_medico_erro = None

        # id_medico do médico atualmente vinculado a este usuário (edição).
        # Descoberto dentro da própria lista de médicos (filtrando por
        # id_usuario == usuario["id_usuario"]) quando ela chegar do
        # backend — não depende de nenhum campo extra em listar_usuarios().
        id_medico_vinculado_atual = None

        # Mapa nome_exibido -> id_medico, preenchido depois que a lista de
        # médicos chega do backend.
        mapa_medico_por_nome = {}

        def _popular_dropdown_medicos(lista_medicos):
            nonlocal medico_menu, label_medico_erro, id_medico_vinculado_atual
            mapa_medico_por_nome.clear()

            # Descobre, dentro da lista recebida, se algum médico já está
            # vinculado a este usuário em edição (id_usuario == este usuário).
            if usuario:
                for m in lista_medicos:
                    if m.get("id_usuario") == usuario.get("id_usuario"):
                        id_medico_vinculado_atual = m.get("id_medico")
                        break

            # Só entram no dropdown: médicos sem usuário vinculado (livres)
            # OU o médico que já é o vinculado deste usuário em edição
            # (pra não "desaparecer" a seleção atual ao editar).
            disponiveis = [
                m for m in lista_medicos
                if m.get("id_usuario") is None or m.get("id_medico") == id_medico_vinculado_atual
            ]

            for w in secao_medico_frame.winfo_children():
                w.destroy()

            if not disponiveis:
                ctk.CTkLabel(
                    secao_medico_frame,
                    text="Nenhum médico disponível para vincular (todos já têm login).",
                    font=ctk.CTkFont(size=12), text_color=get_color("danger"), wraplength=360,
                ).pack(anchor="w", pady=(4, 0))
                return

            nomes = [m["nome"] for m in disponiveis]
            for m in disponiveis:
                mapa_medico_por_nome[m["nome"]] = m["id_medico"]

            valor_inicial = nomes[0]
            if usuario:
                for m in disponiveis:
                    if m.get("id_medico") == id_medico_vinculado_atual:
                        valor_inicial = m["nome"]
                        break
            medico_var.set(valor_inicial)

            medico_menu = _select(
                secao_medico_frame, "Qual médico é esse? *", nomes, medico_var, self._muted,
            )

        def _atualizar_visibilidade_medico(*_):
            if tipo_var.get() == "medico":
                secao_medico_frame.pack(fill="x", pady=(0, 6))
            else:
                secao_medico_frame.pack_forget()

        tipo_var.trace_add("write", _atualizar_visibilidade_medico)

        # Busca a lista de médicos assim que o popup abre — precisa vir
        # do backend (envolve rede), então roda via run_async com o
        # loading overlay já existente nesta aba.
        def _ao_concluir_medicos(lista_medicos):
            _popular_dropdown_medicos(lista_medicos)
            _atualizar_visibilidade_medico()

        def _ao_erro_medicos(erro):
            ctk.CTkLabel(
                secao_medico_frame,
                text=f"Erro ao carregar médicos: {erro}",
                font=ctk.CTkFont(size=12), text_color=get_color("danger"), wraplength=360,
            ).pack(anchor="w")
            _atualizar_visibilidade_medico()

        self.loading.run_async(
            tarefa=listar_medico,
            ao_concluir=_ao_concluir_medicos,
            ao_erro=_ao_erro_medicos,
            mensagem="Carregando médicos...",
        )

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
            cpf = cpf_e.get().strip()
            login = login_e.get().strip()
            senha = senha_e.get()
            conf  = confirma_e.get()
            if not nome:  erro.configure(text="⚠  Nome é obrigatório."); return
            if not login: erro.configure(text="⚠  Login é obrigatório."); return
            if not cpf: erro.configure(text="⚠  CPF é obrigatório."); return
            if not usuario and not senha: erro.configure(text="⚠  Senha é obrigatória."); return
            if senha and senha != conf:   erro.configure(text="⚠  As senhas não coincidem."); return

            tipo_escolhido = tipo_var.get()
            id_medico_selecionado = None
            if tipo_escolhido == "medico":
                nome_medico_escolhido = medico_var.get()
                id_medico_selecionado = mapa_medico_por_nome.get(nome_medico_escolhido)
                if id_medico_selecionado is None:
                    erro.configure(text="⚠  Selecione qual médico é este usuário.")
                    return

            dados = {
                "nome":  nome,
                "cpf": cpf,
                "login": login,
                "tipo":  tipo_escolhido,
                "id_medico_selecionado": id_medico_selecionado,
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
        # Lista de consultórios carregada uma única vez (junto com a
        # listagem inicial de médicos), e reaproveitada em memória no
        # popup de salvar/editar — sem nova ida à rede a cada vez que o
        # popup é aberto ou salvo, igual ao padrão já usado na AgendaView
        # com dados_medico/dados_paciente.
        self.consultorios_disponiveis: list[dict] = []
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

        # Overlay de loading desta aba (mesma observação da AbaUsuarios).
        self.loading = LoadingOverlay(self)

        self._carregar_dados_iniciais()

    def _carregar_dados_iniciais(self):
        """Busca médicos E consultórios juntos, numa única ida à nuvem,
        na abertura da aba. self.consultorios_disponiveis fica em memória
        e é reaproveitada no popup de salvar/editar médico — sem precisar
        buscar de novo a cada vez que o popup abre ou salva."""

        def _tarefa():
            medicos = listar_medico()
            consultorios = lista_consultorios()
            return medicos, consultorios

        def _ao_concluir(resultado):
            medicos, consultorios = resultado
            self.consultorios_disponiveis = consultorios
            self._aplicar_lista_medicos(medicos)

        def _ao_erro(erro):
            self._lbl_cont.configure(text="Erro ao carregar médicos")
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="⚠️", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(
                f, text=f"Não foi possível carregar os médicos.\n{erro}",
                font=ctk.CTkFont(size=13), text_color=get_color("danger"),
            ).pack(pady=(8, 4))

        self.loading.run_async(
            tarefa=_tarefa,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando médicos...",
        )

    def _filtrar(self):
        self._filtro = self._busca.get().strip().lower(); self._render()

    def _limpar(self):
        self._filtro = ""; self._busca.delete(0, "end"); self._render()

    def _render(self):
        """Busca médicos atualizados no banco (consultórios continuam só
        em memória, não são buscados de novo aqui) — usado em filtro,
        limpar busca, e depois de salvar/editar/remover médico."""
        for w in self._lista.winfo_children():
            w.destroy()

        def _ao_concluir(medicos):
            self.medicos = medicos
            print(self.medicos)
            self._aplicar_lista_medicos(medicos)

        def _ao_erro(erro):
            self._lbl_cont.configure(text="Erro ao carregar médicos")
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="⚠️", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(
                f, text=f"Não foi possível carregar os médicos.\n{erro}",
                font=ctk.CTkFont(size=13), text_color=get_color("danger"),
            ).pack(pady=(8, 4))

        self.loading.run_async(
            tarefa=listar_medico,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando médicos...",
        )

    def _aplicar_lista_medicos(self, medicos):
        """Filtra pelo termo de busca e desenha os cards. Separado de
        _render()/_carregar_dados_iniciais() porque os dois precisam
        terminar com o mesmo resultado visual, vindo de caminhos
        diferentes (com ou sem busca de consultórios)."""
        self.medicos = medicos

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
            # ── BACK ──────────────────────────────────────────────────────
            nome = dados['nome']
            especialidade = dados['especialidade']
            crm = dados['crm']
            id_consultorio = dados['id_consultorio']
            _dados = (nome, especialidade, crm, id_consultorio)
            print(_dados)

            self.loading.run_async(
                tarefa=lambda: salvar_medico(_dados),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao salvar médico:", erro),
                mensagem="Salvando médico...",
            )
        self._abrir_popup(None, salvar)

    def _editar(self, m: dict):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):

            # ── BACK ──────────────────────────────────────────────────────
            id_medico = m["id"]
            nome = dados['nome']
            especialidade = dados['especialidade']
            crm = dados['crm']
            id_consultorio = dados['id_consultorio']
            _dados = (nome, especialidade, crm, id_consultorio)

            self.loading.run_async(
                tarefa=lambda: atualizar_medico(_dados, id_medico),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao editar médico:", erro),
                mensagem="Salvando médico...",
            )
        self._abrir_popup(m, salvar)

    def _remover(self, m: dict):
        def ok():
            # ── BACK ──────────────────────────────────────────────────────
            id_medico = m['id_medico']

            self.loading.run_async(
                tarefa=lambda: remover_medico(id_medico),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao remover médico:", erro),
                mensagem="Removendo médico...",
            )
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
            nome_e.insert(0, str(medico.get("nome") or ""))
            esp_var.set(medico.get("especialidade") or ESPECIALIDADES[0])
            crm_e.insert(0, str(medico.get("crm") or ""))
            # "consultorio" pode vir como int (número) ou None do banco —
            # CTkEntry.insert exige string, então converte explicitamente
            # antes de inserir. Sem isso, médico sem consultório vinculado
            # (valor None) ou número puro quebra com TclError.
            cons_e.insert(0, str(medico.get("consultorio")) if medico.get("consultorio") is not None else "")
            status_var.set(medico.get("status") or "Ativo")

        erro = ctk.CTkLabel(frame, text="", text_color=get_color("danger"))
        erro.pack(pady=(8, 0))

        def _salvar():
            # Validação dos campos + resolução do id_consultorio a partir
            # da lista já carregada em memória (self.consultorios_disponiveis),
            # buscada uma única vez no início da aba — sem nova chamada de
            # rede aqui, igual à regra original do seu backend.
            try:
                cons = int(cons_e.get())
                nome = nome_e.get().strip(); crm = crm_e.get().strip()
            except Exception:
                erro.configure(text="⚠  Número de consultório inválido.")
                return

            if not nome: erro.configure(text="⚠  Nome é obrigatório."); return
            if not crm:  erro.configure(text="⚠  CRM é obrigatório."); return

            id_consultorio = None
            for consultorio in self.consultorios_disponiveis:
                if consultorio['numero'] == cons:
                    id_consultorio = consultorio['id_consultorio']
                    break
            if id_consultorio is None:
                erro.configure(text="⚠ Consultório não encontrado")
                return

            dados = {
                "nome": nome, "especialidade": esp_var.get(),
                "crm": crm, "id_consultorio": id_consultorio, "status": status_var.get(),
            }
            on_salvar(dados)
            _fechar()

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

        # Overlay de loading desta aba (mesma observação da AbaUsuarios).
        self.loading = LoadingOverlay(self)

        self._render()

    def _render(self):
        for w in self._lista.winfo_children(): w.destroy()

        # ------------------------------------------------------------------
        # ANTES: "self.planos = listar_planos()" rodava direto aqui.
        # AGORA: mesma chamada, em thread separada via run_async.
        # ------------------------------------------------------------------
        def _ao_concluir(planos):
            self.planos = planos

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

        def _ao_erro(erro):
            self._lbl_cont.configure(text="Erro ao carregar planos")
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="⚠️", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(
                f, text=f"Não foi possível carregar os planos.\n{erro}",
                font=ctk.CTkFont(size=13), text_color=get_color("danger"),
            ).pack(pady=(8, 4))

        self.loading.run_async(
            tarefa=listar_planos,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando planos...",
        )

    def _novo(self):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            #self.planos.append(dados)
            # ── BACK ──────────────────────────────────────────────────────
            nome = dados['nome']
            status = dados['status']
            _dados = (nome, status)

            self.loading.run_async(
                tarefa=lambda: salvar_plano(_dados),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao salvar plano:", erro),
                mensagem="Salvando plano...",
            )
        self._abrir_popup(None, salvar)

    def _editar(self, pl: dict):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            #pl.update(dados)
            # ── BACK ──────────────────────────────────────────────────────
            id_plano = pl['id_plano']
            nome = dados['nome']
            status = dados['status']
            _dados = (nome, status)

            self.loading.run_async(
                tarefa=lambda: editar_planos(id_plano, _dados),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao editar plano:", erro),
                mensagem="Salvando plano...",
            )
        self._abrir_popup(pl, salvar)

    def _remover(self, pl: dict):
        def ok():
            #self.planos.remove(pl)
            # ── BACK ──────────────────────────────────────────────────────
            id_plano = pl['id_plano']

            self.loading.run_async(
                tarefa=lambda: remover_plano(id_plano),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao remover plano:", erro),
                mensagem="Removendo plano...",
            )
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
            try:
                nome = str(nome_e.get().strip())
            except Exception:
                erro.configure(text="⚠ Digite o nome do plano corretamente.")
                return
            if not nome: erro.configure(text="⚠  Nome é obrigatório."); return

            # ------------------------------------------------------------
            # ANTES: "planos = listar_planos()" rodava direto aqui para
            # checar duplicidade de nome, travando o popup.
            # AGORA: mesma checagem, só que a chamada de rede vai via
            # run_async; o resto da validação (comparação de nomes)
            # roda dentro do callback, exatamente como antes.
            # ------------------------------------------------------------
            def _ao_concluir(planos):
                for plano_existente in planos:
                    if plano_existente['nome'].lower() == nome.lower():
                        erro.configure(text="⚠ Plano já cadastrado")
                        return
                on_salvar({"nome": nome, "status": status_var.get()})
                _fechar()

            def _ao_erro(e):
                erro.configure(text=f"⚠ Erro ao verificar plano: {e}")

            self.loading.run_async(
                tarefa=listar_planos,
                ao_concluir=_ao_concluir,
                ao_erro=_ao_erro,
                mensagem="Verificando plano...",
            )

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
            linha1, text=f"Consultório n° {c.get('numero', '—')}",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=get_color("text"),
        ).pack(side="left")
        status = c.get("status", "Disponível")
        s_cor = _CORES_STATUS_CONS.get(status, get_color("accent"))
        badge = ctk.CTkFrame(linha1, fg_color=s_cor, corner_radius=10)
        badge.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(badge, text=f"  {status}  ", font=ctk.CTkFont(size=10, weight="bold"), text_color="white").pack()
        ctk.CTkLabel(
            self._info, text=f"📍 {c.get('andar', '—')}° andar",
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

        # Overlay de loading desta aba (mesma observação da AbaUsuarios).
        self.loading = LoadingOverlay(self)

        self._render()

    def _render(self):
        for w in self._lista.winfo_children(): w.destroy()

        # ------------------------------------------------------------------
        # ANTES: "self.consultorios = listar_consultorios()" + print(...)
        # rodava direto aqui, travando a tela.
        # AGORA: mesma chamada, em thread separada. print de debug mantido.
        # ------------------------------------------------------------------
        def _ao_concluir(consultorios):
            self.consultorios = consultorios
            print(self.consultorios)

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

        def _ao_erro(erro):
            self._lbl_cont.configure(text="Erro ao carregar consultórios")
            f = ctk.CTkFrame(self._lista, fg_color="transparent"); f.pack(pady=60)
            ctk.CTkLabel(f, text="⚠️", font=ctk.CTkFont(size=40)).pack()
            ctk.CTkLabel(
                f, text=f"Não foi possível carregar os consultórios.\n{erro}",
                font=ctk.CTkFont(size=13), text_color=get_color("danger"),
            ).pack(pady=(8, 4))

        self.loading.run_async(
            tarefa=listar_consultorios,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando consultórios...",
        )

    def _novo(self):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):

            # ── BACK ──────────────────────────────────────────────────────
            numero = dados['numero']
            andar = dados['andar']
            status = dados['status']
            _dados = (numero, andar, status)
            print(_dados)
            print(dados)

            self.loading.run_async(
                tarefa=lambda: salvar_consultorio(_dados),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao salvar consultório:", erro),
                mensagem="Salvando consultório...",
            )
        self._abrir_popup(None, salvar)

    def _editar(self, c: dict):
        if self._popup_aberto: return
        self._popup_aberto = True
        def salvar(dados):
            #c.update(dados)
            # ── BACK ──────────────────────────────────────────────────────
            numero = dados['numero']
            andar = dados['andar']
            status = dados['status']
            _dados = (numero, andar, status)
            id_consutorio = c['id_consultorio']
            print(dados)
            print(_dados)
            print(id_consutorio)

            self.loading.run_async(
                tarefa=lambda: editar_consutorio(id_consutorio, _dados),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao editar consultório:", erro),
                mensagem="Salvando consultório...",
            )
        self._abrir_popup(c, salvar)

    def _remover(self, c: dict):
        def ok():
           #self.consultorios.remove(c)
            # ── BACK ──────────────────────────────────────────────────────
            id_consultorio = c['id_consultorio']

            self.loading.run_async(
                tarefa=lambda: remover_consultorio(id_consultorio),
                ao_concluir=lambda resultado: self._render(),
                ao_erro=lambda erro: print("Erro ao remover consultório:", erro),
                mensagem="Removendo consultório...",
            )
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
            # "numero" e "andar" vêm como int do banco — mesma correção
            # aplicada na AbaMedicos para o campo "consultorio": converter
            # explicitamente pra string antes de inserir, senão quebra
            # com TclError no CTkEntry.insert.
            num_e.insert(0, str(cons.get("numero")) if cons.get("numero") is not None else "")
            andar_e.insert(0, str(cons.get("andar")) if cons.get("andar") is not None else "")
            status_var.set(cons.get("status") or "Disponível")

        erro = ctk.CTkLabel(frame, text="", text_color=get_color("danger"))
        erro.pack(pady=(8, 0))

        def _salvar():
            try:
                num = int(num_e.get().strip()); andar = int(andar_e.get().strip())
            except Exception:
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