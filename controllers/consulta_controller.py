from models import consulta_model
from models.documento_consulta_model import DocumentoConsultaModel
from services.storage_service import StorageService


class ConsultaContrroler():
    def __init__(self):
        self.storage = StorageService()
        self.documentos_model = DocumentoConsultaModel()

    def salvar(self,
            data_consulta,
            hora_consulta,
            tipo_atendimento,
            id_paciente,
            id_medico, arquivos_pdf):
        id_consulta = consulta_model.inserir(data_consulta,
            hora_consulta,
            tipo_atendimento,
            id_paciente,
            id_medico)
        erros_upload = []

        for arquivo in arquivos_pdf:
            try:
                caminho_storage = self.storage.upload_pdf(
                    id_consulta=id_consulta,
                    caminho_arquivo=arquivo['caminho']
                )
                self.documentos_model.inserir_documento(
                    id_consulta=id_consulta,
                    nome_original=arquivo['nome'],
                    caminho_storage=caminho_storage
                    
                )
            except Exception as e:
                erros_upload.append(arquivo['nome'])
                print(e)
        return {"sucesso": True,
                    "erros_upload": erros_upload}
    
    def lista_paciente(self):
        return consulta_model.lista_pacientes()
    
    def lista_medico(self):
        return consulta_model.lista_medicos()
                



    def listar(self):
        
        consultas = consulta_model.listar()

        for consulta in consultas:
            consulta["anexos"] = self.documentos_model.listar_por_consulta(
                consulta["id_consulta"]
            )
        return consultas
