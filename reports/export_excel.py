import pandas as pd
from models.consulta_model import listar

def exportar_consultas():
    dados = listar()

    df = pd.DataFrame(dados, columns=[
        "ID", "Paciente", "Médico", "Data", "Tipo"
    ])

    df.to_excel("consultas.xlsx", index=False)