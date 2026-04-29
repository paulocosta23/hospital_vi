import tkinter as tk
from tkinter import ttk
from controllers.medico_controller import salvar as salvar_medico, listar as listar_medico

class MedicoView:
    def __init__(self, root):
        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True)

        self.nome = tk.Entry(frame)
        self.nome.pack()

        self.crm = tk.Entry(frame)
        self.crm.pack()

        tk.Button(frame, text="Salvar", command=self.salvar).pack()

        self.tree = ttk.Treeview(frame, columns=("ID","Nome","CRM"), show="headings")
        for col in ("ID","Nome","CRM"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.listar()

    def salvar(self):
        salvar((self.nome.get(),"Geral",self.crm.get(),1))
        self.listar()

    def listar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for m in listar():
            self.tree.insert("", "end", values=(m[0], m[1], m[3]))