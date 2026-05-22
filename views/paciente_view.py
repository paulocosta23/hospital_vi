from logging import root
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.paciente_controller import (
    salvar as salvar_paciente,
    listar as listar_paciente,
    deletar as deletar_paciente
)
# from views.login_view import LoginView


class PacienteView:
    def __init__(self, root):
        self.root = root

        # FRAME PRINCIPAL
        self.frame = tk.Frame(root, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        # TOPO
        top_frame = tk.Frame(self.frame, bg="#2f3640", height=50)
        top_frame.pack(fill="x")

        tk.Label(
            top_frame,
            text="Gestão de Pacientes",
            bg="#2f3640",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=10)

        tk.Button(
            top_frame,
            text="Sair",
            command=self.sair,
            bg="#e84118",
            fg="white",
        ).pack(side="right", padx=10, pady=10)

        # CONTAINER
        container = tk.Frame(self.frame, bg="#f5f6fa")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # FORMULÁRIO
        form_frame = tk.LabelFrame(container, text="Cadastro", bg="#f5f6fa")
        form_frame.pack(side="left", fill="y", padx=10)

        tk.Label(form_frame, text="Nome", bg="#f5f6fa").pack(anchor="w")
        self.nome = tk.Entry(form_frame, width=30)
        self.nome.pack(pady=5)

        tk.Label(form_frame, text="CPF", bg="#f5f6fa").pack(anchor="w")
        self.cpf = tk.Entry(form_frame, width=30)
        self.cpf.pack(pady=5)

        tk.Button(
            form_frame,
            text="Salvar",
            command=self.salvar,
            bg="#44bd32",
            fg="white",
            width=20
        ).pack(pady=5)

        tk.Button(
            form_frame,
            text="Excluir",
            command=self.excluir,
            bg="#c23616",
            fg="white",
            width=20
        ).pack(pady=5)

        # TABELA
        table_frame = tk.Frame(container)
        table_frame.pack(side="right", fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Nome", "CPF"),
            show="headings"
        )

        for col in ("ID", "Nome", "CPF"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.listar()

    # -----------------------
    # FUNÇÕES
    # ----------------------


    def limpar_campos(self):
        self.nome.delete(0, tk.END)
        self.cpf.delete(0, tk.END)

    def salvar(self):

        dados = (self.nome.get(), None, None, self.cpf.get(), None, None)

        if not dados[0] or not dados[3]:
            messagebox.showerror("ERRO", "Preencha todos os campos corretamente.")
            return

        resultado = salvar_paciente(dados)
       
        if resultado == "CPF já cadastrado":
            messagebox.showerror("erro", resultado)
            return
        elif resultado == "CPF inválido":
            messagebox.showerror("ERRO", "CPF inválido, revise os dados e tente novamente.")
            return
        elif resultado == "Paciente salvo com sucesso.":
            messagebox.showinfo("Sucesso", resultado)

        salvar_paciente(dados)
        self.limpar_campos()
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

        confirmar = messagebox.askyesno(
            "Confirmação",
            "Deseja excluir o paciente?"
        )

        if confirmar:
            deletar_paciente(id_paciente)
            self.listar()

    def sair(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        

        from views.login_view import LoginView
        LoginView(self.root) 

        



        
