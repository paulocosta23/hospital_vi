import tkinter as tk
from tkinter import ttk
from controllers.consulta_controller import salvar as salvar_consulta, listar as listar_consulta
from views.cores import C
from datetime import datetime


class ConsultaView:
    def __init__(self, root):

        main = tk.Frame(root, bg=C["bg_panel"])
        main.pack(fill="both", expand=True, padx=16, pady=16)

        # ===== TÍTULO =====
        tk.Label(
            main,
            text="Consultas",
            bg=C["bg_panel"],
            fg=C["text_hi"],
            font=("Segoe UI", 18, "bold")
        ).pack(fill="x", pady=(0, 16))

        # ===== ÁREA CENTRAL =====
        body = tk.Frame(main, bg=C["bg_panel"])
        body.pack(fill="both", expand=True)

        # ===== LADO ESQUERDO (FORMULÁRIO) =====
        form_card = tk.Frame(
            body,
            bg=C["bg_card"],
            highlightbackground=C["border"],
            highlightthickness=1
        )
        form_card.pack(side="left", fill="y", padx=(0, 12), pady=4)

        form = tk.Frame(form_card, bg=C["bg_card"])
        form.pack(fill="both", expand=True, padx=16, pady=16)

        def campo(label):
            box = tk.Frame(form, bg=C["bg_card"])
            box.pack(fill="x", pady=8)

            tk.Label(
                box,
                text=label,
                bg=C["bg_card"],
                fg=C["text_mid"],
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w")

            entry = tk.Entry(
                box,
                bg=C["bg_panel"],
                fg=C["text_hi"],
                insertbackground=C["text_hi"],
                relief="flat"
            )
            entry.pack(fill="x", ipady=8)
            return entry

        # ===== CAMPOS =====
        self.data     = campo("Data")
        self.tipo     = campo("Tipo")
        self.paciente = campo("Paciente")
        self.medico   = campo("Médico")

        # ===== BOTÃO SALVAR (EMBAIXO) =====
        tk.Button(
            form,
            text="Salvar",
            command=self.salvar,
            bg=C["accent"],
            fg="black",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=32,
            pady=10,
            cursor="hand2"
        ).pack(side="bottom", pady=(24, 0))

        # ===== LADO DIREITO (TABELA) =====
        table_card = tk.Frame(
            body,
            bg=C["bg_card"],
            highlightbackground=C["border"],
            highlightthickness=1
        )
        table_card.pack(side="right", fill="both", expand=True, padx=(12, 0), pady=4)

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background=C["bg_panel"],
            fieldbackground=C["bg_panel"],
            foreground=C["text_hi"],
            rowheight=32,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=C["bg_card"],
            foreground=C["text_mid"],
            font=("Segoe UI", 10, "bold")
        )

        self.tree = ttk.Treeview(
            table_card,
            columns=("ID", "Paciente", "Médico", "Data", "Tipo"),
            show="headings"
        )

        for col in ("ID", "Paciente", "Médico", "Data", "Tipo"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=12, pady=12)

        self.listar()

    # ===== LÓGICA (SEM ALTERAR) =====
    def salvar(self):
        data = self.data.get()
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        salvar_consulta(
            data_formatada,
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