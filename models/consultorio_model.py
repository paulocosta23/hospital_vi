from config.db import conectar

def inserir(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO CONSULTORIO (numero, andar, bloco) VALUES (%s, %s, %s)
                   """, dados)
    conn.commit()
    cursor.close()
    conn.close()

def listar():
    conn = conectar()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM consultorio")

    dados = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return dados
def remover(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM consultorio WHERE id_consultorio = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    