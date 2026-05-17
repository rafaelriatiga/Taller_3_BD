# Automatización de Inserción Masiva (100k Registros)

Este proyecto es un script en Python que automatiza la creación de una base de datos local y maneja la inyección masiva de **100,000 registros ficticios** en MySQL usando SQLAlchemy y Faker.

> 💡 **Nota:** El script es 100% automático. No se necesita crear la base de datos ni la tabla manualmente en MySQL o DBeaver; el propio código verifica si existen en el servidor local y las crea desde cero antes de iniciar la carga.

## 🚀 Características y Optimización
* **Inserción por bloques (Chunks):** Divide los 100,000 registros en lotes de 5,000 para optimizar el uso de memoria y acelerar la carga en MySQL.
* **Datos únicos en español:** Usa Faker configurado en `es_ES` y genera correos electrónicos con identificadores únicos para evitar errores de duplicidad.
* **Seguridad:** Las credenciales de MySQL de la máquina local se manejan de forma segura a través de un archivo `.env` (oculto en Git).

## 🛠️ Requisitos y Dependencias
Para correr el proyecto se necesita tener el servidor de **MySQL Server** activo y las librerías del archivo `requirements.txt`:
* `SQLAlchemy` y `PyMySQL` (con `cryptography` para la conexión segura).
* `python-dotenv`
* `Faker`