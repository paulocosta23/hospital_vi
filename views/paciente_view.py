import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controllers.paciente_controller import salvar as salvar_paciente, listar as listar_paciente

class PacienteView:
    def __init__(self, root):
       
        main = tk.Frame(root, bg=C["bg_panel"])
        main.pack(fill="both", expand=True, padx=16, pady=16)
        
        self.nome = tk.Entry(main)
        self.nome.pack()

        self.cpf = tk.Entry(main)
        self.cpf.pack()

        tk.Button(main, text="Salvar", command=self.salvar).pack()
        tk.Button(main, text="Excluir", command=self.excluir).pack()

        self.tree = ttk.Treeview(main, columns=("ID","Nome","CPF"), show="headings")
        for col in ("ID","Nome","CPF"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.listar()

    def salvar(self):
        dados = (self.nome.get(), None, None, self.cpf.get(), None, None)
        salvar_paciente(dados)
        self.listar()

    def listar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in listar_paciente():
            self.tree.insert("", "end", values=(p[0], p[1], p[4]))
   
    def excluir(self):
        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um paciente")
            return

        item = self.tree.item(selecionado)
        id_paciente = item["values"][0]

        confirmar = messagebox.askyesno("Confirmação", "Deseja excluir o paciente?")

        if confirmar:
            from controllers.paciente_controller import deletar
            deletar(id_paciente)
            self.listar() 