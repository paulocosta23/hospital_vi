from models import plano_model

def adicionar(_dados):
    plano_model.inserir(_dados)

def listar():
    return plano_model.listar()

def remover(id_plano):
    plano_model.remover(id_plano)

def editar(id_plano, _dados):
    plano_model.editar(id_plano, _dados)