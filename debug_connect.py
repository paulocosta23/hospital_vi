import traceback
from config import db
import sys

try:
    print('Chamando conectar()...')
    conn = db.conectar()
    print('Retornou:', type(conn), conn)
except Exception as e:
    print('Exception type:', type(e))
    traceback.print_exc()
    sys.exit(1)
else:
    print('Done')
