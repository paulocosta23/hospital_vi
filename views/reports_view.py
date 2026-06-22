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

        # Cabeçalho
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(28, 8))

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="y")

        # Eyebrow label acima do título
        ctk.CTkLabel(
            title_frame,
            text="CLÍNICA MÉDICA  ·  GESTÃO",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="#4A7FD4",
            fg_color="transparent",
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Relatórios",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=get_color("text"),
        ).pack(anchor="w")

        # Linha decorativa sob o título
        accent_line = ctk.CTkFrame(self, height=2, fg_color="#2D5FA8", corner_radius=1)
        accent_line.pack(fill="x", padx=32, pady=(0, 20))

        # Área scrollável
        self.area = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=get_color("border"),
            scrollbar_button_hover_color=get_color("accent"),
        )
        self.area.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        self.update_data()

    # ── dados ────────────────────────────────────────────────────────────────

    def update_data(self):
        dados = self.consultas
        total      = len(dados)
        convenio   = len([c for c in dados if c["tipo"] == "Convênio"])
        particular = len([c for c in dados if c["tipo"] == "Particular"])

        medicos: dict = {}
        planos:  dict = {}

        for c in dados:
            plano  = c["plano"] if c["plano"] else "Particular"
            medico = c["medico"]
            planos[plano] = planos.get(plano, 0) + 1
            medicos.setdefault(medico, {})
            medicos[medico][plano] = medicos[medico].get(plano, 0) + 1

        # ── cards de resumo ──────────────────────────────────────────────────
        row = ctk.CTkFrame(self.area, fg_color="transparent")
        row.pack(fill="x", pady=(4, 16))
        row.columnconfigure((0, 1, 2), weight=1, uniform="col")

        cards_data = [
            ("Total", str(total), "#1A3A6B", "#4A7FD4"),
            ("Convênios", str(convenio), "#0F3D2E", "#1D9E75"),
            ("Particular", str(particular), "#3D1A1A", "#D85A30"),
        ]

        for i, (titulo, valor, bg, accent) in enumerate(cards_data):
            self._summary_card(row, titulo, valor, col=i, bg=bg, accent=accent)

        # ── gráfico ──────────────────────────────────────────────────────────
        self._grafico(planos)

        # ── lista por médico ─────────────────────────────────────────────────
        self._lista_medicos(medicos)

    # ── widgets ──────────────────────────────────────────────────────────────

    def _summary_card(self, parent, titulo: str, valor: str, col: int,
                      bg: str = None, accent: str = None):
        bg_color     = bg     or get_color("surface")
        accent_color = accent or get_color("accent")

        card = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=14,
            border_width=1,
            border_color=accent_color,
        )
        card.grid(row=0, column=col, padx=6, pady=0, sticky="nsew")

        # Barra de topo colorida
        top_bar = ctk.CTkFrame(card, height=4, fg_color=accent_color, corner_radius=0)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=titulo.upper(),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=accent_color,
            fg_color="transparent",
        ).pack(pady=(14, 2))

        ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#FFFFFF",
            fg_color="transparent",
        ).pack(pady=(0, 16))

    def _grafico(self, dados: dict):
        # Wrapper com sombra simulada (frame maior levemente deslocado)
        outer = ctk.CTkFrame(
            self.area,
            fg_color=get_color("border"),
            corner_radius=14,
        )
        outer.pack(fill="x", pady=(0, 14), padx=1)

        box = ctk.CTkFrame(
            outer,
            fg_color=get_color("surface"),
            corner_radius=13,
            border_width=0,
        )
        box.pack(fill="both", expand=True, padx=1, pady=1)

        # Cabeçalho da seção
        hdr = ctk.CTkFrame(box, fg_color="transparent")
        hdr.pack(fill="x", padx=18, pady=(16, 0))

        # Ícone simulado com quadradinho colorido
        dot = ctk.CTkFrame(hdr, width=4, height=20, fg_color="#4A7FD4", corner_radius=2)
        dot.pack(side="left", padx=(0, 10))
        dot.pack_propagate(False)

        ctk.CTkLabel(
            hdr,
            text="Distribuição por Plano",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color("text"),
            fg_color="transparent",
        ).pack(side="left")

        ctk.CTkFrame(box, height=1, fg_color=get_color("border")).pack(
            fill="x", padx=18, pady=(12, 0)
        )

        canvas = ctk.CTkCanvas(
            box,
            height=220,
            bg=get_color("surface"),
            highlightthickness=0,
        )
        canvas.pack(fill="x", padx=18, pady=(12, 18))

        if not dados:
            return

        canvas.bind(
            "<Configure>",
            lambda e, d=dados, c=canvas: self._draw_bars(c, d, e.width),
        )

    def _draw_bars(self, canvas, dados: dict, canvas_width: int):
        canvas.delete("all")
        if not dados:
            return

        # Paleta de cores para as barras (uma cor por plano)
        cores = ["#4A7FD4", "#1D9E75", "#D85A30", "#E8B84B", "#9B6FD4"]
        text_color = get_color("text_secondary")
        base_y     = 170
        max_val    = max(dados.values())
        n          = len(dados)
        bar_w      = min(60, (canvas_width - 80) // max(n, 1) - 16)
        gap        = (canvas_width - bar_w * n) // (n + 1)
        x          = gap

        # Linhas de grade horizontais
        for frac in [0.25, 0.5, 0.75, 1.0]:
            y = base_y - int(frac * 120)
            canvas.create_line(
                0, y, canvas_width, y,
                fill=get_color("border"), width=1, dash=(4, 6),
            )

        for i, (nome, valor) in enumerate(dados.items()):
            cor   = cores[i % len(cores)]
            h     = int((valor / max_val) * 120)
            top_y = base_y - h
            r     = 6

            # Sombra da barra (deslocada 2px)
            shadow = self._hex_alpha(cor, 0.25)
            canvas.create_rectangle(
                x + 2, top_y + r + 2, x + bar_w + 2, base_y + 2,
                fill=shadow, outline="",
            )

            # Barra principal com topo arredondado
            canvas.create_rectangle(
                x, top_y + r, x + bar_w, base_y,
                fill=cor, outline="",
            )
            canvas.create_oval(
                x, top_y, x + bar_w, top_y + r * 2,
                fill=cor, outline="",
            )

            # Brilho sutil no topo da barra
            highlight = self._hex_alpha("#FFFFFF", 0.15)
            canvas.create_rectangle(
                x + 2, top_y + r, x + bar_w // 2, top_y + r + h // 3,
                fill=highlight, outline="",
            )

            # Valor acima da barra — com fundo pill
            pill_x1 = x + bar_w / 2 - 14
            pill_x2 = x + bar_w / 2 + 14
            pill_y1 = top_y - 26
            pill_y2 = top_y - 8
            canvas.create_oval(pill_x1, pill_y1, pill_x1 + 8, pill_y2, fill=cor, outline="")
            canvas.create_oval(pill_x2 - 8, pill_y1, pill_x2, pill_y2, fill=cor, outline="")
            canvas.create_rectangle(pill_x1 + 4, pill_y1, pill_x2 - 4, pill_y2, fill=cor, outline="")
            canvas.create_text(
                x + bar_w / 2, top_y - 17,
                text=str(valor),
                fill="#FFFFFF",
                font=("", 10, "bold"),
            )

            # Label abaixo com cor do plano
            canvas.create_text(
                x + bar_w / 2, base_y + 18,
                text=nome,
                fill=get_color("text"),
                font=("", 11),
            )

            # Indicador de cor (pequeno quadrado abaixo do label)
            sq = 8
            sx = x + bar_w / 2 - sq / 2
            canvas.create_rectangle(
                sx, base_y + 32, sx + sq, base_y + 32 + sq,
                fill=cor, outline="",
            )

            x += bar_w + gap

        # Linha de base
        canvas.create_line(
            0, base_y, canvas_width, base_y,
            fill=get_color("border"), width=1,
        )

    @staticmethod
    def _hex_alpha(hex_color: str, alpha: float) -> str:
        """Retorna cor com transparência simulada misturando com preto."""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = int(r * alpha)
        g = int(g * alpha)
        b = int(b * alpha)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _lista_medicos(self, dados: dict):
        outer = ctk.CTkFrame(
            self.area,
            fg_color=get_color("border"),
            corner_radius=14,
        )
        outer.pack(fill="x", pady=(0, 14), padx=1)

        box = ctk.CTkFrame(
            outer,
            fg_color=get_color("surface"),
            corner_radius=13,
        )
        box.pack(fill="both", expand=True, padx=1, pady=1)

        # Cabeçalho da seção
        hdr = ctk.CTkFrame(box, fg_color="transparent")
        hdr.pack(fill="x", padx=18, pady=(16, 0))

        dot = ctk.CTkFrame(hdr, width=4, height=20, fg_color="#1D9E75", corner_radius=2)
        dot.pack(side="left", padx=(0, 10))
        dot.pack_propagate(False)

        ctk.CTkLabel(
            hdr,
            text="Atendimentos por Médico",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color("text"),
            fg_color="transparent",
        ).pack(side="left")

        ctk.CTkFrame(box, height=1, fg_color=get_color("border")).pack(
            fill="x", padx=18, pady=(12, 12)
        )

        # Cores dos badges por índice de médico
        badge_cores = [
            ("#1A3A6B", "#4A7FD4"),  # azul
            ("#0F3D2E", "#1D9E75"),  # verde
            ("#3D1A1A", "#D85A30"),  # coral
        ]

        for i, (medico, planos) in enumerate(dados.items()):
            bg_badge, fg_badge = badge_cores[i % len(badge_cores)]

            sub = ctk.CTkFrame(
                box,
                fg_color=get_color("surface_alt"),
                corner_radius=10,
                border_width=1,
                border_color=get_color("border"),
            )
            sub.pack(fill="x", padx=14, pady=(0, 10))

            # Cabeçalho do card de médico com avatar
            med_hdr = ctk.CTkFrame(sub, fg_color="transparent")
            med_hdr.pack(fill="x", padx=14, pady=(12, 8))

            # Avatar circular com iniciais
            inicial = medico.replace("Dr. ", "").replace("Dra. ", "")[0].upper()
            avatar = ctk.CTkFrame(
                med_hdr,
                width=32, height=32,
                fg_color=fg_badge,
                corner_radius=16,
            )
            avatar.pack(side="left", padx=(0, 10))
            avatar.pack_propagate(False)
            ctk.CTkLabel(
                avatar,
                text=inicial,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#FFFFFF",
                fg_color="transparent",
            ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                med_hdr,
                text=medico,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=get_color("text"),
                fg_color="transparent",
            ).pack(side="left")

            # Total de atendimentos do médico (badge à direita)
            total_med = sum(planos.values())
            total_badge = ctk.CTkFrame(
                med_hdr,
                fg_color=bg_badge,
                corner_radius=10,
                width=60, height=22,
            )
            total_badge.pack(side="right")
            total_badge.pack_propagate(False)
            ctk.CTkLabel(
                total_badge,
                text=f"{total_med} atend.",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=fg_badge,
                fg_color="transparent",
            ).place(relx=0.5, rely=0.5, anchor="center")

            # Separador interno
            ctk.CTkFrame(sub, height=1, fg_color=get_color("border")).pack(
                fill="x", padx=14, pady=(0, 8)
            )

            # Linhas de plano com barra de progresso
            total_med = sum(planos.values()) or 1
            for plano, qtd in planos.items():
                linha = ctk.CTkFrame(sub, fg_color="transparent")
                linha.pack(fill="x", padx=14, pady=(0, 8))

                # Nome do plano
                ctk.CTkLabel(
                    linha,
                    text=plano,
                    font=ctk.CTkFont(size=12),
                    text_color=get_color("text_secondary"),
                    fg_color="transparent",
                    width=80,
                    anchor="w",
                ).pack(side="left")

                # Barra de progresso
                prog_outer = ctk.CTkFrame(
                    linha,
                    height=6,
                    fg_color=get_color("border"),
                    corner_radius=3,
                )
                prog_outer.pack(side="left", fill="x", expand=True, padx=(8, 10))
                prog_outer.pack_propagate(False)

                pct = qtd / total_med
                if pct > 0:
                    prog_inner = ctk.CTkFrame(
                        prog_outer,
                        height=6,
                        fg_color=fg_badge,
                        corner_radius=3,
                    )
                    prog_inner.place(relx=0, rely=0, relwidth=pct, relheight=1)

                # Badge de quantidade
                badge = ctk.CTkFrame(
                    linha,
                    fg_color=bg_badge,
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
                    text_color=fg_badge,
                    fg_color="transparent",
                ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkFrame(sub, height=4, fg_color="transparent").pack()

        ctk.CTkFrame(box, height=10, fg_color="transparent").pack()