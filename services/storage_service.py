import os 
import uuid

from services.supabase_client import supabase
from config.settings import SUPABASE_BUCKET

class StorageService ():
    def __init__(self):
        self.bucket = SUPABASE_BUCKET
    
    def upload_pdf(self, id_consulta, caminho_arquivo):
        
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
        return caminho_storage