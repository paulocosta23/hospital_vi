import tkinter as tk
from tkinter import ttk
from controllers.medico_controller import salvar as salvar_medico, listar as listar_medico
from tkinter import messagebox

class MedicoView:
    def __init__(self, root):
        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True)

        self.text_nome = tk.Label(frame, text="Nome do Médico")
        self.text_nome.pack()
        self.nome = tk.Entry(frame)
        self.nome.pack()

        self.text_especialidade = tk.Label(frame, text="Especialidade")
        self.text_especialidade.pack()
        self.especialidade = tk.Entry(frame)
        self.especialidade.pack()

        self.text_crm = tk.Label(frame, text="CRM")
        self.text_crm.pack()
        self.crm = tk.Entry(frame)
        self.crm.pack()

        self.text_id_consultorio = tk.Label(frame, text="ID do Consultório")
        self.text_id_consultorio.pack()
        self.id_consultorio = tk.Entry(frame)
        self.id_consultorio.pack()

        
        
      
        tk.Button(frame, text="Salvar", command=self.salvar).pack()

        self.tree = ttk.Treeview(frame, columns=("ID","Nome", "Especialidade","CRM","ID Consultorio"), show="headings")
        for col in ("ID","Nome","Especialidade","CRM","ID Consultorio"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.listar()

    def limpar_campos(self):
        self.nome.delete(0, tk.END),
        self.especialidade.delete(0, tk.END),
        self.crm.delete(0, tk.END),
        self.id_consultorio.delete(0, tk.END)
        

    def salvar(self):
       
        try:
            salvar_medico((self.nome.get(), self.especialidade.get(), self.crm.get(), self.id_consultorio.get()))
        except Exception as e:
            messagebox.showerror("Erro", "Erro ao salvar médico, verifique os dados e tente novamente.")
            return
       
        #salvar_medico((self.nome.get(), self.especialidade.get(), self.crm.get(), self.id_consultorio.get()))
        self.listar()
        self.limpar_campos()

    def listar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for m in listar_medico():
            self.tree.insert("", "end", values=(m[0], m[1], m[2], m[3], m[4]))
