from models import medico_model

def salvar(_dados):
    medico_model.inserir(_dados)

def listar():
    return medico_model.listar()

def atualizar(_dados, id_medico):
    medico_model.atualizar(_dados,id_medico)

def remover(id_medico):
    medico_model.remover(id_medico)

def lista_consultorios():
    return medico_model.lista_consultorios()

def vincular_medico_usuario(id_medico, id_usuario):
    medico_model.vincular_medico_usuario(id_medico=id_medico, id_usuario=id_usuario)

def buscar_por_usuario(id_usuario):
    return medico_model.buscar_por_usuario(id_usuario)