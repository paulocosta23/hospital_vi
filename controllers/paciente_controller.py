from models import paciente_model
from utils.validacoes import validar_cpf

def salvar(dados):
    if paciente_model.cpf_existe(cpf=dados[3]):
        return "CPF já cadastrado"
    
    if not validar_cpf(dados[3]):
        return "CPF inválido"
    
    paciente_model.inserir(dados)
    return "Paciente salvo com sucesso."

def listar():
    return paciente_model.listar()

def deletar(id):
    paciente_model.deletar(id)