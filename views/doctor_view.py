import customtkinter as ctk
from datetime import datetime
import os  # ✅ ADICIONADO


class DoctorView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=("white", "#1F2937")
)

        self.consultas = [
            {"hora": "08:00", "paciente": "João Silva", "cpf": "123.456.789-00"},
            {"hora": "08:30", "paciente": "Maria Souza", "cpf": "987.654.321-00"},
        ]

        self.historico = {}

        self.render_lista()

    def render_lista(self):
        for w in self.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(
            header,
            text="Consultas de hoje",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(anchor="w")

        lista = ctk.CTkScrollableFrame(self)
        lista.pack(fill="both", expand=True, padx=30, pady=10)

        for c in self.consultas:
            self.card_consulta(lista, c)

    # ===================== CARD CONSULTA =====================
    def card_consulta(self, parent, c):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8)

        box = ctk.CTkFrame(card, fg_color="transparent")
        box.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(box, text=c["hora"], width=70,
                     font=ctk.CTkFont(weight="bold")).pack(side="left")

        info = ctk.CTkFrame(box, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(info, text=c["paciente"],
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        ctk.CTkLabel(info, text=c["cpf"],
                     text_color="#6B7280").pack(anchor="w")

        # ✅ ADIÇÃO: MOSTRAR SE TEM ANEXOS
        if c.get("anexos"):
            ctk.CTkLabel(
                info,
                text="📎 Documentos disponíveis",
                text_color="#2563EB",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(anchor="w", pady=(4, 0))

        ctk.CTkButton(
            box,
            text="Atender",
            fg_color="#2563EB",
            command=lambda c=c: self.abrir_prontuario(c)
        ).pack(side="right")

    # ===================== PRONTUÁRIO =====================
    def abrir_prontuario(self, consulta):
        for w in self.winfo_children():
            w.destroy()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkButton(header, text="← Voltar",
                      command=self.render_lista).pack(side="left")

        ctk.CTkLabel(header,
                     text=consulta["paciente"],
                     font=ctk.CTkFont(size=20, weight="bold")
                     ).pack(side="left", padx=10)

        form = ctk.CTkFrame(container, fg_color="white", corner_radius=12)
        form.pack(fill="both", expand=True, pady=20)

        scroll = ctk.CTkScrollableFrame(form)
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        # ✅ ADIÇÃO: BLOCO DE ANEXOS
        if consulta.get("anexos"):
            ctk.CTkLabel(
                scroll,
                text="Documentos do paciente",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", pady=(0, 10))

            for arq in consulta["anexos"]:
                nome = os.path.basename(arq)

                ctk.CTkButton(
                    scroll,
                    text=f"Abrir {nome}",
                    fg_color="#E5E7EB",
                    text_color="#111827",
                    hover_color="#D1D5DB",
                    command=lambda a=arq: self.abrir_arquivo(a)
                ).pack(anchor="w", pady=2)

        # ===== FORM =====
        queixa = self.campo(scroll, "Queixa")
        observacoes = self.campo(scroll, "Observações")
        diagnostico = self.campo(scroll, "Diagnóstico")
        receita = self.campo(scroll, "Receita")
        exames = self.campo(scroll, "Exames")

        ctk.CTkLabel(
            scroll,
            text="Histórico do paciente",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(25, 10))

        lista_hist = ctk.CTkFrame(scroll, fg_color="transparent")
        lista_hist.pack(fill="x")

        historicos = self.historico.get(consulta["cpf"], [])

        if not historicos:
            ctk.CTkLabel(
                lista_hist,
                text="Sem histórico ainda",
                text_color="#6B7280"
            ).pack(anchor="w")
        else:
            for h in reversed(historicos):
                self.card_hist_premium(lista_hist, h)

        def salvar():
            registro = {
                "data": datetime.now().strftime("%d/%m/%Y"),
                "queixa": queixa.get("1.0", "end").strip(),
                "observacoes": observacoes.get("1.0", "end").strip(),
                "diagnostico": diagnostico.get("1.0", "end").strip(),
                "receita": receita.get("1.0", "end").strip(),
                "exames": exames.get("1.0", "end").strip()
            }

            if consulta["cpf"] not in self.historico:
                self.historico[consulta["cpf"]] = []

            self.historico[consulta["cpf"]].append(registro)

            self.abrir_prontuario(consulta)

        ctk.CTkButton(
            container,
            text="Salvar atendimento",
            fg_color="#059669",
            command=salvar
        ).pack()

    # ===================== ABRIR ARQUIVO =====================
    def abrir_arquivo(self, caminho):
        os.startfile(caminho)

    # ================= RESTO (INALTERADO) =================
    def card_hist_premium(self, parent, h):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=6)

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=12, pady=10)

        top = ctk.CTkFrame(container, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(
            top,
            text=f"📅 {h['data']}",
            font=ctk.CTkFont(weight="bold"),
            text_color="#2563EB"
        ).pack(side="left")

        ctk.CTkButton(
            top,
            text="Ver completo",
            width=110,
            fg_color="#E5E7EB",
            text_color="#111827",
            command=lambda h=h: self.ver_detalhes(h)
        ).pack(side="right")

        resumo = ctk.CTkFrame(container, fg_color="transparent")
        resumo.pack(fill="x", pady=(5, 0))

        ctk.CTkLabel(
            resumo,
            text=f"Queixa: {h['queixa']}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            resumo,
            text=f"Diagnóstico: {h['diagnostico']}",
            text_color="#374151"
        ).pack(anchor="w")

    def ver_detalhes(self, h):
        popup = ctk.CTkToplevel(self)

        popup.geometry("520x520")
        popup.grab_set()

        frame = ctk.CTkScrollableFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text=f"📅 {h['data']}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=10)

        campos = [
            ("Queixa", h["queixa"]),
            ("Observações", h["observacoes"]),
            ("Diagnóstico", h["diagnostico"]),
            ("Receita", h["receita"]),
            ("Exames", h["exames"]),
        ]

        for titulo, valor in campos:
            ctk.CTkLabel(frame, text=titulo,
                         font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))

            ctk.CTkLabel(
                frame,
                text=valor or "-",
                wraplength=460,
                justify="left"
            ).pack(anchor="w")

    def campo(self, parent, titulo):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.pack(fill="x", pady=8)

        ctk.CTkLabel(box, text=titulo,
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        entry = ctk.CTkTextbox(box, height=70)
        entry.pack(fill="x")

        return entry