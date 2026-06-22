from services.storage_service import StorageService

storage = StorageService()
caminho = storage.upload_pdf(id_consulta=1,caminho_arquivo=r"C:\Users\Almeida\Desktop\LP_Venda_1021_01-06-2026.pdf")

print(caminho)