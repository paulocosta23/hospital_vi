from models import consultorio_model

def salvar(dados):
    consultorio_model.inserir(dados)
    
def listar():
    return consultorio_model.listar()

def remover(id):
    consultorio_model.remover(id)