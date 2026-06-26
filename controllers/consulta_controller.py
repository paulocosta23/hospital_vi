from models import consulta_model
from models.documento_consulta_model import DocumentoConsultaModel
from services.storage_service import StorageService
from datetime import datetime, timedelta
import time


class ConsultaContrroler():
    def __init__(self):
        self.storage = StorageService()
        self.documentos_model = DocumentoConsultaModel()

    def salvar(self,
            data_consulta,
            hora_consulta,
            status_consulta,
            tipo_atendimento,
            id_paciente,
            id_medico, arquivos_pdf):
        id_consulta = consulta_model.inserir(data_consulta,
            hora_consulta,
            status_consulta,
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
                    nome_original=arquivo['nome_original'],
                    caminho_storage=caminho_storage
                    
                )
            except Exception as e:
                erros_upload.append(arquivo['nome_original'])
                print(e)
        return {"sucesso": True,
                    "erros_upload": erros_upload}
    
    def lista_paciente(self):
        return consulta_model.lista_pacientes()
    
    def lista_medico(self):
        return consulta_model.lista_medicos()
                



    def listar(self):
        inicio = time.time()

        hoje = datetime.now().date()
        data_inicio = hoje - timedelta(days=5)
        data_fim = hoje + timedelta(days=5)

        consultas = consulta_model.listar(data_inicio=data_inicio,
                                          data_fim=data_fim)
        print("consulta_model:", time.time() - inicio)

        documentos = self.documentos_model.listar_todos()
    
        documentos_por_consulta = {}

        for documento in documentos:
            id_consulta = documento["id_consulta"]
            if id_consulta not in documentos_por_consulta:
                documentos_por_consulta[id_consulta] = []
            documentos_por_consulta[id_consulta].append(documento)
        for consulta in consultas:
            consulta["anexos"] = documentos_por_consulta.get(
                consulta["id_consulta"], []
            )
        return consultas

    def editar(self,
               id_consulta,
               data_consulta,
               hora_consulta,
               status_consulta,
               tipo_atendimento,
               id_medico,
               arquivos_pdf,
               anexos_antigos):
        
        consulta_model.editar(id_consulta=id_consulta,
                              data=data_consulta,
                              hora=hora_consulta,
                              status_consulta=status_consulta,
                              tipo_atendimento=tipo_atendimento,
                              id_medico=id_medico)
        
        nomes_novos = sorted(
            arquivo["nome_original"]
            for arquivo in arquivos_pdf
        )
        
        nomes_antigos = sorted(
            documento["nome_original"]
            for documento in anexos_antigos
        )

        documentos_removidos = [
            documento
            for documento in anexos_antigos
            if documento["nome_original"] not in nomes_novos
        ]

        documentos_novos = [
            arquivo
            for arquivo in arquivos_pdf
            if arquivo["nome_original"] not in nomes_antigos
        ]

        if nomes_novos != nomes_antigos:
            erros_upload = []

            for documento in documentos_removidos:
                try:
                    self.storage.excluir_pdf(
                        documento["caminho_storage"]
                    )
                    self.documentos_model.excluir_documento(documento["id_documento"])
                except Exception as e:
                    print(e)

            #self.documentos_model.excluir_por_consulta(id_consulta)

            for arquivo in documentos_novos:
                try:
                    caminho_storage = self.storage.upload_pdf(
                        id_consulta=id_consulta,
                        caminho_arquivo=arquivo['caminho']
                    )
                    self.documentos_model.inserir_documento(
                        id_consulta=id_consulta,
                        nome_original=arquivo['nome_original'],
                        caminho_storage=caminho_storage
                        
                    )
                except Exception as e:
                    erros_upload.append(arquivo['nome_original'])
                    print(e)
            return {"sucesso": True,
                        "erros_upload": erros_upload}
        
        return {"sucesso": True,
                        "erros_upload": []}

    def baixar_anexo(self, caminho_storage):
        return self.storage.baixar_pdf(caminho_storage)
    

