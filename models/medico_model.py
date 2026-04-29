from config.db import conectar

def inserir(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO  medico (nome, especialidade, crm, id_consultorio)
        VALUES(%s, %s, %s, %s )  
        """, dados)
    conn.commit()
    cursor.close()
    conn.close()

def listar():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Medico")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados