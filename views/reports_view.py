import customtkinter as ctk
from tkinter import filedialog, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class ReportsView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=("white", "#1F2937"))

        # DADOS
        self.consultas = [
            {"medico": "Dr. Carlos", "tipo": "Particular", "plano": ""},
            {"medico": "Dr. Ana", "tipo": "Convênio", "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Convênio", "plano": "Hapvida"},
            {"medico": "Dr. Ana", "tipo": "Convênio", "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Convênio", "plano": "Unimed"},
            {"medico": "Dr. Carlos", "tipo": "Particular", "plano": ""},
        ]

        self.render()

    # ================= UI =================
    def render(self):
        for w in self.winfo_children():
            w.destroy()

        titulo = ctk.CTkLabel(
            self,
            text="Relatórios",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#111827"
        )
        titulo.pack(anchor="w", padx=30, pady=15)

        btn_pdf = ctk.CTkButton(
            self,
            text="Exportar PDF",
            command=self.exportar_pdf,
            width=140,
            height=35
        )
        btn_pdf.pack(anchor="e", padx=30)

        # SCROLL (resolve corte de tela)
        self.area = ctk.CTkScrollableFrame(self)
        self.area.pack(fill="both", expand=True, padx=20, pady=10)

        self.update_data()

    # ================= DADOS =================
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

        # ================= CARDS =================
        cards = ctk.CTkFrame(self.area, fg_color="transparent")
        cards.pack(fill="x", pady=10)

        self.card(cards, "Total", total)
        self.card(cards, "Convênios", convenio)
        self.card(cards, "Particular", particular)

        # ================= GRÁFICO =================
        self.grafico(planos)

        # ================= MÉDICOS =================
        self.lista_medicos(medicos)

    # ================= CARD =================
    def card(self, parent, titulo, valor):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=10)
        card.pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkLabel(
            card,
            text=titulo,
            text_color="#6B7280",
            fg_color="#FFFFFF"
        ).pack(pady=(8, 2))

        ctk.CTkLabel(
            card,
            text=str(valor),
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#FFFFFF"
        ).pack(pady=(0, 8))

    # ================= GRÁFICO =================
    def grafico(self, dados):
        box = ctk.CTkFrame(self.area, fg_color="#FFFFFF", corner_radius=10)
        box.pack(fill="x", pady=10)

        ctk.CTkLabel(
            box,
            text="Planos",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#FFFFFF"
        ).pack(anchor="w", padx=10, pady=10)

        canvas = ctk.CTkCanvas(
            box,
            width=350,
            height=180,
            bg="#FFFFFF",
            highlightthickness=0
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
                fill="#2563EB",
                outline=""
            )

            canvas.create_text(
                x + largura / 2,
                base - altura - 10,
                text=str(valor)
            )

            canvas.create_text(
                x + largura / 2,
                base + 12,
                text=nome
            )

            x += largura + espacamento

    # ================= LISTA =================
    def lista_medicos(self, dados):
        box = ctk.CTkFrame(self.area, fg_color="#FFFFFF", corner_radius=10)
        box.pack(fill="x", pady=10)

        ctk.CTkLabel(
            box,
            text="Por médico",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#FFFFFF"
        ).pack(anchor="w", padx=10, pady=10)

        for medico, planos in dados.items():
            sub = ctk.CTkFrame(box, fg_color="#F9FAFB", corner_radius=8)
            sub.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(
                sub,
                text=medico,
                font=ctk.CTkFont(weight="bold"),
                fg_color="#F9FAFB"
            ).pack(anchor="w", padx=10, pady=5)

            for plano, qtd in planos.items():
                linha = ctk.CTkFrame(sub, fg_color="#F9FAFB")
                linha.pack(fill="x", padx=10, pady=2)

                ctk.CTkLabel(
                    linha,
                    text=plano,
                    fg_color="#F9FAFB"
                ).pack(side="left")

                ctk.CTkLabel(
                    linha,
                    text=str(qtd),
                    text_color="#2563EB",
                    fg_color="#F9FAFB"
                ).pack(side="right")

    # ================= EXPORTAR PDF =================
    def exportar_pdf(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Salvar relatório"
        )

        if not caminho:
            return

        try:
            pdf = SimpleDocTemplate(caminho)
            styles = getSampleStyleSheet()

            elementos = []

            elementos.append(
                Paragraph("RELATÓRIO DE CONSULTAS", styles["Title"])
            )

            elementos.append(Spacer(1, 20))

            total = len(self.consultas)
            convenio = len(
                [c for c in self.consultas if c["tipo"] == "Convênio"]
            )
            particular = len(
                [c for c in self.consultas if c["tipo"] == "Particular"]
            )

            elementos.append(
                Paragraph(f"Total de consultas: {total}", styles["Normal"])
            )

            elementos.append(
                Paragraph(f"Consultas por convênio: {convenio}", styles["Normal"])
            )

            elementos.append(
                Paragraph(f"Consultas particulares: {particular}", styles["Normal"])
            )

            elementos.append(Spacer(1, 20))

            elementos.append(
                Paragraph("ATENDIMENTOS POR PLANO", styles["Heading2"])
            )

            planos = {}

            for consulta in self.consultas:
                plano = consulta["plano"] if consulta["plano"] else "Particular"
                planos[plano] = planos.get(plano, 0) + 1

            for plano, qtd in planos.items():
                elementos.append(
                    Paragraph(
                        f"{plano}: {qtd} atendimento(s)",
                        styles["Normal"]
                    )
                )

            elementos.append(Spacer(1, 20))

            elementos.append(
                Paragraph("ATENDIMENTOS POR MÉDICO", styles["Heading2"])
            )

            medicos = {}

            for consulta in self.consultas:

                medico = consulta["medico"]
                plano = consulta["plano"] if consulta["plano"] else "Particular"

                if medico not in medicos:
                    medicos[medico] = {}

                medicos[medico][plano] = (
                    medicos[medico].get(plano, 0) + 1
                )

            for medico, dados in medicos.items():

                elementos.append(
                    Paragraph(
                        f"<b>{medico}</b>",
                        styles["Heading3"]
                    )
                )

                total_medico = sum(dados.values())

                elementos.append(
                    Paragraph(
                        f"Total de atendimentos: {total_medico}",
                        styles["Normal"]
                    )
                )

                for plano, qtd in dados.items():

                    elementos.append(
                        Paragraph(
                            f"• {plano}: {qtd} atendimento(s)",
                            styles["Normal"]
                        )
                    )

                elementos.append(Spacer(1, 10))

            elementos.append(Spacer(1, 20))

            elementos.append(
                Paragraph("LISTA COMPLETA DE CONSULTAS", styles["Heading2"])
            )

            for i, consulta in enumerate(self.consultas, start=1):

                medico = consulta["medico"]
                tipo = consulta["tipo"]
                plano = consulta["plano"] if consulta["plano"] else "Particular"

                elementos.append(
                    Paragraph(
                        f"{i}. Médico: {medico} | Tipo: {tipo} | Plano: {plano}",
                        styles["Normal"]
                    )
                )

            pdf.build(elementos)

            messagebox.showinfo(
                "Sucesso",
                "Relatório exportado com sucesso!"
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível gerar o PDF.\n\n{erro}"
            )