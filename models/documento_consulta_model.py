from config.db import conectar
import time

class DocumentoConsultaModel():

    def inserir_documento(
            self,
            id_consulta,
            nome_original,
            caminho_storage
    ):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO DocumentoConsulta (
                       id_consulta,
                       nome_original,
                       caminho_storage)
                       VALUES (
                       %s,
                       %s,
                       %s)""", (
                           id_consulta,
                           nome_original,
                           caminho_storage))
        conn.commit()
        cursor.close()
        conn.close()

    def listar_todos(self):
        inicio = time.time()
        conn = conectar()
        print("conectar:", time.time() - inicio)
        inicio = time.time()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT
        
                       id_documento,
                       id_consulta,
                       nome_original,
                       caminho_storage
                       FROM DocumentoConsulta
                    """)
        documentos = cursor.fetchall()
        print("select:", time.time() - inicio)
        cursor.close()
        conn.close()
        return documentos 
          
    def excluir_documento(self, id_documento):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
                       DELETE FROM DocumentoConsulta
                       WHERE id_documento = %s""", (id_documento,))
        conn.commit()
        
        cursor.close()
        conn.close()
