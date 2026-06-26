import customtkinter as ctk
from controllers.relatorios_controller import RelatorioContrroler
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox, TclError
import matplotlib
matplotlib.use("TkAgg")  # backend consistente com FigureCanvasTkAgg abaixo.
                          # Usar "Agg" (não-interativo, sem suporte a
                          # eventos/foco) junto com FigureCanvasTkAgg é uma
                          # combinação inconsistente — o Agg não tem a
                          # infraestrutura de eventos que o canvas Tkinter
                          # espera, o que gera callbacks malformados
                          # apontando pra widgets já destruídos.
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .theme import get_color
from .exportar_relatorio_pdf import exportar_relatorio_pdf

# ─────────────────────────────────────────────────────────────────────────────
# BACKEND PLUGADO: RelatorioContrroler().listar_relatorio() já traz todas
# as consultas (medico, tipo, plano, data), filtradas por status =
# 'Atendido' no SQL. O filtro de período e todo o agrupamento (por
# médico, por plano, por dia) continua sendo feito aqui em Python, sobre
# essa lista completa.
#
# IMPORTANTE — formato do campo "tipo":
# O banco guarda o valor BRUTO da coluna tipo_atendimento como
# "plano" ou "particular" (minúsculo). Todas as COMPARAÇÕES internas
# (contagem, filtros) usam esses valores brutos. O texto "Convênio" só
# aparece na CAMADA DE EXIBIÇÃO (labels de cards, gráficos, PDF) — nunca
# em comparações com c["tipo"].
# ─────────────────────────────────────────────────────────────────────────────

# Valores brutos exatamente como vêm da coluna tipo_atendimento no banco.
TIPO_PLANO_BANCO = "plano"
TIPO_PARTICULAR_BANCO = "particular"

# Rótulos exibidos para o usuário (camada de exibição apenas).
LABEL_CONVENIO = "Convênio"
LABEL_PARTICULAR = "Particular"


FILTROS_PERIODO = ["Hoje", "Última semana", "Último mês", "Personalizado"]


class ReportsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=get_color("bg"))

        self.relatorio_controller = RelatorioContrroler()
        self.todas_consultas = self.relatorio_controller.listar_relatorio()

        self.filtro_atual = "Último mês"
        self.data_inicio_personalizada = None
        self.data_fim_personalizada = None

        # Mantém referência às figuras matplotlib abertas, para fechar
        # explicitamente antes de redesenhar — encerrar a figura antiga
        # evita acumular memória cada vez que o relatório é atualizado
        # (troca de filtro, troca de tema, etc).
        self._figuras_abertas = []

        # Mantém referência aos FigureCanvasTkAgg (não só às Figures),
        # para poder desconectá-los do widget Tkinter de forma limpa
        # antes da destruição — ver _fechar_figuras_abertas() para o
        # porquê disso ser necessário.
        self._canvases_abertos = []

        # Preenchidos por _popular_relatorio() a cada render(); usados
        # pelo botão "Exportar PDF" para montar o documento com os
        # mesmos números e gráficos que estão na tela no momento do clique.
        self._dados_relatorio_atual = None
        self._fig_pizza = None
        self._fig_barras = None
        self._fig_linha = None

        self._instalar_filtro_erro_matplotlib()

        self.render()

    def _instalar_filtro_erro_matplotlib(self):
        """O matplotlib agenda internamente, via after()/after_idle() do
        Tkinter, callbacks de foco/redraw ligados ao FigureCanvasTkAgg.
        Esses callbacks rodam no loop principal do Tkinter, fora do nosso
        controle direto — se a tela for recriada (troca de tema, troca de
        filtro) entre o agendamento e a execução, o callback dispara
        contra um widget já destruído, gerando TclError "invalid command
        name" que por padrão derruba a aplicação.

        Isso é um problema conhecido da combinação matplotlib+Tkinter,
        não um bug da nossa lógica de destruição (já cuidamos da ordem
        certa em _fechar_figuras_abertas). A forma correta de neutralizar
        é interceptar esse erro específico no tratador de exceções de
        callback do Tkinter, deixando qualquer OUTRO erro real continuar
        sendo reportado normalmente.
        """
        janela_raiz = self.winfo_toplevel()
        tratador_original = janela_raiz.report_callback_exception

        def _tratador_filtrado(exc_type, exc_value, exc_traceback):
            if exc_type is TclError and "invalid command name" in str(exc_value):
                # Callback fantasma do matplotlib contra widget já
                # destruído — ignora silenciosamente, não é um erro real
                # do nosso código.
                return
            tratador_original(exc_type, exc_value, exc_traceback)

        janela_raiz.report_callback_exception = _tratador_filtrado

    def destroy(self):
        # Fecha qualquer figura matplotlib pendente quando a tela for
        # destruída (troca de aba no menu), evitando acúmulo de memória
        # entre uma visita e outra à tela de Relatórios.
        self._fechar_figuras_abertas()
        super().destroy()

    def _fechar_figuras_abertas(self):
        # Desconecta cada FigureCanvasTkAgg do Tkinter ANTES de fechar a
        # Figure correspondente. Sem isso, o matplotlib pode deixar
        # callbacks internos (foco, hover) agendados apontando para um
        # widget que está sendo destruído "por fora" (ex: quando o
        # render() chama winfo_children().destroy() no início de cada
        # nova renderização) — o que gera "invalid command name" mais
        # tarde, quando esse callback fantasma tenta rodar.
        for canvas in self._canvases_abertos:
            try:
                canvas.get_tk_widget().destroy()
            except Exception:
                pass  # widget já pode ter sido destruído pelo Tkinter
        self._canvases_abertos = []

        for fig in self._figuras_abertas:
            plt.close(fig)
        self._figuras_abertas = []

    # ──────────────────────────────────────────────────────────────────
    # FILTRO DE PERÍODO
    # ──────────────────────────────────────────────────────────────────
    def _consultas_do_periodo(self):
        """Filtra self.todas_consultas de acordo com self.filtro_atual,
        comparando contra a data de cada consulta (string dd/mm/aaaa)."""
        hoje = datetime.now()

        if self.filtro_atual == "Hoje":
            inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
            fim = hoje
        elif self.filtro_atual == "Última semana":
            inicio = hoje - timedelta(days=7)
            fim = hoje
        elif self.filtro_atual == "Último mês":
            inicio = hoje - timedelta(days=30)
            fim = hoje
        else:  # Personalizado
            if not self.data_inicio_personalizada or not self.data_fim_personalizada:
                return []
            inicio = self.data_inicio_personalizada
            fim = self.data_fim_personalizada

        resultado = []
        for c in self.todas_consultas:
            data_c = datetime.strptime(c["data"], "%d/%m/%Y")
            if inicio.date() <= data_c.date() <= fim.date():
                resultado.append(c)
        return resultado

    def _selecionar_filtro(self, nome_filtro):
        self.filtro_atual = nome_filtro
        self.render()

    def _aplicar_filtro_personalizado(self):
        texto_inicio = self.input_data_inicio.get().strip()
        texto_fim = self.input_data_fim.get().strip()
        try:
            self.data_inicio_personalizada = datetime.strptime(texto_inicio, "%d/%m/%Y")
            self.data_fim_personalizada = datetime.strptime(texto_fim, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Data inválida",
                "Digite as duas datas no formato dd/mm/aaaa.",
            )
            return
        self.filtro_atual = "Personalizado"
        self.render()

    # ──────────────────────────────────────────────────────────────────
    # RENDER PRINCIPAL
    # ──────────────────────────────────────────────────────────────────
    def render(self):
        self._fechar_figuras_abertas()
        for w in self.winfo_children():
            w.destroy()

        titulo = ctk.CTkLabel(
            self,
            text="📊 Relatórios",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=get_color("text"),
        )
        titulo.pack(anchor="w", padx=30, pady=(20, 10))

        self._montar_filtro_periodo()

        self.area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.area.pack(fill="both", expand=True, padx=20, pady=10)

        self._popular_relatorio()

    def _montar_filtro_periodo(self):
        linha = ctk.CTkFrame(self, fg_color="transparent")
        linha.pack(fill="x", padx=30, pady=(0, 10))

        for nome in FILTROS_PERIODO:
            ativo = nome == self.filtro_atual
            ctk.CTkButton(
                linha, text=nome, height=34, corner_radius=10,
                fg_color=get_color("accent") if ativo else get_color("surface_alt"),
                hover_color=get_color("accent_hover"),
                text_color="#FFFFFF" if ativo else get_color("text_secondary"),
                font=ctk.CTkFont(size=13, weight="bold" if ativo else "normal"),
                command=lambda n=nome: self._selecionar_filtro(n),
            ).pack(side="left", padx=(0, 8))

        if self.filtro_atual == "Personalizado":
            self.input_data_inicio = ctk.CTkEntry(linha, placeholder_text="dd/mm/aaaa", width=110)
            self.input_data_inicio.pack(side="left", padx=(8, 4))
            if self.data_inicio_personalizada:
                self.input_data_inicio.insert(0, self.data_inicio_personalizada.strftime("%d/%m/%Y"))

            ctk.CTkLabel(linha, text="até", text_color=get_color("text_secondary")).pack(side="left", padx=4)

            self.input_data_fim = ctk.CTkEntry(linha, placeholder_text="dd/mm/aaaa", width=110)
            self.input_data_fim.pack(side="left", padx=4)
            if self.data_fim_personalizada:
                self.input_data_fim.insert(0, self.data_fim_personalizada.strftime("%d/%m/%Y"))

            ctk.CTkButton(
                linha, text="Aplicar", height=34, width=70, corner_radius=10,
                fg_color=get_color("surface_alt"), text_color=get_color("accent"),
                border_width=1, border_color=get_color("accent"),
                command=self._aplicar_filtro_personalizado,
            ).pack(side="left", padx=(8, 0))

        ctk.CTkButton(
            linha, text="📄 Exportar PDF", height=34, corner_radius=10,
            fg_color=get_color("accent"), hover_color=get_color("accent_hover"),
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._exportar_pdf,
        ).pack(side="right")

    # ──────────────────────────────────────────────────────────────────
    # PROCESSAMENTO DOS DADOS (tudo em memória, sobre a lista filtrada)
    # ──────────────────────────────────────────────────────────────────
    def _popular_relatorio(self):
        dados = self._consultas_do_periodo()

        # Limpa estado anterior — se o período não tiver dados, não deve
        # sobrar referência de relatório antigo disponível pra exportar.
        self._dados_relatorio_atual = None
        self._fig_pizza = None
        self._fig_barras = None
        self._fig_linha = None

        if not dados:
            ctk.CTkLabel(
                self.area, text="📭 Nenhuma consulta no período selecionado",
                text_color=get_color("text_secondary"), font=ctk.CTkFont(size=14),
            ).pack(pady=60)
            return

        total = len(dados)
        # Comparações usam o valor BRUTO do banco ("plano"/"particular"),
        # não os rótulos de exibição ("Convênio"/"Particular").
        convenio = len([c for c in dados if c["tipo"] == TIPO_PLANO_BANCO])
        particular = len([c for c in dados if c["tipo"] == TIPO_PARTICULAR_BANCO])

        medicos = {}
        planos = {}
        por_dia = {}

        for c in dados:
            # c["plano"] já vem com o NOME do plano (ex: "Unimed"),
            # vindo do LEFT JOIN com a tabela Plano — None quando a
            # consulta é particular (paciente sem plano cadastrado).
            # Para exibição, agrupamos esses casos sob o rótulo "Particular".
            plano = c["plano"] if c["plano"] else LABEL_PARTICULAR
            medico = c["medico"]

            planos[plano] = planos.get(plano, 0) + 1

            if medico not in medicos:
                medicos[medico] = {}
            medicos[medico][plano] = medicos[medico].get(plano, 0) + 1

            por_dia[c["data"]] = por_dia.get(c["data"], 0) + 1

        # Guarda os números já processados para o botão "Exportar PDF"
        # usar depois, sem precisar reprocessar nada.
        self._dados_relatorio_atual = {
            "total": total, "convenio": convenio, "particular": particular,
            "medicos": medicos,
        }

        # ---- Cards -----------------------------------------------------------
        cards = ctk.CTkFrame(self.area, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 15))
        self._card(cards, "📋", "Total de consultas", total, get_color("accent"))
        self._card(cards, "🏥", LABEL_CONVENIO, convenio, get_color("success"))
        self._card(cards, "💳", LABEL_PARTICULAR, particular, get_color("warning"))

        # ---- Gráficos lado a lado: pizza + barras -----------------------------
        linha_graficos = ctk.CTkFrame(self.area, fg_color="transparent")
        linha_graficos.pack(fill="x", pady=(0, 15))

        self._grafico_pizza(linha_graficos, convenio, particular)
        self._grafico_barras_medico(linha_graficos, medicos)

        # ---- Gráfico de linha: consultas por dia ------------------------------
        self._grafico_linha_por_dia(self.area, por_dia)

        # ---- Detalhamento por médico --------------------------------------------
        self._lista_medicos(self.area, medicos)

    def _card(self, parent, icone, titulo, valor, cor_destaque):
        card = ctk.CTkFrame(
            parent, fg_color=get_color("surface"), corner_radius=14,
            border_width=1, border_color=get_color("border"),
        )
        card.pack(side="left", expand=True, fill="x", padx=5)

        # Barra de destaque lateral (esquerda) — substitui o card neutro
        # original por um indicador de cor por categoria.
        barra = ctk.CTkFrame(card, width=4, fg_color=cor_destaque, corner_radius=0)
        barra.pack(side="left", fill="y")

        conteudo = ctk.CTkFrame(card, fg_color="transparent")
        conteudo.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        ctk.CTkLabel(
            conteudo, text=icone, font=ctk.CTkFont(size=18),
        ).pack(anchor="w")

        ctk.CTkLabel(
            conteudo, text=titulo, text_color=get_color("text_secondary"),
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkLabel(
            conteudo, text=str(valor), font=ctk.CTkFont(size=26, weight="bold"),
            text_color=get_color("text"),
        ).pack(anchor="w")

    # ──────────────────────────────────────────────────────────────────
    # GRÁFICOS (matplotlib embutido, cores vindas do tema)
    # ──────────────────────────────────────────────────────────────────
    def _criar_figura(self, figsize):
        """Cria uma figura matplotlib já com as cores de fundo do tema
        atual aplicadas, e a guarda em self._figuras_abertas para fechar
        depois (evita acúmulo de memória entre re-renderizações)."""
        cor_fundo = get_color("surface")
        fig, ax = plt.subplots(figsize=figsize, dpi=100)
        fig.patch.set_facecolor(cor_fundo)
        ax.set_facecolor(cor_fundo)
        self._figuras_abertas.append(fig)
        return fig, ax

    def _embutir_figura(self, parent, fig):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        self._canvases_abertos.append(canvas)
        widget = canvas.get_tk_widget()
        widget.configure(bg=get_color("surface"), highlightthickness=0)
        return widget

    def _grafico_pizza(self, parent, convenio, particular):
        box = ctk.CTkFrame(
            parent, fg_color=get_color("surface"), corner_radius=14,
            border_width=1, border_color=get_color("border"),
        )
        box.pack(side="left", fill="both", expand=True, padx=(0, 8))

        ctk.CTkLabel(
            box, text=f"{LABEL_CONVENIO} vs {LABEL_PARTICULAR}", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color("accent"),
        ).pack(anchor="w", padx=14, pady=(12, 4))

        cor_texto = get_color("text")
        fig, ax = self._criar_figura(figsize=(3.4, 2.8))

        valores = [convenio, particular]
        labels = [f"{LABEL_CONVENIO}\n{convenio}", f"{LABEL_PARTICULAR}\n{particular}"]
        cores = [get_color("success"), get_color("warning")]

        if sum(valores) > 0:
            ax.pie(
                valores, labels=labels, colors=cores, autopct="%1.0f%%",
                textprops={"color": cor_texto, "fontsize": 9},
                wedgeprops={"linewidth": 0},
            )
        ax.set_aspect("equal")

        self._fig_pizza = fig

        widget = self._embutir_figura(box, fig)
        widget.pack(padx=10, pady=(0, 12))

    def _grafico_barras_medico(self, parent, medicos):
        box = ctk.CTkFrame(
            parent, fg_color=get_color("surface"), corner_radius=14,
            border_width=1, border_color=get_color("border"),
        )
        box.pack(side="left", fill="both", expand=True, padx=(8, 0))

        ctk.CTkLabel(
            box, text="Consultas por médico", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color("accent"),
        ).pack(anchor="w", padx=14, pady=(12, 4))

        nomes = list(medicos.keys())
        totais = [sum(planos.values()) for planos in medicos.values()]

        cor_texto = get_color("text")
        cor_grade = get_color("border")
        fig, ax = self._criar_figura(figsize=(4.4, 2.8))

        ax.barh(nomes, totais, color=get_color("accent"))
        ax.set_xlabel("")
        ax.tick_params(colors=cor_texto, labelsize=9)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["bottom"].set_color(cor_grade)
        ax.invert_yaxis()  # primeiro médico no topo

        for i, v in enumerate(totais):
            ax.text(v + max(totais) * 0.02, i, str(v), color=cor_texto, fontsize=9, va="center")

        fig.tight_layout()
        self._fig_barras = fig

        widget = self._embutir_figura(box, fig)
        widget.pack(padx=10, pady=(0, 12), fill="both", expand=True)

    def _grafico_linha_por_dia(self, parent, por_dia):
        box = ctk.CTkFrame(
            parent, fg_color=get_color("surface"), corner_radius=14,
            border_width=1, border_color=get_color("border"),
        )
        box.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            box, text="Consultas por dia (no período)", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color("accent"),
        ).pack(anchor="w", padx=14, pady=(12, 4))

        # Ordena por data real (não pela string dd/mm/aaaa, que ordenaria
        # alfabeticamente errado) antes de plotar.
        dias_ordenados = sorted(por_dia.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y"))
        valores = [por_dia[d] for d in dias_ordenados]

        # Eixo X mostra só dia/mês (sem ano) para não poluir quando o
        # período tem muitos dias.
        labels_x = [datetime.strptime(d, "%d/%m/%Y").strftime("%d/%m") for d in dias_ordenados]

        cor_texto = get_color("text")
        cor_grade = get_color("border")
        fig, ax = self._criar_figura(figsize=(8.4, 2.6))

        ax.plot(labels_x, valores, color=get_color("accent"), linewidth=2)
        ax.fill_between(range(len(valores)), valores, color=get_color("accent"), alpha=0.15)
        ax.tick_params(colors=cor_texto, labelsize=8)
        ax.grid(axis="y", color=cor_grade, linewidth=0.5, alpha=0.5)
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Evita poluir o eixo X com um rótulo por dia quando o período é
        # longo (ex: último mês = 30+ pontos) — mostra só uma amostra.
        passo = max(1, len(labels_x) // 10)
        ax.set_xticks(range(0, len(labels_x), passo))
        ax.set_xticklabels(labels_x[::passo], rotation=0)

        fig.tight_layout()
        self._fig_linha = fig

        widget = self._embutir_figura(box, fig)
        widget.pack(padx=10, pady=(0, 12), fill="both", expand=True)

    # ──────────────────────────────────────────────────────────────────
    # DETALHAMENTO POR MÉDICO (lista, igual ao original)
    # ──────────────────────────────────────────────────────────────────
    def _lista_medicos(self, parent, dados):
        box = ctk.CTkFrame(
            parent, fg_color=get_color("surface"), corner_radius=14,
            border_width=1, border_color=get_color("border"),
        )
        box.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            box, text="Detalhamento por médico", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color("accent"),
        ).pack(anchor="w", padx=14, pady=(12, 8))

        for medico, planos in dados.items():
            sub = ctk.CTkFrame(box, fg_color=get_color("surface_alt"), corner_radius=10)
            sub.pack(fill="x", padx=14, pady=(0, 8))

            ctk.CTkLabel(
                sub, text=medico, font=ctk.CTkFont(weight="bold", size=13),
                text_color=get_color("text"),
            ).pack(anchor="w", padx=12, pady=(8, 4))

            for plano, qtd in planos.items():
                linha = ctk.CTkFrame(sub, fg_color="transparent")
                linha.pack(fill="x", padx=12, pady=2)

                ctk.CTkLabel(
                    linha, text=plano, text_color=get_color("text_secondary"),
                    font=ctk.CTkFont(size=12),
                ).pack(side="left")

                ctk.CTkLabel(
                    linha, text=str(qtd), text_color=get_color("accent"),
                    font=ctk.CTkFont(size=12, weight="bold"),
                ).pack(side="right")

            ctk.CTkFrame(sub, fg_color="transparent", height=4).pack()

    # ──────────────────────────────────────────────────────────────────
    # EXPORTAR PDF
    # ──────────────────────────────────────────────────────────────────
    def _exportar_pdf(self):
        if not self._dados_relatorio_atual:
            messagebox.showwarning(
                "Nada para exportar",
                "Não há consultas no período selecionado para gerar o relatório.",
            )
            return

        destino = filedialog.asksaveasfilename(
            title="Salvar relatório como PDF",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"relatorio_{self.filtro_atual.lower().replace(' ', '_')}.pdf",
        )
        if not destino:
            return

        # Monta o texto do período exibido no cabeçalho do PDF. Para o
        # filtro "Personalizado", inclui as datas escolhidas.
        if self.filtro_atual == "Personalizado" and self.data_inicio_personalizada and self.data_fim_personalizada:
            periodo_label = (
                f"Personalizado "
                f"({self.data_inicio_personalizada.strftime('%d/%m/%Y')} a "
                f"{self.data_fim_personalizada.strftime('%d/%m/%Y')})"
            )
        else:
            periodo_label = self.filtro_atual

        dados = self._dados_relatorio_atual
        try:
            exportar_relatorio_pdf(
                caminho_saida=destino,
                periodo_label=periodo_label,
                total=dados["total"],
                convenio=dados["convenio"],
                particular=dados["particular"],
                medicos=dados["medicos"],
                fig_pizza=self._fig_pizza,
                fig_barras=self._fig_barras,
                fig_linha=self._fig_linha,
            )
            messagebox.showinfo("Exportado", "Relatório em PDF gerado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro ao exportar", str(e))