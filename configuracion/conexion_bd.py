import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    usuario = os.getenv("DB_USER")
    clave = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")

    if not usuario or not clave or not dsn:
        raise RuntimeError("Faltan variables en .env: DB_USER, DB_PASSWORD, DB_DSN")

    return oracledb.connect(user=usuario, password=clave, dsn=dsn)
