from config.db import conectar

def inserir(data, tipo, id_paciente, id_medico):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO consulta (data, tipo_atendimento, id_paciente, id_medico)
        VALUES (%s, %s, %s, %s)
    """, (data, tipo, id_paciente, id_medico))

    conn.commit()
    cursor.close()
    conn.close()

def listar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id_consulta, p.nome, m.nome, c.data, c.tipo_atendimento
        FROM Consulta c
        JOIN Paciente p ON c.id_paciente = p.id_paciente
        JOIN Medico m ON c.id_medico = m.id_medico
    """)

    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados