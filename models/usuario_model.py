from config.db import conectar

def autenticar(username, senha):
    conn = conectar()
    cursor = conn.cursor()


    # Verificar se usuário existe
    cursor.execute(
        "SELECT senha, tipo FROM Usuario WHERE username=%s", (username,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if not usuario:
        return "usuario_nao_existe"
    
    senha_db, tipo = usuario

    if senha != senha_db:
        return "Senha_incorreta"
    
    return ("ok", tipo)