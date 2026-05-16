import os
from dotenv import load_dotenv
import sys

# Cargar las variables ocultas del archivo .env
load_dotenv()

# Función principal para ejecutar el proceso completo
def main():
    try:
        print("Iniciando la configuracion de la automatizacion...")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO]: El proceso se detuvo debido a: {e}", file=sys.stderr)

#Ejecutar la función principal si este script es el programa principal
if __name__ == "__main__":
    main()