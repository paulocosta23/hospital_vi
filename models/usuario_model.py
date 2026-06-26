from config.db import conectar

def autenticar(username, senha):
    conn = conectar()
    cursor = conn.cursor()


    # Verificar se usuário existe
    cursor.execute(
        "SELECT senha_usuario, tipo_login, nome_usuario, id_usuario FROM Usuario WHERE login_usuario = %s", (username,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if not usuario:
        return "usuario_nao_existe"
    
    senha_db, tipo, nome, id_usuario = usuario

    if senha != senha_db:
        return "Senha_incorreta"
    
    return ("ok", tipo, nome, id_usuario)

def inserir(_dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Usuario (nome_usuario, cpf_usuario, login_usuario, tipo_login, senha_usuario)
                   VALUES (%s, %s, %s, %s, %s)
                   """, _dados)
    id_usuario = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    
    return id_usuario

def remover(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))

    conn.commit()
    cursor.close()
    conn.close()

def listar():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT
                   id_usuario,
                   nome_usuario as nome,
                   cpf_usuario as cpf,
                   login_usuario as login,
                   tipo_login as tipo,
                   senha_usuario as senha
                   FROM Usuario""")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados
def editar(id_usuario, _dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE Usuario SET nome_usuario=%s, cpf_usuario=%s, login_usuario=%s, tipo_login=%s, senha_usuario=%s
                   WHERE id_usuario=%s
                   """, (*_dados, id_usuario))
    conn.commit()
    cursor.close()
    conn.close()

