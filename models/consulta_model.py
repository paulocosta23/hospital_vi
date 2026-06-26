from config.db import conectar

def inserir(data, hora, status_consulta, tipo, id_paciente, id_medico):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Consulta (data, hora, status_consulta, tipo_atendimento, id_paciente, id_medico)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data, hora, status_consulta, tipo, id_paciente, id_medico))

    id_consulta = cursor.lastrowid

    conn.commit()
    cursor.close()
    conn.close()
    return id_consulta

def listar(data_inicio, data_fim):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    
    sql ="""
        SELECT 
            c.id_consulta,
            p.nome as paciente,
            p.cpf,
            m.nome as medico,
            DATE_FORMAT(c.data, '%%d/%%m/%%Y') as data,
            TIME_FORMAT(c.hora, '%%H:%%i') as hora,
            c.status_consulta as status,
            c.tipo_atendimento
        FROM (
            select id_consulta, id_paciente, id_medico, data, hora, status_consulta, tipo_atendimento 
            from Consulta 	
            where data between %s and %s
        ) as c
        JOIN Paciente p ON c.id_paciente = p.id_paciente
        JOIN Medico m ON c.id_medico = m.id_medico
    """
    values = data_inicio, data_fim
    cursor.execute(sql, values)


    consultas = cursor.fetchall()
    cursor.close()
    conn.close()
    return consultas

def editar(id_consulta, data, hora, status_consulta, tipo_atendimento, id_medico):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""UPDATE Consulta
                   SET data=%s,
                   hora=%s,
                   status_consulta=%s,
                   tipo_atendimento=%s,
                   id_medico=%s
                   WHERE id_consulta=%s""",
                   (data, hora, status_consulta, tipo_atendimento, id_medico, id_consulta))
    conn.commit()
    cursor.close()
    conn.close()

def lista_pacientes():
    conn = conectar()
    cursor = conn.cursor(dictionary= True)
    
    cursor.execute("SELECT id_paciente, nome, cpf, id_plano FROM Paciente")
   
    dados_paciente = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados_paciente

def lista_medicos():
    conn = conectar()
    cursor = conn.cursor(dictionary= True)
    
    cursor.execute("SELECT id_medico, nome FROM Medico")
   
    dados_medico = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados_medico

def listar_por_data(data):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    
    sql ="""
        SELECT 
            c.id_consulta,
            p.nome as paciente,
            p.cpf,
            m.nome as medico,
            DATE_FORMAT(c.data, '%%d/%%m/%%Y') as data,
            TIME_FORMAT(c.hora, '%%H:%%i') as hora,
            c.status_consulta as status,
            c.tipo_atendimento
        FROM (
            select id_consulta, id_paciente, id_medico, data, hora, status_consulta, tipo_atendimento 
            from Consulta 	
            where data = %s
        ) as c
        JOIN Paciente p ON c.id_paciente = p.id_paciente
        JOIN Medico m ON c.id_medico = m.id_medico
    """
    values = data
    cursor.execute(sql, values)


    consultas = cursor.fetchall()
    cursor.close()
    conn.close()
    return consultas