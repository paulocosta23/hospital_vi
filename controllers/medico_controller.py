from models import medico_model

def salvar(_dados):
    medico_model.inserir(_dados)

def listar():
    return medico_model.listar()

def atualizar():
    pass

def remover():
    pass

def lista_consultorios():
    return medico_model.lista_consultorios()