from config.db import conectar

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

    def listar_por_consulta(self, id_consulta):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT
        
                       id_documento,
                       nome_original,
                       caminho_storage
                       FROM DocumentoConsulta
                       WHERE id_consulta = %s""", (id_consulta,))
        documentos = cursor.fetchall()

        cursor.close()
        conn.close()
        return documentos 
          

