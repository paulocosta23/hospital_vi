import customtkinter as ctk
from .theme import get_color


class ReportsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=get_color("bg"))

        self.consultas = [
            {"medico": "Dr. Carlos", "tipo": "Particular", "plano": ""},
            {"medico": "Dr. Ana",    "tipo": "Convênio",   "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Convênio",   "plano": "Hapvida"},
            {"medico": "Dr. Ana",    "tipo": "Convênio",   "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Convênio",   "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Particular", "plano": ""},
        ]

        self.render()

    # ── render ──────────────────────────────────────────────────────────────

    def render(self):
        for w in self.winfo_children():
            w.destroy()

        # Cabeçalho — igual ao padrão das outras views
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 4))

        ctk.CTkLabel(
            header,
            text="Relatórios",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=get_color("text"),
        ).pack(side="left")

        # Área scrollável
        self.area = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=get_color("border"),
            scrollbar_button_hover_color=get_color("accent"),
        )
        self.area.pack(fill="both", expand=True, padx=20, pady=(6, 16))

        self.update_data()

    # ── dados ────────────────────────────────────────────────────────────────

    def update_data(self):
        dados = self.consultas
        total     = len(dados)
        convenio  = len([c for c in dados if c["tipo"] == "Convênio"])
        particular = len([c for c in dados if c["tipo"] == "Particular"])

        medicos: dict = {}
        planos:  dict = {}

        for c in dados:
            plano  = c["plano"] if c["plano"] else "Particular"
            medico = c["medico"]
            planos[plano] = planos.get(plano, 0) + 1
            medicos.setdefault(medico, {})
            medicos[medico][plano] = medicos[medico].get(plano, 0) + 1

        # ── linha de cards de resumo ─────────────────────────────────────────
        row = ctk.CTkFrame(self.area, fg_color="transparent")
        row.pack(fill="x", pady=(4, 12))
        row.columnconfigure((0, 1, 2), weight=1, uniform="col")

        self._summary_card(row, "Total",      str(total),      col=0)
        self._summary_card(row, "Convênios",  str(convenio),   col=1)
        self._summary_card(row, "Particular", str(particular), col=2)

        # ── gráfico ──────────────────────────────────────────────────────────
        self._grafico(planos)

        # ── lista por médico ─────────────────────────────────────────────────
        self._lista_medicos(medicos)

    # ── widgets ──────────────────────────────────────────────────────────────

    def _summary_card(self, parent, titulo: str, valor: str, col: int):
        card = ctk.CTkFrame(
            parent,
            fg_color=get_color("surface"),
            corner_radius=12,
            border_width=1,
            border_color=get_color("border"),
        )
        card.grid(row=0, column=col, padx=6, pady=0, sticky="nsew")

        ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(size=12),
            text_color=get_color("text_secondary"),
            fg_color="transparent",
        ).pack(pady=(14, 2))

        ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=get_color("text"),
            fg_color="transparent",
        ).pack(pady=(0, 14))

    def _grafico(self, dados: dict):
        box = ctk.CTkFrame(
            self.area,
            fg_color=get_color("surface"),
            corner_radius=12,
            border_width=1,
            border_color=get_color("border"),
        )
        box.pack(fill="x", pady=6)

        ctk.CTkLabel(
            box,
            text="Planos",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color("text"),
            fg_color="transparent",
        ).pack(anchor="w", padx=16, pady=(14, 0))

        # Separador fino
        ctk.CTkFrame(box, height=1, fg_color=get_color("border")).pack(
            fill="x", padx=16, pady=(8, 0)
        )

        canvas = ctk.CTkCanvas(
            box,
            height=200,
            bg=get_color("surface"),
            highlightthickness=0,
        )
        canvas.pack(fill="x", padx=16, pady=(10, 16))

        if not dados:
            return

        # Desenha barras após o widget estar visível
        canvas.bind(
            "<Configure>",
            lambda e, d=dados, c=canvas: self._draw_bars(c, d, e.width),
        )

    def _draw_bars(self, canvas, dados: dict, canvas_width: int):
        canvas.delete("all")
        if not dados:
            return

        accent     = get_color("accent")
        text_color = get_color("text_secondary")
        base_y     = 160
        max_val    = max(dados.values())
        n          = len(dados)
        bar_w      = min(50, (canvas_width - 60) // max(n, 1) - 20)
        gap        = (canvas_width - bar_w * n) // (n + 1)
        x          = gap

        for nome, valor in dados.items():
            h        = int((valor / max_val) * 110)
            top_y    = base_y - h
            radius   = 6

            # Barra com topo arredondado (simulado com retângulo + oval)
            canvas.create_rectangle(
                x, top_y + radius, x + bar_w, base_y,
                fill=accent, outline="",
            )
            canvas.create_oval(
                x, top_y, x + bar_w, top_y + radius * 2,
                fill=accent, outline="",
            )

            # Valor acima da barra
            canvas.create_text(
                x + bar_w / 2, top_y - 12,
                text=str(valor),
                fill=get_color("text"),
                font=("", 11, "bold"),
            )

            # Label abaixo
            canvas.create_text(
                x + bar_w / 2, base_y + 16,
                text=nome,
                fill=text_color,
                font=("", 10),
            )

            x += bar_w + gap

        # Linha de base
        canvas.create_line(
            0, base_y, canvas_width, base_y,
            fill=get_color("border"), width=1,
        )

    def _lista_medicos(self, dados: dict):
        box = ctk.CTkFrame(
            self.area,
            fg_color=get_color("surface"),
            corner_radius=12,
            border_width=1,
            border_color=get_color("border"),
        )
        box.pack(fill="x", pady=6)

        ctk.CTkLabel(
            box,
            text="Por médico",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color("text"),
            fg_color="transparent",
        ).pack(anchor="w", padx=16, pady=(14, 0))

        ctk.CTkFrame(box, height=1, fg_color=get_color("border")).pack(
            fill="x", padx=16, pady=(8, 8)
        )

        for i, (medico, planos) in enumerate(dados.items()):
            # Card por médico
            sub = ctk.CTkFrame(
                box,
                fg_color=get_color("surface_alt"),
                corner_radius=10,
            )
            sub.pack(fill="x", padx=12, pady=(0, 8))

            # Nome do médico
            ctk.CTkLabel(
                sub,
                text=medico,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=get_color("text"),
                fg_color="transparent",
            ).pack(anchor="w", padx=14, pady=(10, 6))

            # Linhas de plano
            for plano, qtd in planos.items():
                linha = ctk.CTkFrame(sub, fg_color="transparent")
                linha.pack(fill="x", padx=14, pady=3)

                ctk.CTkLabel(
                    linha,
                    text=plano,
                    font=ctk.CTkFont(size=12),
                    text_color=get_color("text_secondary"),
                    fg_color="transparent",
                ).pack(side="left")

                # Badge de quantidade
                badge = ctk.CTkFrame(
                    linha,
                    fg_color=get_color("button"),
                    corner_radius=8,
                    width=28,
                    height=22,
                )
                badge.pack(side="right")
                badge.pack_propagate(False)

                ctk.CTkLabel(
                    badge,
                    text=str(qtd),
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#FFFFFF",
                    fg_color="transparent",
                ).place(relx=0.5, rely=0.5, anchor="center")

            # Espaço inferior interno
            ctk.CTkFrame(sub, height=6, fg_color="transparent").pack()

        # Padding inferior do box
        ctk.CTkFrame(box, height=8, fg_color="transparent").pack()