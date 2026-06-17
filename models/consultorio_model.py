from config.db import conectar

def inserir(_dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO Consultorio (numero, andar, bloco) VALUES (%s, %s, %s)
                   """, _dados)
    conn.commit()
    cursor.close()
    conn.close()

def listar():
    conn = conectar()
    cursor =conn.cursor(dictionary=True)
    cursor.execute("""SELECT
                    id_consultorio,
                    numero,
                    andar,
                    bloco as status
                    FROM Consultorio""")

    dados = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return dados

def remover(id_consultorio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Consultorio WHERE id_consultorio = %s", (id_consultorio,))
    conn.commit()
    cursor.close()
    conn.close()
    
def editar(id_consultorio, _dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""UPDATE Consultorio SET numero=%s, andar=%s, bloco=%s WHERE id_consultorio=%s""", (*_dados, id_consultorio))

    conn.commit()
    cursor.close()
    conn.close()
