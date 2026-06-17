from models import consultorio_model

def salvar(_dados):
    consultorio_model.inserir(_dados)
    
def listar():
    return consultorio_model.listar()

def remover(id_consultorio):
    consultorio_model.remover(id_consultorio)

def atualizar(id_consultorio, _dados):
    consultorio_model.editar(id_consultorio, _dados)