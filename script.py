import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import declarative_base
from faker import Faker
from sqlalchemy import insert
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
    global engine  
    try:
        # 1. Conectarse al servidor para asegurar que la base de datos exista
        with engine.connect() as conexion_servidor:
            # Ejecutamos SQL crudo para crear la base de datos si no existe
            from sqlalchemy import text
            conexion_servidor.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        print(f"¡Base de datos '{DB_NAME}' verificada/creada con éxito!")
        
        # 2. Re-apuntar el motor (engine) a la base de datos específica ya creada
        engine = create_engine(DATABASE_URL)
        
        # 3. Crear la tabla si no existe dentro de esa base de datos
        Base.metadata.create_all(engine)
        print("¡Tabla 'personas_rafael' verificada/creada con éxito!")
        
        # 4. Generar los 100.000 registros en memoria
        lista_de_personas = generar_datos_lote(cantidad=100000)
        
        # 5. Configurar el tamaño del lote (Chunks) para la inserción masiva
        tamano_lote = 5000
        total_registros = len(lista_de_personas)
        print(f"Iniciando inserción masiva en bloques de {tamano_lote}...")
        
        # 6. Abrimos la transacción segura para inyectar los datos
        with engine.begin() as conexion:
            for i in range(0, total_registros, tamano_lote):
                # Cortamos un pedazo de la lista
                lote_actual = lista_de_personas[i:i + tamano_lote]
                
                # Usamos RegistroFalso.__table__ en vez de la clase directa 
                conexion.execute(
                    insert(RegistroFalso.__table__),
                    lote_actual
                )
                print(f"Progreso: {i + len(lote_actual)} / {total_registros} registros insertados.")
                
        print("¡Proceso finalizado con éxito! Los 100.000 registros están en MySQL.")

    except Exception as e:
        print(f"\n[ERROR CRÍTICO]: El proceso se detuvo debido a: {e}", file=sys.stderr)
        print("Se ha aplicado un ROLLBACK automático. La base de datos no sufrió modificaciones estructurales dañadas.")

#Ejecutar la función principal si este script es el programa principal
if __name__ == "__main__":
    main()