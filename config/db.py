import os 
from dotenv import load_dotenv

load_dotenv()

# Prefer PyMySQL (pure-Python) to avoid C-extension crashes; fall back to mysql.connector
try:
    import pymysql
    from pymysql.cursors import DictCursor
    _DB_DRIVER = 'pymysql'
except Exception:
    import mysql.connector
    _DB_DRIVER = 'mysqlconnector'

def conectar():
    try: 
        if _DB_DRIVER == 'pymysql':
            raw_conn = pymysql.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                port=int(os.getenv("DB_PORT")),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE"),
                connect_timeout=5,
                charset='utf8mb4'
            )

            # wrapper to provide cursor(dictionary=True) compatibility
            class _ConnWrapper:
                def __init__(self, conn):
                    self._conn = conn

                def cursor(self, dictionary=False):
                    if dictionary:
                        return self._conn.cursor(DictCursor)
                    return self._conn.cursor()

                def commit(self):
                    return self._conn.commit()

                def close(self):
                    return self._conn.close()

                def __getattr__(self, name):
                    return getattr(self._conn, name)

            return _ConnWrapper(raw_conn)

        else:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                port=int(os.getenv("DB_PORT")),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE"),
                #ssl_disabled=False 
                connection_timeout=5
            )
    
    except Exception as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        mostrar_erro_de_conexao()
        return None


def mostrar_erro_de_conexao():
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Erro de conexão",
            "Não foi possível conectar ao banco de dados. Verifique sua conexão e tente novamente."
        )
        root.destroy()
    except Exception as err:
        print("Erro de conexão com o banco de dados. Verifique sua conexão e tente novamente.", err)
