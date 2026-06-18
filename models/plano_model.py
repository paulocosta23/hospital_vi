from config.db import conectar

def inserir(_dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Plano (nome, telefone)
                   VALUES (%s, %s)""", _dados)
    conn.commit()
    cursor.close()
    conn.close

def editar(id_plano, _dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""UPDATE Plano SET nome=%s, telefone=%s
                   WHERE id_plano=%s""", 
                   (*_dados, id_plano))
    
    conn.commit()
    cursor.close()
    conn.close()

def listar():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT
                   id_plano,
                   nome,
                   telefone as status
                   FROM Plano""")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

def remover(id_plano):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Plano WHERE id_plano=%s", (id_plano,))
    conn.commit()
    cursor.close()
    conn.close()
    

