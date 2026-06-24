import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox
import os
from .theme import get_color
from .exportar_atendimento_pdf import exportar_atendimento_pdf

# ─────────────────────────────────────────────────────────────────────────────
# VERSÃO COM DADOS FICTÍCIOS (sem backend, sem loading)
#
# Esta versão usa listas/dicts em memória só pra você visualizar o front
# funcionando de ponta a ponta. Quando o backend estiver pronto, me manda
# o código que você implementou e eu troco os pontos certos por chamadas
# reais + LoadingOverlay — igual fizemos com Agenda, Patients e Configurações.
# ─────────────────────────────────────────────────────────────────────────────


STATUS_COLORS = {
    "Agendado": "#3B82F6",
    "Chegou": "#F59E0B",
    "Atendido": "#22C55E",
}


def _dados_ficticios():
    """Gera consultas fictícias pra hoje e pra alguns outros dias, com
    histórico de atendimentos por paciente. Só pra teste visual."""
    hoje = datetime.now().strftime("%d/%m/%Y")
    ontem = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")

    consultas = [
        {
            "id_consulta": 1, "hora": "08:00", "paciente": "João Silva",
            "cpf": "123.456.789-00", "id_paciente": 101, "data": hoje,
            "status": "Agendado",
            "anexos": [
                {"nome_original": "exame_sangue.pdf", "caminho_storage": "fake/exame_sangue.pdf", "id_documento": 901},
                {"nome_original": "raio_x_torax.pdf", "caminho_storage": "fake/raio_x.pdf", "id_documento": 902},
            ],
        },
        {
            "id_consulta": 2, "hora": "08:30", "paciente": "Maria Souza",
            "cpf": "987.654.321-00", "id_paciente": 102, "data": hoje,
            "status": "Chegou", "anexos": [],
        },
        {
            "id_consulta": 3, "hora": "09:15", "paciente": "Pedro Lima",
            "cpf": "456.789.123-00", "id_paciente": 103, "data": hoje,
            "status": "Atendido", "anexos": [],
        },
        {
            "id_consulta": 4, "hora": "10:00", "paciente": "Ana Costa",
            "cpf": "321.654.987-00", "id_paciente": 104, "data": ontem,
            "status": "Atendido", "anexos": [],
        },
    ]

    # Atendimentos já salvos (simulando o que viria de buscar_atendimento)
    atendimentos = {
        3: {
            "queixa": "Check-up de rotina",
            "observacoes": "Paciente sem queixas relevantes.",
            "diagnostico": "Sem alterações",
            "receita": "",
            "exames": "",
        },
    }

    # Histórico por paciente (simulando listar_historico_paciente)
    historico = {
        101: [
            {
                "id_consulta": 50, "data": "12/05/2026", "medico": "Dr. Carlos",
                "queixa": "Dor lombar ao se levantar, há 1 semana.",
                "observacoes": "Paciente relata melhora ao repouso.",
                "diagnostico": "Lombalgia mecânica leve.",
                "receita": "Ciclobenzaprina 5mg — 1x ao dia por 5 dias.",
                "exames": "",
                "anexos": [
                    {"nome_original": "receita_anterior.pdf", "caminho_storage": "fake/receita_ant.pdf", "id_documento": 800},
                ],
            },
            {
                "id_consulta": 30, "data": "02/03/2026", "medico": "Dr. Carlos",
                "queixa": "Febre e tosse",
                "observacoes": "Sem dificuldade respiratória.",
                "diagnostico": "Gripe comum",
                "receita": "Paracetamol 750mg se febre.",
                "exames": "",
                "anexos": [],
            },
        ],
    }

    return consultas, atendimentos, historico


class DoctorView(ctk.CTkFrame):
    def __init__(self, master, id_medico=1, nome_medico="Dr. Carlos"):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.bg = get_color("bg")
        self.panel = get_color("panel")
        self.card_color = get_color("card")
        self.soft = get_color("surface_dark")
        self.primary = get_color("accent")
        self.accent = get_color("accent")
        self.text_dark = get_color("text")

        self.configure(fg_color=self.bg)

        self.id_medico = id_medico
        self.nome_medico = nome_medico

        self.data_atual = datetime.now()

        # ---- DADOS FICTÍCIOS EM MEMÓRIA (trocar por chamadas reais depois) --
        self.todas_consultas, self.atendimentos_salvos, self.historico_pacientes = _dados_ficticios()

        self._montar_lista()

    # ──────────────────────────────────────────────────────────────────
    # TELA 1: LISTA DE CONSULTAS DO DIA (COM NAVEGAÇÃO DE DATA)
    # ──────────────────────────────────────────────────────────────────
    def _montar_lista(self):
        for w in self.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self, fg_color=self.panel, corner_radius=20)
        header.pack(fill="x", padx=20, pady=(20, 10))

        topo = ctk.CTkFrame(header, fg_color="transparent")
        topo.pack(fill="x", padx=20, pady=(15, 5))

        titulo_frame = ctk.CTkFrame(topo, fg_color="transparent")
        titulo_frame.pack(side="left")

        ctk.CTkLabel(
            titulo_frame,
            text="🩺 Minhas Consultas",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=get_color("text"),
        ).pack(anchor="w")

        self.label_contador = ctk.CTkLabel(
            titulo_frame, text="",
            font=ctk.CTkFont(size=12),
            text_color=get_color("text_secondary"),
        )
        self.label_contador.pack(anchor="w")

        nav = ctk.CTkFrame(header, fg_color="transparent")
        nav.pack(fill="x", padx=20, pady=(5, 5))

        ctk.CTkButton(
            nav, text="◀", width=35, fg_color=self.soft, text_color=self.accent,
            command=self._voltar_dia,
        ).pack(side="left", padx=2)

        self.label_data = ctk.CTkLabel(
            nav, text="", width=120,
            text_color=get_color("text"),
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.label_data.pack(side="left", padx=10)

        ctk.CTkButton(
            nav, text="▶", width=35, fg_color=self.soft, text_color=self.accent,
            command=self._avancar_dia,
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            nav, text="Hoje", width=60, fg_color=self.primary,
            hover_color=get_color("accent_hover"),
            command=self._ir_hoje,
        ).pack(side="left", padx=5)

        jump = ctk.CTkFrame(header, fg_color="transparent")
        jump.pack(fill="x", padx=20, pady=(0, 15))

        self.input_data = ctk.CTkEntry(jump, placeholder_text="dd/mm/aaaa", width=140)
        self.input_data.pack(side="left", padx=(0, 8))
        self.input_data.bind("<Return>", lambda e: self._ir_data())

        ctk.CTkButton(
            jump, text="Ir", width=50, fg_color=self.soft, text_color=self.accent,
            border_width=1, border_color=self.accent,
            command=self._ir_data,
        ).pack(side="left")

        self.lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.lista.pack(fill="both", expand=True, padx=20, pady=10)

        self._atualizar_label_data()
        self._renderizar_consultas()

    def _atualizar_label_data(self):
        self.label_data.configure(text=self.data_atual.strftime("%d/%m/%Y"))

    def _voltar_dia(self):
        self.data_atual -= timedelta(days=1)
        self._atualizar_label_data()
        self._renderizar_consultas()

    def _avancar_dia(self):
        self.data_atual += timedelta(days=1)
        self._atualizar_label_data()
        self._renderizar_consultas()

    def _ir_hoje(self):
        self.data_atual = datetime.now()
        self._atualizar_label_data()
        self._renderizar_consultas()

    def _ir_data(self):
        texto = self.input_data.get().strip()
        try:
            nova_data = datetime.strptime(texto, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Data inválida", "Digite a data no formato dd/mm/aaaa.")
            self.input_data.focus_set()
            return
        self.data_atual = nova_data
        self._atualizar_label_data()
        self._renderizar_consultas()

    def _renderizar_consultas(self):
        for w in self.lista.winfo_children():
            w.destroy()

        data_str = self.data_atual.strftime("%d/%m/%Y")

        # FICTÍCIO: filtra a lista em memória pela data.
        # BACKEND (depois): listar_consultas_por_data(id_medico, data_str)
        consultas_do_dia = [c for c in self.todas_consultas if c["data"] == data_str]

        total = len(consultas_do_dia)
        if total == 0:
            self.label_contador.configure(text="Nenhuma consulta")
        elif total == 1:
            self.label_contador.configure(text="1 consulta")
        else:
            self.label_contador.configure(text=f"{total} consultas")

        if not consultas_do_dia:
            ctk.CTkLabel(
                self.lista, text="📭 Nenhuma consulta neste dia",
                text_color=self.text_dark, font=ctk.CTkFont(size=14),
            ).pack(pady=50)
            return

        consultas_ordenadas = sorted(consultas_do_dia, key=lambda c: c.get("hora", ""))
        for c in consultas_ordenadas:
            self._card_consulta(c)

    def _card_consulta(self, c):
        card = ctk.CTkFrame(self.lista, fg_color=self.card_color, corner_radius=16)
        card.pack(fill="x", pady=6)

        cor_status = STATUS_COLORS.get(c.get("status", "Agendado"), self.primary)
        bar = ctk.CTkFrame(card, width=6, fg_color=cor_status, corner_radius=10)
        bar.pack(side="left", fill="y")

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", expand=True, padx=15, pady=15)

        ctk.CTkLabel(
            container, text=c["hora"], width=70, height=32,
            fg_color=self.soft, text_color=self.accent, corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=(0, 15))

        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(
            info, text=c["paciente"], font=ctk.CTkFont(size=15, weight="bold"),
            text_color=get_color("text"), anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info, text=f"CPF: {self._ocultar_cpf(c['cpf'])}",
            text_color=get_color("text_secondary"), font=ctk.CTkFont(size=12), anchor="w",
        ).pack(anchor="w")

        if c.get("anexos"):
            ctk.CTkLabel(
                info, text=f"📎 {len(c['anexos'])} anexo(s)",
                text_color=get_color("text_secondary"), font=ctk.CTkFont(size=11), anchor="w",
            ).pack(anchor="w", pady=(2, 0))

        status_atual = c.get("status", "Agendado")
        ctk.CTkLabel(
            container, text=f"  {status_atual}  ", fg_color=cor_status,
            text_color="#FFFFFF", corner_radius=10,
            font=ctk.CTkFont(size=11, weight="bold"), height=26,
        ).pack(side="right", padx=(0, 10))

        texto_botao = "Ver atendimento" if status_atual == "Atendido" else "Iniciar consulta"
        ctk.CTkButton(
            container, text=texto_botao, width=130, height=32, corner_radius=14,
            fg_color=self.primary, hover_color=get_color("accent_hover"),
            command=lambda c=c: self._abrir_atendimento(c),
        ).pack(side="right")

    def _ocultar_cpf(self, cpf):
        nums = "".join(filter(str.isdigit, cpf))
        if len(nums) < 11:
            return cpf
        return f"{nums[:3]}.***.***-{nums[-2:]}"

    # ──────────────────────────────────────────────────────────────────
    # TELA 2: ATENDIMENTO (anexos + campos estruturados)
    # ──────────────────────────────────────────────────────────────────
    def _abrir_atendimento(self, consulta):
        for w in self.winfo_children():
            w.destroy()

        self.anexos_atendimento = [dict(a) for a in consulta.get("anexos", [])]

        # Atendimentos já concluídos ficam bloqueados: campos só-leitura,
        # sem botão de salvar, sem poder anexar/excluir anexo. Evita que
        # o médico sobrescreva um registro médico já finalizado sem
        # querer, só por ter clicado em "Ver atendimento" de novo.
        #
        # BACKEND: esta trava aqui é só de UI. Quando salvar_atendimento
        # for implementado, vale repetir essa checagem no servidor também
        # (ex: recusar UPDATE se a consulta já estiver com status
        # "Atendido"), pra não depender só do front impedir o reenvio.
        somente_leitura = consulta.get("status") == "Atendido"

        container = ctk.CTkFrame(self, fg_color=self.bg)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkButton(
            header, text="← Voltar", width=110, fg_color=self.soft,
            text_color=self.accent,
            command=self._montar_lista,
        ).pack(side="left")

        info_paciente = ctk.CTkFrame(header, fg_color="transparent")
        info_paciente.pack(side="left", padx=15)

        ctk.CTkLabel(
            info_paciente, text=consulta["paciente"],
            font=ctk.CTkFont(size=18, weight="bold"), text_color=get_color("text"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_paciente, text=self._ocultar_cpf(consulta["cpf"]),
            font=ctk.CTkFont(size=12), text_color=get_color("text_secondary"),
        ).pack(anchor="w")

        if somente_leitura:
            ctk.CTkLabel(
                header, text="🔒 Atendimento concluído — somente leitura",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=get_color("success"),
            ).pack(side="right", padx=10)

        form_frame = ctk.CTkFrame(
            container, fg_color=self.card_color, corner_radius=20,
            border_width=1, border_color=get_color("border"),
        )
        form_frame.pack(fill="both", expand=True, pady=15)

        scroll = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            scroll, text="📎 Anexos desta consulta",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=self.accent,
        ).pack(anchor="w", pady=(0, 8))

        self.anexos_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        self.anexos_frame.pack(fill="x", pady=(0, 5))
        self._redesenhar_anexos_atendimento(consulta, somente_leitura)

        if not somente_leitura:
            ctk.CTkButton(
                scroll, text="+ Anexar PDF", height=32,
                command=lambda: self._adicionar_anexo_atendimento(consulta),
            ).pack(fill="x", pady=(0, 18))
        else:
            ctk.CTkFrame(scroll, fg_color="transparent", height=10).pack()

        ctk.CTkLabel(
            scroll, text="📝 Atendimento",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=self.accent,
        ).pack(anchor="w", pady=(0, 8))

        campo_queixa = self._campo(scroll, "Queixa")
        campo_observacoes = self._campo(scroll, "Observações")
        campo_diagnostico = self._campo(scroll, "Diagnóstico")
        campo_receita = self._campo(scroll, "Receita")
        campo_exames = self._campo(scroll, "Exames solicitados")

        # FICTÍCIO: busca no dict em memória pelo id_consulta.
        # BACKEND (depois): buscar_atendimento(id_consulta) -> dict | None
        atendimento_existente = self.atendimentos_salvos.get(consulta["id_consulta"])
        if atendimento_existente:
            campo_queixa.insert("1.0", atendimento_existente.get("queixa", ""))
            campo_observacoes.insert("1.0", atendimento_existente.get("observacoes", ""))
            campo_diagnostico.insert("1.0", atendimento_existente.get("diagnostico", ""))
            campo_receita.insert("1.0", atendimento_existente.get("receita", ""))
            campo_exames.insert("1.0", atendimento_existente.get("exames", ""))

        if somente_leitura:
            for campo in (campo_queixa, campo_observacoes, campo_diagnostico, campo_receita, campo_exames):
                campo.configure(state="disabled")

        ctk.CTkButton(
            scroll, text="📜 Ver histórico deste paciente",
            fg_color="transparent", border_width=1, border_color=self.accent,
            text_color=self.accent, height=36,
            command=lambda: self._abrir_historico(consulta),
        ).pack(fill="x", pady=(18, 0))

        if somente_leitura:
            # Nenhum botão de salvar é criado — o atendimento já foi
            # concluído e não pode ser sobrescrito por esta tela.
            return

        def salvar():
            dados = {
                "queixa": campo_queixa.get("1.0", "end").strip(),
                "observacoes": campo_observacoes.get("1.0", "end").strip(),
                "diagnostico": campo_diagnostico.get("1.0", "end").strip(),
                "receita": campo_receita.get("1.0", "end").strip(),
                "exames": campo_exames.get("1.0", "end").strip(),
            }

            # FICTÍCIO: salva no dict em memória e marca status como Atendido.
            # BACKEND (depois): salvar_atendimento(id_consulta, dados)
            self.atendimentos_salvos[consulta["id_consulta"]] = dados
            consulta["status"] = "Atendido"

            messagebox.showinfo("Sucesso", "Atendimento salvo com sucesso.")
            self._montar_lista()

        ctk.CTkButton(
            container, text="✓ Salvar Atendimento", height=45, corner_radius=12,
            fg_color=get_color("success"), hover_color=get_color("success_hover"),
            command=salvar,
        ).pack(pady=(5, 0))

    def _campo(self, parent, titulo):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.pack(fill="x", pady=8)

        ctk.CTkLabel(
            box, text=titulo, font=ctk.CTkFont(size=13, weight="bold"),
            text_color=get_color("text"),
        ).pack(anchor="w", pady=(0, 5))

        entry = ctk.CTkTextbox(
            box, height=80, corner_radius=12,
            border_width=1, border_color=get_color("border"),
        )
        entry.pack(fill="x")
        return entry

    def _redesenhar_anexos_atendimento(self, consulta, somente_leitura=None):
        # Guarda a flag como atributo de instância na primeira chamada
        # (vinda de _abrir_atendimento) para que adicionar_anexo/excluir_anexo
        # — que chamam este método de novo depois — continuem respeitando
        # o mesmo modo sem precisar repassar o parâmetro toda vez.
        if somente_leitura is not None:
            self._anexos_somente_leitura = somente_leitura
        somente_leitura = getattr(self, "_anexos_somente_leitura", False)

        for w in self.anexos_frame.winfo_children():
            w.destroy()

        if not self.anexos_atendimento:
            ctk.CTkLabel(
                self.anexos_frame, text="Nenhum anexo nesta consulta.",
                text_color=get_color("text_secondary"), font=ctk.CTkFont(size=12),
            ).pack(anchor="w", pady=4)
            return

        for anexo in self.anexos_atendimento:
            self._mini_card_anexo(
                self.anexos_frame, anexo,
                on_abrir=lambda a=anexo: self._abrir_anexo(a),
                on_excluir=None if somente_leitura else (
                    lambda a=anexo: self._excluir_anexo_atendimento(a, consulta)
                ),
            )

    def _mini_card_anexo(self, parent, anexo, on_abrir, on_excluir=None):
        card = ctk.CTkFrame(
            parent, fg_color=self.soft, corner_radius=12,
            border_width=1, border_color=get_color("border"),
        )
        card.pack(fill="x", pady=4)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(
            inner, text="📄", width=34, height=34, fg_color=get_color("surface"),
            corner_radius=9, font=ctk.CTkFont(size=16),
        ).pack(side="left", padx=(0, 10))

        meta = ctk.CTkFrame(inner, fg_color="transparent")
        meta.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(
            meta, text=anexo.get("nome_original", "arquivo.pdf"),
            font=ctk.CTkFont(size=12, weight="bold"), text_color=get_color("text"),
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            meta, text="PDF", font=ctk.CTkFont(size=10),
            text_color=get_color("text_secondary"), anchor="w",
        ).pack(anchor="w")

        ctk.CTkButton(
            inner, text="📂", width=30, height=30, corner_radius=8,
            fg_color=self.accent, hover_color=get_color("accent_hover"),
            command=on_abrir,
        ).pack(side="right", padx=(4, 0))

        if on_excluir:
            ctk.CTkButton(
                inner, text="🗑", width=30, height=30, corner_radius=8,
                fg_color="#7C2D2D", hover_color="#9B3A3A",
                command=on_excluir,
            ).pack(side="right", padx=(4, 0))

    def _abrir_anexo(self, anexo):
        # FICTÍCIO: como os anexos de teste não existem em disco de
        # verdade, só avisa qual seria aberto, em vez de tentar abrir.
        # BACKEND (depois): se vier de storage, baixar_anexo(caminho_storage)
        # roda via run_async; se já tiver caminho local, abre direto com
        # self._abrir_arquivo(caminho).
        if anexo.get("caminho") and os.path.exists(anexo["caminho"]):
            try:
                self._abrir_arquivo(anexo["caminho"])
            except Exception as e:
                messagebox.showerror("ERRO", str(e))
        else:
            messagebox.showinfo(
                "Simulação",
                f"(Fictício) Aqui abriria: {anexo.get('nome_original', '')}",
            )

    def _excluir_anexo_atendimento(self, anexo, consulta):
        confirmar = messagebox.askyesno(
            "Excluir anexo",
            f"Remover o arquivo \"{anexo.get('nome_original', '')}\" desta consulta?",
        )
        if not confirmar:
            return

        # FICTÍCIO: remove só da lista em memória.
        # BACKEND (depois): excluir_anexo(id_documento) antes de remover
        # da lista local, se o anexo já tiver id_documento (já persistido).
        self.anexos_atendimento.remove(anexo)
        self._redesenhar_anexos_atendimento(consulta)

    def _adicionar_anexo_atendimento(self, consulta):
        arq = filedialog.askopenfilename(title="Selecionar PDF", filetypes=[("Arquivos PDF", "*.pdf")])
        if not arq:
            return

        nome_arquivo = os.path.basename(arq)
        ja_existe = any(
            a.get("nome_original", "").lower() == nome_arquivo.lower()
            for a in self.anexos_atendimento
        )
        if ja_existe:
            messagebox.showwarning(
                "Arquivo já anexado",
                f"O arquivo \"{nome_arquivo}\" já está anexado a esta consulta.",
            )
            return

        self.anexos_atendimento.append({
            "nome_original": nome_arquivo,
            "caminho": arq,
            "caminho_storage": None,
            "id_documento": None,
        })
        self._redesenhar_anexos_atendimento(consulta)

    def _abrir_arquivo(self, caminho):
        if not os.path.exists(caminho):
            messagebox.showerror("Arquivo não encontrado", f"O arquivo não existe mais:\n{caminho}")
            return
        try:
            os.startfile(caminho)
        except AttributeError:
            messagebox.showerror("Não suportado", "Abrir arquivos automaticamente só funciona no Windows por enquanto.")
        except OSError as e:
            messagebox.showerror("Erro ao abrir arquivo", str(e))

    # ──────────────────────────────────────────────────────────────────
    # TELA 3: HISTÓRICO DO PACIENTE
    # ──────────────────────────────────────────────────────────────────
    def _abrir_historico(self, consulta):
        for w in self.winfo_children():
            w.destroy()

        container = ctk.CTkFrame(self, fg_color=self.bg)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkButton(
            header, text="← Voltar", width=110, fg_color=self.soft,
            text_color=self.accent,
            command=lambda: self._abrir_atendimento(consulta),
        ).pack(side="left")

        info = ctk.CTkFrame(header, fg_color="transparent")
        info.pack(side="left", padx=15)

        ctk.CTkLabel(
            info, text=f"Histórico — {consulta['paciente']}",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=get_color("text"),
        ).pack(anchor="w")

        # FICTÍCIO: busca no dict em memória pelo id_paciente.
        # BACKEND (depois): listar_historico_paciente(id_paciente) -> list[dict]
        historicos = self.historico_pacientes.get(consulta["id_paciente"], [])

        total = len(historicos)
        ctk.CTkLabel(
            info, text=f"{total} atendimento{'s' if total != 1 else ''} registrado{'s' if total != 1 else ''}",
            font=ctk.CTkFont(size=12), text_color=get_color("text_secondary"),
        ).pack(anchor="w")

        lista_hist = ctk.CTkScrollableFrame(container, fg_color="transparent")
        lista_hist.pack(fill="both", expand=True, pady=15)

        if not historicos:
            ctk.CTkLabel(
                lista_hist, text="Sem histórico ainda",
                text_color=get_color("text_secondary"),
            ).pack(anchor="w", pady=20)
            return

        for h in historicos:
            self._card_historico(lista_hist, h, consulta)

    def _card_historico(self, parent, h, consulta_atual):
        card = ctk.CTkFrame(
            parent, fg_color=self.card_color, corner_radius=14,
            border_width=1, border_color=get_color("border"),
        )
        card.pack(fill="x", pady=6)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=14, pady=10)

        topo = ctk.CTkFrame(inner, fg_color="transparent")
        topo.pack(fill="x")

        ctk.CTkLabel(
            topo, text=f"📅 {h['data']}", font=ctk.CTkFont(weight="bold"),
            text_color=self.accent,
        ).pack(side="left")

        ctk.CTkButton(
            topo, text="Ver completo", width=110, fg_color=self.soft,
            text_color=get_color("text"),
            command=lambda h=h: self._ver_historico_completo(h, consulta_atual),
        ).pack(side="right")

        ctk.CTkLabel(
            inner, text=f"Queixa: {h.get('queixa') or '—'}",
            text_color=get_color("text"), font=ctk.CTkFont(size=12),
        ).pack(anchor="w", pady=(6, 0))
        ctk.CTkLabel(
            inner, text=f"Diagnóstico: {h.get('diagnostico') or '—'}",
            text_color=get_color("text_secondary"), font=ctk.CTkFont(size=12),
        ).pack(anchor="w")

    # ──────────────────────────────────────────────────────────────────
    # TELA 4: VER COMPLETO (anexo visível, exportar PDF sem anexo)
    # ──────────────────────────────────────────────────────────────────
    def _ver_historico_completo(self, h, consulta_atual):
        popup = ctk.CTkToplevel(self)
        popup.title(f"Atendimento — {h['data']}")
        popup.geometry("520x600")
        popup.grab_set()
        popup.configure(fg_color=self.card_color)

        frame = ctk.CTkScrollableFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame, text=f"📅 {h['data']}",
            font=ctk.CTkFont(size=16, weight="bold"), text_color=get_color("text"),
        ).pack(anchor="w", pady=(0, 12))

        anexos_h = h.get("anexos", [])
        if anexos_h:
            ctk.CTkLabel(
                frame, text="📎 Anexo desta consulta",
                font=ctk.CTkFont(size=13, weight="bold"), text_color=self.accent,
            ).pack(anchor="w", pady=(0, 6))

            anexos_frame_hist = ctk.CTkFrame(frame, fg_color="transparent")
            anexos_frame_hist.pack(fill="x", pady=(0, 4))

            for anexo in anexos_h:
                self._mini_card_anexo(
                    anexos_frame_hist, anexo,
                    on_abrir=lambda a=anexo: self._abrir_anexo(a),
                    on_excluir=None,
                )

            ctk.CTkLabel(
                frame,
                text="* O anexo pode ser aberto aqui, mas não entra no PDF exportado abaixo.",
                font=ctk.CTkFont(size=10, slant="italic"),
                text_color=get_color("text_secondary"),
            ).pack(anchor="w", pady=(0, 12))

        campos = [
            ("Queixa", h.get("queixa", "")),
            ("Observações", h.get("observacoes", "")),
            ("Diagnóstico", h.get("diagnostico", "")),
            ("Receita", h.get("receita", "")),
            ("Exames", h.get("exames", "")),
        ]

        for titulo, valor in campos:
            ctk.CTkLabel(
                frame, text=titulo, font=ctk.CTkFont(weight="bold"),
                text_color=get_color("text"),
            ).pack(anchor="w", pady=(10, 0))
            ctk.CTkLabel(
                frame, text=valor or "—", wraplength=460, justify="left",
                text_color=get_color("text_secondary"),
            ).pack(anchor="w")

        def exportar():
            destino = filedialog.asksaveasfilename(
                title="Salvar atendimento como PDF",
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf")],
                initialfile=f"atendimento_{h['data'].replace('/', '-')}.pdf",
            )
            if not destino:
                return

            paciente_info = {
                "nome": consulta_atual.get("paciente", ""),
                "cpf": consulta_atual.get("cpf", ""),
            }
            try:
                exportar_atendimento_pdf(h, paciente_info, destino)
                messagebox.showinfo("Exportado", "PDF gerado com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro ao exportar", str(e))

        botoes = ctk.CTkFrame(frame, fg_color="transparent")
        botoes.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(
            botoes, text="Fechar", fg_color=self.soft, text_color=self.accent,
            command=popup.destroy,
        ).pack(side="left", expand=True, padx=(0, 5))

        ctk.CTkButton(
            botoes, text="📄 Exportar PDF", fg_color=self.primary,
            hover_color=get_color("accent_hover"),
            command=exportar,
        ).pack(side="left", expand=True, padx=(5, 0))