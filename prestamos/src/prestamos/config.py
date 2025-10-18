import os

# Configuración de la aplicación
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-por-defecto')

# Configuración de PostgreSQL
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'Prestamos123')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'prestamos_db')

# URI de conexión a PostgreSQL (psycopg v3)
POSTGRES_URI = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', POSTGRES_URI)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración del sistema de login
LOGIN_MESSAGE = "Por favor inicia sesión para acceder a esta página."