import tkinter as tk
from tkinter import ttk
from controllers.consulta_controller import salvar as salvar_consulta, listar as listar_consulta


class ConsultaView:
    def __init__(self, root):
        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True)

        self.data = tk.Entry(frame)
        self.data.pack()

        self.tipo = tk.Entry(frame)
        self.tipo.pack()

        self.paciente = tk.Entry(frame)
        self.paciente.pack()

        self.medico = tk.Entry(frame)
        self.medico.pack()

        tk.Button(frame, text="Salvar", command=self.salvar).pack()

        self.tree = ttk.Treeview(
            frame,
            columns=("ID", "Paciente", "Médico", "Data", "Tipo"),
            show="headings"
        )

        for col in ("ID", "Paciente", "Médico", "Data", "Tipo"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

        self.listar()

    def salvar(self):
        salvar_consulta(
            self.data.get(),
            self.tipo.get(),
            self.paciente.get(),
            self.medico.get()
        )
        self.listar()

    def listar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for c in listar_consulta():
            self.tree.insert("", "end", values=c)