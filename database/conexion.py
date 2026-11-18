import os
import psycopg2
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'servidor', 'backend', '.env'))

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("No se encontró DATABASE_URL en el archivo .env")
    return psycopg2.connect(database_url)
