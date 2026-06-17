from config.db import conectar

def inserir(_dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO  Medico (nome, especialidade, crm, id_consultorio)
        VALUES(%s, %s, %s, %s )  
        """, _dados)
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

def lista_consultorios():
    conn = conectar()
    cursor = conn.cursor(dictionary= True)
    
    cursor.execute("SELECT * FROM Consultorio")
   
    consultorios = cursor.fetchall()
    cursor.close()
    conn.close()
    return consultorios

