from models import atendimento_model
from models.documento_consulta_model import DocumentoConsultaModel
from services.storage_service import StorageService
from datetime import datetime, timedelta

class AtendimentosContrroler():
    def __init__(self):
        self.storage = StorageService()
        self.documentos_model = DocumentoConsultaModel()

    def listar_consultas_por_medico(self, id_medico):

        hoje = datetime.now().date()
        data_inicio = hoje - timedelta(days=5)
        data_fim = hoje + timedelta(days=5)

        consulta_por_medico = atendimento_model.listar_consultas_por_medico(data_inicio=data_inicio,
                                          data_fim=data_fim,
                                          id_medico=id_medico)

        documentos = self.documentos_model.listar_todos()
    
        documentos_por_consulta = {}

        for documento in documentos:
            id_consulta = documento["id_consulta"]
            if id_consulta not in documentos_por_consulta:
                documentos_por_consulta[id_consulta] = []
            documentos_por_consulta[id_consulta].append(documento)
        for consulta in consulta_por_medico:
            consulta["anexos"] = documentos_por_consulta.get(
                consulta["id_consulta"], []
            )
        return consulta_por_medico
    
    def salvar_prontuario(self,
                          queixa,
                          observacoes,
                          diagnostico,
                          medicacao,
                          exames,
                          id_consulta,
                          id_medico,
                          id_paciente):
        return atendimento_model.salvar_prontuario(queixa,
                                                    observacoes,
                                                    diagnostico,
                                                    medicacao,
                                                    exames,
                                                    id_consulta,
                                                    id_medico,
                                                    id_paciente)
    
   
    def historico_por_paciente(self,
                               id_paciente):
        consultas = atendimento_model.historico_por_paciente(id_paciente)

        if not consultas:
            return consultas

        ids_consulta = [c["id_consulta"] for c in consultas]

        documentos = atendimento_model.historico_documentos(ids_consulta)

        for consulta in consultas:
            consulta["anexos"] = []

        for doc in documentos:
            for consulta in consultas:
                if consulta["id_consulta"] == doc["id_consulta"]:
                    consulta["anexos"].append(doc)
                    break

        return consultas

    def atualizar_status(self,id_consulta, status):
        atendimento_model.atualizar_status(id_consulta, status)
        

    def baixar_anexo(self, caminho_storage):
        return self.storage.baixar_pdf(caminho_storage)
    
    def excluir_anexo(self, id_documento, caminho_storage):
        self.storage.excluir_pdf(caminho_storage)
        self.documentos_model.excluir_documento(id_documento)

    def atendimentos_salvos(self, id_consulta):
        return atendimento_model.atendimentos_salvos(id_consulta=id_consulta)
    
    def listar_consultas_por_medico_data(self, nova_data, id_medico):

        consulta_por_medico = atendimento_model.listar_consultas_por_medico_data(nova_data=nova_data, id_medico=id_medico)

        documentos = self.documentos_model.listar_todos()
    
        documentos_por_consulta = {}

        for documento in documentos:
            id_consulta = documento["id_consulta"]
            if id_consulta not in documentos_por_consulta:
                documentos_por_consulta[id_consulta] = []
            documentos_por_consulta[id_consulta].append(documento)
        for consulta in consulta_por_medico:
            consulta["anexos"] = documentos_por_consulta.get(
                consulta["id_consulta"], []
            )
        return consulta_por_medico