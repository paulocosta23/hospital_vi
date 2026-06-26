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
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT
                   m.id_medico,
                   m.nome,
                   m.especialidade,
                   m.crm,
                   c.numero as consultorio,
                   m.id_usuario
                   FROM Medico m
                   LEFT JOIN Consultorio c
                   ON m.id_consultorio = c.id_consultorio
                   """)
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    print(dados)
    return dados

def atualizar(_dados, id_medico):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""UPDATE Medico SET nome=%s, especialidade=%s, crm=%s, id_consultorio=%s
                   WHERE id_medico=%s""", (*_dados, id_medico))
    conn.commit()
    cursor.close()
    conn.close()

    
def remover(id_medico):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Medico WHERE id_medico = %s", (id_medico,))

    conn.commit()
    cursor.close()
    conn.close()

def lista_consultorios():
    conn = conectar()
    cursor = conn.cursor(dictionary= True)
    
    cursor.execute("SELECT * FROM Consultorio")
   
    consultorios = cursor.fetchall()
    cursor.close()
    conn.close()
    return consultorios

def vincular_medico_usuario(id_medico, id_usuario):

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Medico SET id_usuario = %s WHERE id_medico = %s",(id_usuario, id_medico)
    )
    conn.commit()

    cursor.close()
    conn.close()

def buscar_por_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_medico, nome FROM Medico WHERE id_usuario = %s", (id_usuario))
   
    dados_medico_logado = cursor.fetchone()
    cursor.close()
    conn.close()
    return dados_medico_logado