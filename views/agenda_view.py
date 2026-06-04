import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import filedialog
import os


class AgendaView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # ================= THEME =================
        self.bg = "#0B2A4A"
        self.panel = "#0F3A66"
        self.card = "#FFFFFF"
        self.soft = "#EAF2FF"
        self.primary = "#2EC7E6"
        self.accent = "#1E88E5"
        self.text_dark = "#0F172A"

        self.configure(fg_color=self.bg)

        self.data_atual = datetime.now()

        self.medicos = ["Dr. Carlos", "Dr. Ana"]
        self.consultas = []

        # ================= HEADER =================
        header = ctk.CTkFrame(
            self,
            fg_color=self.panel,
            corner_radius=25,
            height=100
        )
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="📅 Agenda Clínica",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).place(x=25, y=20)

        ctk.CTkLabel(
            header,
            text="Gestão de consultas médicas",
            font=ctk.CTkFont(size=13),
            text_color="#BFD7FF"
        ).place(x=25, y=55)

        # ================= CONTROLES DATA =================
        data_frame = ctk.CTkFrame(header, fg_color="transparent")
        data_frame.pack(side="right", padx=15, pady=20)

        ctk.CTkButton(
            data_frame,
            text="◀",
            width=35,
            fg_color=self.soft,
            text_color=self.accent,
            command=self.voltar
        ).pack(side="left", padx=2)

        self.label_data = ctk.CTkLabel(
            data_frame,
            text="",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_data.pack(side="left", padx=10)

        ctk.CTkButton(
            data_frame,
            text="▶",
            width=35,
            fg_color=self.soft,
            text_color=self.accent,
            command=self.avancar
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            data_frame,
            text="Hoje",
            width=60,
            fg_color=self.primary,
            hover_color="#1B9BD1",
            command=self.ir_hoje
        ).pack(side="left", padx=5)

        self.input_data = ctk.CTkEntry(
            data_frame,
            width=110,
            placeholder_text="dd/mm/aaaa"
        )
        self.input_data.pack(side="left", padx=5)

        ctk.CTkButton(
            data_frame,
            text="Ir",
            width=40,
            fg_color=self.accent,
            command=self.ir_data
        ).pack(side="left")

        # ================= NOVA CONSULTA =================
        ctk.CTkButton(
            header,
            text="+ Nova consulta",
            fg_color=self.primary,
            hover_color="#1B9BD1",
            corner_radius=18,
            command=lambda: self.popup()
        ).pack(side="right", padx=15)

        # ================= LISTA =================
        self.lista = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.lista.pack(fill="both", expand=True, padx=20, pady=10)

        self.update_data()
        self.render()

    # ================= DATA =================
    def update_data(self):
        self.label_data.configure(
            text=self.data_atual.strftime("%d/%m/%Y")
        )

    def avancar(self):
        self.data_atual += timedelta(days=1)
        self.update_data()
        self.render()

    def voltar(self):
        self.data_atual -= timedelta(days=1)
        self.update_data()
        self.render()

    def ir_hoje(self):
        self.data_atual = datetime.now()
        self.update_data()
        self.render()

    def ir_data(self):
        try:
            self.data_atual = datetime.strptime(
                self.input_data.get(),
                "%d/%m/%Y"
            )
            self.update_data()
            self.render()
        except:
            print("Data inválida")

    # ================= UTIL =================
    def formatar_cpf(self, texto):
        nums = ''.join(filter(str.isdigit, texto))[:11]
        if len(nums) <= 3:
            return nums
        elif len(nums) <= 6:
            return f"{nums[:3]}.{nums[3:]}"
        elif len(nums) <= 9:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:]}"
        return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"

    def ocultar_cpf(self, cpf):
        nums = ''.join(filter(str.isdigit, cpf))
        if len(nums) < 11:
            return cpf
        return f"{nums[:3]}.***.***-{nums[-2:]}"

    # ================= RENDER =================
    def render(self):
        for w in self.lista.winfo_children():
            w.destroy()

        data = self.data_atual.strftime("%d/%m/%Y")
        consultas = [c for c in self.consultas if c["data"] == data]

        if not consultas:
            ctk.CTkLabel(
                self.lista,
                text="📭 Nenhuma consulta neste dia",
                text_color="#94A3B8"
            ).pack(pady=50)
            return

        for i, c in enumerate(consultas):
            self.card(c, i)

    # ================= CARD =================
    def card(self, c, index=0):

        card = ctk.CTkFrame(
            self.lista,
            fg_color=self.card,
            corner_radius=20
        )
        card.pack(fill="x", pady=10)

        # barra lateral dinâmica
        bar = ctk.CTkFrame(
            card,
            width=6,
            fg_color=self.primary if index % 2 == 0 else self.accent,
            corner_radius=10
        )
        bar.pack(side="left", fill="y")

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=15)

        # HORA
        hora = ctk.CTkLabel(
            container,
            text=c["hora"],
            width=80,
            fg_color=self.soft,
            text_color=self.accent,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        hora.pack(side="left", padx=(0, 15))

        # INFO
        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(
            info,
            text=c["paciente"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.text_dark
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"CPF: {self.ocultar_cpf(c['cpf'])}",
            text_color="#64748B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Médico: {c['medico']}",
            text_color="#475569"
        ).pack(anchor="w")

        # STATUS
        ctk.CTkLabel(
            container,
            text=c["status"],
            text_color=self.primary,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="right")

        # EDITAR
        ctk.CTkButton(
            container,
            text="Editar",
            width=90,
            height=32,
            corner_radius=16,
            fg_color=self.primary,
            hover_color="#1B9BD1",
            command=lambda c=c: self.popup(c)
        ).pack(side="right", padx=10)

    # ================= POPUP =================
    def popup(self, consulta=None):
        popup = ctk.CTkToplevel(self)
        popup.geometry("420x520")
        popup.grab_set()
        popup.configure(fg_color=self.card)

        frame = ctk.CTkScrollableFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="📋 Consulta",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        paciente = ctk.CTkEntry(frame, placeholder_text="Paciente")
        paciente.pack(fill="x", pady=5)

        cpf = ctk.CTkEntry(frame, placeholder_text="CPF")
        cpf.pack(fill="x", pady=5)

        medico = ctk.CTkOptionMenu(frame, values=self.medicos)
        medico.pack(fill="x", pady=5)

        data = ctk.CTkEntry(frame, placeholder_text="Data")
        data.pack(fill="x", pady=5)

        hora = ctk.CTkEntry(frame, placeholder_text="Hora")
        hora.pack(fill="x", pady=5)

        status = ctk.CTkOptionMenu(
            frame,
            values=["Agendado", "Chegou", "Atendido"]
        )
        status.pack(fill="x", pady=5)

        anexos = consulta.get("anexos", []) if consulta else []

        box = ctk.CTkTextbox(frame, height=70)
        box.pack(fill="x", pady=10)

        def add():
            arq = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
            if arq:
                anexos.append(arq)
                box.insert("end", os.path.basename(arq) + "\n")

        for a in anexos:
            box.insert("end", os.path.basename(a) + "\n")

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(fill="x", pady=10)

        ctk.CTkButton(
            btns,
            text="+ Arquivo",
            command=add
        ).pack(side="left", expand=True, padx=5)

        def salvar():
            dados = {
                "paciente": paciente.get(),
                "cpf": cpf.get(),
                "medico": medico.get(),
                "data": data.get(),
                "hora": hora.get(),
                "status": status.get(),
                "anexos": anexos
            }

            if consulta:
                consulta.update(dados)
            else:
                self.consultas.append(dados)

            self.render()
            popup.destroy()

        ctk.CTkButton(
            btns,
            text="Salvar",
            fg_color=self.primary,
            command=salvar
        ).pack(side="right", expand=True, padx=5)

    # ================= ARQUIVO =================
    def abrir_arquivo(self, caminho):
        os.startfile(caminho)