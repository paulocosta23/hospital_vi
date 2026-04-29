from config.db import conectar

def inserir(data_entrada, data_saida, id_paciente, id_ala):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Internacao (data_entrada, data_saida, id_paciente, id_ala)
        VALUES (%s, %s, %s, %s)
    """, (data_entrada, data_saida, id_paciente, id_ala))

    conn.commit()
    cursor.close()
    conn.close()