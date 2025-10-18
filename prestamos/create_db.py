import os
import sys
import psycopg

# Configuración de PostgreSQL
postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'Prestamos123')
postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_port = os.environ.get('POSTGRES_PORT', '5432')
postgres_db = os.environ.get('POSTGRES_DB', 'prestamos_db')

def reset_database():
    """Elimina y recrea la base de datos PostgreSQL"""
    try:
        # Conectar al catálogo 'postgres' usando psycopg v3
        conn = psycopg.connect(
            f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Cerrar conexiones activas a la base de datos
        cursor.execute(
            """
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = %s
            AND pid <> pg_backend_pid()
            """,
            (postgres_db,)
        )

        # Eliminar la base de datos si existe
        cursor.execute("DROP DATABASE IF EXISTS " + postgres_db)
        print(f"Base de datos '{postgres_db}' eliminada.")

        # Crear la base de datos
        cursor.execute("CREATE DATABASE " + postgres_db)
        print(f"Base de datos '{postgres_db}' creada exitosamente.")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al resetear la base de datos: {e}")
        return False

if __name__ == "__main__":
    if reset_database():
        # Ejecutar el script de inicialización de tablas
        print("Inicializando tablas y datos de ejemplo...")
        os.system(f"{sys.executable} -m src.prestamos.db_init")
        print("Base de datos configurada correctamente.")
    else:
        print("No se pudo resetear la base de datos. Verifique la configuración de PostgreSQL.")