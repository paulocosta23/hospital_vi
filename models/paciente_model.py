from config.db import conectar

def inserir(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO  paciente (nome, data_nascimento, endereco, cpf, telefone, id_plano)
        VALUES(%s, %s, %s, %s, %s, %s )  
        """, dados)
    conn.commit()
    cursor.close()
    conn.close()

def listar():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Paciente")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

def deletar(id_paciente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Paciente WHERE id_paciente=%s", (id_paciente))
    conn.commit()
    cursor.close()
    conn.close()

def deletar(id_paciente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Paciente WHERE id_paciente = %s", (id_paciente,))

    conn.commit()
    cursor.close()
    conn.close()