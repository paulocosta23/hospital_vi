from config.db import conectar

def listar_consultas_por_medico(data_inicio, data_fim, id_medico):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    
    sql ="""
        SELECT 
            c.id_consulta,
            p.nome as paciente,
            c.id_paciente,
            c.id_medico,
            p.cpf,
            m.nome as medico,
            DATE_FORMAT(c.data, '%%d/%%m/%%Y') as data,
            TIME_FORMAT(c.hora, '%%H:%%i') as hora,
            c.status_consulta as status,
            c.tipo_atendimento
        FROM (
            select id_consulta, id_paciente, id_medico, data, hora, status_consulta, tipo_atendimento 
            from Consulta 	
            where data between %s and %s and id_medico = %s
        ) as c
        JOIN Paciente p ON c.id_paciente = p.id_paciente
        JOIN Medico m ON c.id_medico = m.id_medico
    """
    values = data_inicio, data_fim, id_medico
    cursor.execute(sql, values)


    consultas_por_medico = cursor.fetchall()
    cursor.close()
    conn.close()
    return consultas_por_medico

def salvar_prontuario(queixa,
                      observacoes,
                      diagnostico,
                      medicacao,
                      exames,
                      id_consulta,
                      id_medico,
                      id_paciente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Prontuario (
                   sintomas,
                   observacoes, 
                   diagnostico,
                   receita,
                   exame, 
                   id_consulta, 
                   id_medico, 
                   id_paciente) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                   (queixa, observacoes, diagnostico, medicacao, exames, id_consulta, id_medico, id_paciente))
    conn.commit()

    cursor.close()
    conn.close()




def atualizar_status(id_consulta, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE Consulta SET status_consulta= %s WHERE id_consulta = %s", (status, id_consulta))
    
    conn.commit()
    cursor.close()
    conn.close()

def historico_por_paciente(id_paciente):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT
                   p.id_consulta,
                   DATE_FORMAT(c.data, '%%d/%%m/%%Y') as data,
                   m.nome as medico,
                   p.sintomas as queixa,
                   p.observacoes,
                   p.diagnostico,
                   p.receita,
                   p.exame as exames
                   FROM Prontuario p
                   JOIN Consulta c ON p.id_consulta = c.id_consulta
                   JOIN Medico m ON p.id_medico = m.id_medico
                   WHERE p.id_paciente = %s
                   ORDER BY c.data DESC""", (id_paciente,))
    historico_paciente = cursor.fetchall()

    cursor.close()
    conn.close()

    return historico_paciente
    
def historico_documentos(ids_consulta):
    placeholders = ", ".join(["%s"] * len(ids_consulta))
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query_documentos = f"""SELECT
                    id_documento,
                    id_consulta,
                    nome_original,
                    caminho_storage
                    FROM DocumentoConsulta
                   WHERE id_consulta IN ({placeholders})
                    """
    cursor.execute(query_documentos, ids_consulta)
    documentos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return documentos 
    
def atendimentos_salvos(id_consulta):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT 
                   sintomas as queixa,
                   observacoes, 
                   diagnostico,
                   receita,
                   exame as exames
                   FROM Prontuario
                   WHERE id_consulta = %s""", 
                   (id_consulta,))

    dados = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return dados

    
def listar_consultas_por_medico_data(nova_data, id_medico):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    
    sql ="""
        SELECT 
            c.id_consulta,
            p.nome as paciente,
            c.id_paciente,
            c.id_medico,
            p.cpf,
            m.nome as medico,
            DATE_FORMAT(c.data, '%%d/%%m/%%Y') as data,
            TIME_FORMAT(c.hora, '%%H:%%i') as hora,
            c.status_consulta as status,
            c.tipo_atendimento
        FROM (
            select id_consulta, id_paciente, id_medico, data, hora, status_consulta, tipo_atendimento 
            from Consulta 	
            where data = %s and id_medico = %s
        ) as c
        JOIN Paciente p ON c.id_paciente = p.id_paciente
        JOIN Medico m ON c.id_medico = m.id_medico
    """
    values = nova_data , id_medico
    cursor.execute(sql, values)


    consultas_por_medico = cursor.fetchall()
    cursor.close()
    conn.close()
    return consultas_por_medico