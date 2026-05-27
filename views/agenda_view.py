import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import filedialog
import os


class AgendaView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color=("white", "#1F2937")
)

        self.data_atual = datetime.now()

        self.medicos = ["Dr. Carlos", "Dr. Ana"]
        self.consultas = []

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(
            header,
            text="Agenda",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")

        data_frame = ctk.CTkFrame(header, fg_color="transparent")
        data_frame.pack(side="right")

        ctk.CTkButton(data_frame, text="<", width=35, command=self.voltar).pack(side="left")

        self.label_data = ctk.CTkLabel(data_frame, text="")
        self.label_data.pack(side="left", padx=10)

        ctk.CTkButton(data_frame, text=">", width=35, command=self.avancar).pack(side="left")

        ctk.CTkButton(
            data_frame,
            text="Hoje",
            width=60,
            fg_color="#E5E7EB",
            text_color="#111827",
            command=self.ir_hoje
        ).pack(side="left", padx=5)

        self.input_data = ctk.CTkEntry(data_frame, width=110, placeholder_text="dd/mm/aaaa")
        self.input_data.pack(side="left", padx=5)

        ctk.CTkButton(data_frame, text="Ir", width=40, command=self.ir_data).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Nova consulta",
            fg_color="#2563EB",
            hover_color="#1E40AF",
            command=lambda: self.popup()
        ).pack(side="right", padx=10)

        self.lista = ctk.CTkScrollableFrame(self)
        self.lista.pack(fill="both", expand=True, padx=30, pady=10)

        self.update_data()
        self.render()

    def update_data(self):
        self.label_data.configure(text=self.data_atual.strftime("%d/%m/%Y"))

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
            self.data_atual = datetime.strptime(self.input_data.get(), "%d/%m/%Y")
            self.update_data()
            self.render()
        except:
            print("Data inválida")

    def formatar_cpf(self, texto):
        nums = ''.join(filter(str.isdigit, texto))[:11]
        if len(nums) <= 3:
            return nums
        elif len(nums) <= 6:
            return f"{nums[:3]}.{nums[3:]}"
        elif len(nums) <= 9:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:]}"
        else:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"

    def ocultar_cpf(self, cpf):
        nums = ''.join(filter(str.isdigit, cpf))
        if len(nums) < 11:
            return cpf
        return f"{nums[:3]}.***.***-{nums[-2:]}"

    def render(self):
        for w in self.lista.winfo_children():
            w.destroy()

        data = self.data_atual.strftime("%d/%m/%Y")
        consultas = [c for c in self.consultas if c["data"] == data]

        if not consultas:
            ctk.CTkLabel(self.lista, text="Nenhuma consulta neste dia", text_color="#6B7280").pack(pady=40)
            return

        for c in consultas:
            self.card(c)

    def card(self, c):
        card = ctk.CTkFrame(self.lista, fg_color="white", corner_radius=14)
        card.pack(fill="x", pady=10)

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=15)

        hora_box = ctk.CTkFrame(container, fg_color="#EEF2FF", corner_radius=10, width=80, height=50)
        hora_box.pack(side="left", padx=(0, 15))
        hora_box.pack_propagate(False)

        ctk.CTkLabel(hora_box, text=c["hora"],
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#2563EB").pack(expand=True)

        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(info, text=c["paciente"],
                     font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w")

        ctk.CTkLabel(info,
                     text=f"CPF: {self.ocultar_cpf(c['cpf'])}",
                     text_color="#6B7280").pack(anchor="w")

        ctk.CTkLabel(info,
                     text=f"Médico: {c['medico']}",
                     text_color="#374151").pack(anchor="w")

        actions = ctk.CTkFrame(container, fg_color="transparent")
        actions.pack(side="right")

        ctk.CTkLabel(actions, text=c["status"]).pack()

        ctk.CTkButton(actions, text="Editar", width=90,
                      command=lambda c=c: self.popup(c)).pack(pady=4)

    def popup(self, consulta=None):
        popup = ctk.CTkToplevel(self)
        popup.geometry("420x500")
        popup.grab_set()

        frame = ctk.CTkFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Consulta",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        paciente = ctk.CTkEntry(frame, placeholder_text="Paciente")
        paciente.pack(fill="x", pady=5)

        cpf = ctk.CTkEntry(frame, placeholder_text="CPF")
        cpf.pack(fill="x", pady=5)

        def mascara(event):
            valor = self.formatar_cpf(cpf.get())
            cpf.delete(0, "end")
            cpf.insert(0, valor)

        cpf.bind("<KeyRelease>", mascara)

        medico = ctk.CTkOptionMenu(frame, values=self.medicos)
        medico.pack(fill="x", pady=5)

        data = ctk.CTkEntry(frame, placeholder_text="Data")
        data.pack(fill="x", pady=5)

        hora = ctk.CTkEntry(frame, placeholder_text="Hora")
        hora.pack(fill="x", pady=5)

        status = ctk.CTkOptionMenu(frame, values=["Agendado", "Chegou", "Atendido"])
        status.pack(fill="x", pady=5)

        ctk.CTkLabel(frame,
                     text="Anexos da consulta",
                     text_color="#6B7280",
                     font=ctk.CTkFont(size=12, weight="bold")
                     ).pack(anchor="w", pady=(10, 0))

        anexos = consulta.get("anexos", []) if consulta else []

        def add_anexo():
            arq = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
            if arq:
                anexos.append(arq)
                box.insert("end", os.path.basename(arq) + "\n")

        box = ctk.CTkTextbox(frame, height=70)
        box.pack(fill="x", pady=5)

        for a in anexos:
            box.insert("end", os.path.basename(a) + "\n")

        # ✅ BOTÕES LADO A LADO (ÚNICA MUDANÇA REAL)
        botoes = ctk.CTkFrame(frame, fg_color="transparent")
        botoes.pack(fill="x", pady=10)

        ctk.CTkButton(botoes, text="+ Adicionar arquivo",
                      command=add_anexo).pack(side="left", expand=True, padx=5)

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

        ctk.CTkButton(botoes, text="Salvar",
                      command=salvar).pack(side="right", expand=True, padx=5)

    def abrir_arquivo(self, caminho):
        os.startfile(caminho)
