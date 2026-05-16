import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import declarative_base
from faker import Faker
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

# Crear la clase base para los modelos (Forma estándar)
Base = declarative_base()

# Definir el modelo (la estructura de la tabla)
class RegistroFalso(Base):
    __tablename__ = 'personas_rafael' 
    
    # Atributo 1: Clave primaria 
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Atributos del 2 al 8  
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(50), nullable=True)
    ciudad = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    profesion = Column(String(100), nullable=True)
    descripcion = Column(Text, nullable=True)

# Crear una función para generar los datos utilizando Faker y almacenarlos en una lista de diccionarios 
def generar_datos_lote(cantidad=100000):
    fake = Faker('es_ES')
    datos = []
    
    print(f"Generando {cantidad} registros ficticios en memoria...")
    
    for i in range(1, cantidad + 1):
        # Usamos el índice 'i' para asegurar que el correo JAMÁS se repita
        correo_unico = f"persona.{i}.{fake.uuid4()[:8]}@{fake.free_email_domain()}"
        
        registro = {
            "nombre": fake.name(),
            "correo": correo_unico,
            "telefono": fake.phone_number(),
            "ciudad": fake.city(),
            "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=75),
            "profesion": fake.job(),
            "descripcion": fake.text(max_nb_chars=180)
        }
        datos.append(registro)
        
    print("¡Generación de datos completada en memoria!")
    return datos

# Función principal para ejecutar el proceso completo
def main():
    try:
        print("Modelo ORM definido y funcion generadora de Faker lista.")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO]: El proceso se detuvo debido a: {e}", file=sys.stderr)

#Ejecutar la función principal si este script es el programa principal
if __name__ == "__main__":
    main()