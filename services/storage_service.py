import os 
import uuid
import time
import tempfile

from services.supabase_client import supabase
from config.settings import SUPABASE_BUCKET

class StorageService ():
    def __init__(self):
        self.bucket = SUPABASE_BUCKET

    def baixar_pdf(self, caminho_storage):
        try:
            resposta = supabase.storage.from_(self.bucket).download(caminho_storage)

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as arquivo:
                arquivo.write(resposta)
                return arquivo.name
        except Exception as e:
            raise Exception (f"Erro ao baixar o documento: {e}")
    
    def upload_pdf(self, id_consulta, caminho_arquivo):
        inicio = time.time()
        extensao = os.path.splitext(caminho_arquivo)[1]

        nome_storage = f"{uuid.uuid4()}{extensao}"

        caminho_storage = (f"consultas/{id_consulta}/{nome_storage}")

        with open(caminho_arquivo, "rb") as arquivo:
            
            supabase.storage.from_(self.bucket).upload(
                path=caminho_storage,
                file=arquivo,
                file_options={
                    "content-type": "application/pdf"
                }
            )
        print("upload:", time.time() - inicio)
        return caminho_storage
    def excluir_pdf(self, caminho_storage):
        resposta = supabase.storage.from_(self.bucket).remove([caminho_storage])
        print(resposta)