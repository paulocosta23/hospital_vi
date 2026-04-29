from config.db import conectar

def listar():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Procedimento")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados