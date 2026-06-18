from models import usuario_model

def login(username, senha):
    return usuario_model.autenticar(username, senha)

def adicionar(_dados):
    usuario_model.inserir(_dados)

def remover(id_usuario):
    usuario_model.remover(id_usuario)

def listar():
    return usuario_model.listar()

def editar(id_usuario, _dados):
    usuario_model.editar(id_usuario, _dados)