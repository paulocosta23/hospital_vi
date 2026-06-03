import mysql.connector
import os 
from dotenv import load_dotenv

load_dotenv()

def conectar():
    try: 
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            port=os.getenv("DB_PORT"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            ssl_disabled=False 
        )
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

# conexao = conectar()
# if conexao:
#     print("Conexão bem-sucedida!")
