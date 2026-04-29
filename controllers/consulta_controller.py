from models import consulta_model

def salvar(data, tipo, paciente, medico):
    consulta_model.inserir(data, tipo, paciente, medico)

def listar():
    return consulta_model.listar()
