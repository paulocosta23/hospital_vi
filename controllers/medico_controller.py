from models import medico_model

def salvar(dados):
    medico_model.inserir(dados)

def listar():
    return medico_model.listar()