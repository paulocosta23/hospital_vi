from config.db import conectar

def cpf_existe(cpf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Paciente where cpf = %s", (cpf,))
    resultado = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    return resultado > 0


def inserir(_dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO  Paciente (nome, data_nascimento, endereco, cpf, telefone, numero_cartao)
        VALUES(%s, %s, %s, %s, %s, %s )
        """, _dados)
    conn.commit()
    cursor.close()
    conn.close()

def listar():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT
                   nome,
                   DATE_FORMAT(data_nascimento, '%%d/%%m/%%Y') as nascimento,
                   endereco,
                   cpf,
                   telefone,
                   numero_cartao as carteirinha
                   FROM Paciente""")
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