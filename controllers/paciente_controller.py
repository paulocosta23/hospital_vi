from models import paciente_model
from utils.validacoes import validar_cpf

def salvar(dados):
    if not validar_cpf(dados[3]):
        raise ValueError("CPF inválido")
    paciente_model.inserir(dados)

def listar():
    return paciente_model.listar()

def deletar(id):
    paciente_model.deletar(id)