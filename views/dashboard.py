from tkinter import ttk
from views.paciente_view import PacienteView
from views.medico_view import MedicoView
from views.consulta_view import ConsultaView
from views.adicionar_consultorio_view import AdicionarConsultórioView

class Dashboard:
    def __init__(self, root, tipo_usuario):

        print("TIPO USUARIO:", tipo_usuario)  # DEBUG

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        # ATENDENTE
        if tipo_usuario == "atendente":
            aba1 = ttk.Frame(notebook)
            aba2 = ttk.Frame(notebook)

            notebook.add(aba1, text="Pacientes")
            notebook.add(aba2, text="Consultas")

            PacienteView(aba1)
            ConsultaView(aba2)

        # MÉDICO
        elif tipo_usuario == "medico":
            aba1 = ttk.Frame(notebook)

            notebook.add(aba1, text="Consultas do Dia")

            ConsultaView(aba1)

        # ADMIN
        elif tipo_usuario == "admin":
            aba1 = ttk.Frame(notebook)
            aba2 = ttk.Frame(notebook)
            aba3 = ttk.Frame(notebook)
            aba4 = ttk.Frame(notebook)

            notebook.add(aba1, text="Pacientes")
            notebook.add(aba2, text="Médicos")
            notebook.add(aba3, text="Consultas")
            notebook.add(aba4, text="Adicionar Consultório")

            PacienteView(aba1)
            MedicoView(aba2)
            ConsultaView(aba3)
            AdicionarConsultórioView(aba4)

        else:
            raise ValueError(f"Tipo de usuário inválido: {tipo_usuario}")