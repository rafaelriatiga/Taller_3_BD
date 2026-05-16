import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys

# Cargar las variables ocultas del archivo .env
load_dotenv()

# Extraer los valores y guardarlos en variables de Python
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Crear una URL genérica (SIN el nombre de la base de datos al final)
URL_SERVIDOR = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"

# Crear la URL completa que usará SQLAlchemy después
DATABASE_URL = f"{URL_SERVIDOR}/{DB_NAME}"

# Crear el motor de conexión inicial apuntando al servidor general
engine = create_engine(URL_SERVIDOR)

# Función principal para ejecutar el proceso completo
def main():
    try:
        print("Variables de entorno cargadas y motor de conexion inicial creado con exito.")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO]: El proceso se detuvo debido a: {e}", file=sys.stderr)

#Ejecutar la función principal si este script es el programa principal
if __name__ == "__main__":
    main()