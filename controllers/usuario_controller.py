from models.usuario_model import autenticar

def login(username, senha):
    return autenticar(username, senha)