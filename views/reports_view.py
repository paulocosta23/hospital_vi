import customtkinter as ctk
from .theme import get_color


class ReportsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=get_color("bg"))

        self.consultas = [
            {"medico": "Dr. Carlos", "tipo": "Particular", "plano": ""},
            {"medico": "Dr. Ana", "tipo": "Convênio", "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Convênio", "plano": "Hapvida"},
            {"medico": "Dr. Ana", "tipo": "Convênio", "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Convênio", "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Particular", "plano": ""},
        ]

        self.render()

    def render(self):
        for w in self.winfo_children():
            w.destroy()

        titulo = ctk.CTkLabel(
            self,
            text="Relatórios",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=get_color("text"),
        )
        titulo.pack(anchor="w", padx=30, pady=15)

        self.area = ctk.CTkScrollableFrame(self)
        self.area.pack(fill="both", expand=True, padx=20, pady=10)

        self.update_data()

    def update_data(self):
        dados = self.consultas
        total = len(dados)
        convenio = len([c for c in dados if c["tipo"] == "Convênio"])
        particular = len([c for c in dados if c["tipo"] == "Particular"])

        medicos = {}
        planos = {}

        for c in dados:
            plano = c["plano"] if c["plano"] else "Particular"
            medico = c["medico"]

            planos[plano] = planos.get(plano, 0) + 1

            if medico not in medicos:
                medicos[medico] = {}

            medicos[medico][plano] = medicos[medico].get(plano, 0) + 1

        cards = ctk.CTkFrame(self.area, fg_color="transparent")
        cards.pack(fill="x", pady=10)

        self.card(cards, "Total", total)
        self.card(cards, "Convênios", convenio)
        self.card(cards, "Particular", particular)

        self.grafico(planos)
        self.lista_medicos(medicos)

    def card(self, parent, titulo, valor):
        card = ctk.CTkFrame(parent, fg_color=get_color("surface"), corner_radius=10)
        card.pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkLabel(
            card,
            text=titulo,
            text_color=get_color("text_secondary"),
            fg_color=get_color("surface"),
        ).pack(pady=(8, 2))

        ctk.CTkLabel(
            card,
            text=str(valor),
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color=get_color("surface"),
            text_color=get_color("text"),
        ).pack(pady=(0, 8))

    def grafico(self, dados):
        box = ctk.CTkFrame(self.area, fg_color=get_color("surface"), corner_radius=10)
        box.pack(fill="x", pady=10)

        ctk.CTkLabel(
            box,
            text="Planos",
            font=ctk.CTkFont(weight="bold"),
            fg_color=get_color("surface"),
            text_color=get_color("text"),
        ).pack(anchor="w", padx=10, pady=10)

        canvas = ctk.CTkCanvas(
            box,
            width=350,
            height=180,
            bg=get_color("surface"),
            highlightthickness=0,
        )
        canvas.pack(pady=10)

        if not dados:
            return

        max_val = max(dados.values())
        largura = 40
        espacamento = 30
        base = 140
        x = 20

        for nome, valor in dados.items():
            altura = (valor / max_val) * 100
            canvas.create_rectangle(
                x,
                base - altura,
                x + largura,
                base,
                fill=get_color("accent"),
                outline="",
            )
            canvas.create_text(x + largura / 2, base - altura - 10, text=str(valor))
            canvas.create_text(x + largura / 2, base + 12, text=nome)
            x += largura + espacamento

    def lista_medicos(self, dados):
        box = ctk.CTkFrame(self.area, fg_color=get_color("surface"), corner_radius=10)
        box.pack(fill="x", pady=10)

        ctk.CTkLabel(
            box,
            text="Por médico",
            font=ctk.CTkFont(weight="bold"),
            fg_color=get_color("surface"),
            text_color=get_color("text"),
        ).pack(anchor="w", padx=10, pady=10)

        for medico, planos in dados.items():
            sub = ctk.CTkFrame(box, fg_color=get_color("surface_alt"), corner_radius=8)
            sub.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(
                sub,
                text=medico,
                font=ctk.CTkFont(weight="bold"),
                fg_color=get_color("surface_alt"),
                text_color=get_color("text"),
            ).pack(anchor="w", padx=10, pady=5)

            for plano, qtd in planos.items():
                linha = ctk.CTkFrame(sub, fg_color=get_color("surface_alt"))
                linha.pack(fill="x", padx=10, pady=2)

                ctk.CTkLabel(
                    linha,
                    text=plano,
                    fg_color=get_color("surface_alt"),
                    text_color=get_color("text_secondary"),
                ).pack(side="left")

                ctk.CTkLabel(
                    linha,
                    text=str(qtd),
                    text_color=get_color("accent"),
                    fg_color=get_color("surface_alt"),
                ).pack(side="right")