from models import paciente_model
#from utils.validacoes import validar_cpf

def salvar(_dados):
    #if paciente_model.cpf_existe(cpf=dados[3]):
        #return "CPF já cadastrado"
    
    #if not validar_cpf(dados[3]):
        #return "CPF inválido"
    
    paciente_model.inserir(_dados)
    return "Paciente salvo com sucesso."

def listar():
    return paciente_model.listar()

def editar(id_paciente, _dados):
    paciente_model.editar(id_paciente, _dados)

def deletar(id_paciente):
    paciente_model.deletar(id_paciente)