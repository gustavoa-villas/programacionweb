# Sistema de Préstamos Audiovisuales

Aplicación web para gestionar el préstamo de elementos audiovisuales (cámaras, micrófonos, etc.) construida con Flask.

## Requisitos
- Python 3.8 o superior
- Pip
- (Opcional) PostgreSQL 13+ si usas la opción B de base de datos

## Instalación
1) Clonar el repositorio
```
git clone <URL_DEL_REPOSITORIO>
cd prestamos
```

2) (Opcional pero recomendado) Crear entorno virtual
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Instalar dependencias
```
pip install -e .
```

## Configuración de la base de datos
La aplicación lee la URL de base de datos desde `DATABASE_URL`. Si no está definida, usará PostgreSQL con las variables `POSTGRES_*`.

- Variables disponibles:
  - `DATABASE_URL` (prioritaria). Ejemplo SQLite: `sqlite:///prestamos.db`
  - `POSTGRES_USER` (por defecto `postgres`)
  - `POSTGRES_PASSWORD` (por defecto `Prestamos123`)
  - `POSTGRES_HOST` (por defecto `localhost`)
  - `POSTGRES_PORT` (por defecto `5432`)
  - `POSTGRES_DB` (por defecto `prestamos_db`)

### Opción A (rápida): SQLite
```
$env:DATABASE_URL = "sqlite:///prestamos.db"
python -m src.prestamos.db_init   # crea tablas y carga datos de ejemplo
```

### Opción B (recomendada): PostgreSQL
Configura credenciales y ejecuta el script de creación:
```
$env:POSTGRES_USER = "postgres"
$env:POSTGRES_PASSWORD = "Prestamos123"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "5432"
$env:POSTGRES_DB = "prestamos_db"

python create_db.py  # resetea BD, crea tablas y carga datos de ejemplo
```

## Ejecución
Configura las variables de Flask y levanta el servidor:
```
$env:FLASK_APP = "src\prestamos\run.py"
$env:FLASK_ENV = "development"
flask run
```
La app queda disponible en `http://127.0.0.1:5000/`.

También puedes ejecutar directamente:
```
python .\src\prestamos\run.py
```

## Credenciales de ejemplo
Se crean con los scripts de inicialización:
- Admin: `admin@prestamos.com` / `admin123`
- Usuario: `usuario@prestamos.com` / `usuario123`

Todas las vistas (excepto `login`) requieren sesión iniciada.

## Rutas clave
- Inicio (listado de préstamos): `/` (requiere login)
- Iniciar sesión: `/login`
- Cerrar sesión: `/logout`
- Catálogo de elementos: `/elementos`
- Ver detalle de elemento (slug): `/elemento/<slug>/`
- Solicitar préstamo (desde un elemento): `/solicitar-prestamo/<int:elemento_id>`
- Mis préstamos: `/prestamos`
- Registrar préstamo (admin/usuarios con permisos mediante formulario): `/prestamos/nuevo`
- Listado de préstamos (administración): `/prestamos/lista`
- Personas: listar `/personas`, nueva `/personas/nueva`, editar `/personas/editar/<id>`
- Usuarios (solo admin): listar `/usuarios`, nuevo `/usuarios/nuevo`, editar `/usuarios/editar/<id>`
- Elementos: crear `/nuevo-elemento`, eliminar (POST) `/elementos/eliminar/<id>`
- Devolver préstamo: `/devolver-prestamo/<int:prestamo_id>`

## Validaciones y reglas destacadas
- Usuario: email único (no permite duplicados al crear/editar).
- Persona: identificación única y email único (no permite duplicados al crear/editar).
- Elemento: `placa` única (restricción de base de datos) y slug único generado automáticamente.
- Préstamos: al registrar, el elemento pasa a no disponible; al devolver, vuelve a disponible.
- Acceso: rutas administrativas protegidas para usuarios con `es_admin=True`.

## Estructura del proyecto (resumen)
```
prestamos/
├── pyproject.toml
├── README.md
└── src/
    └── prestamos/
        ├── config.py
        ├── database.py
        ├── db_init.py
        ├── forms.py
        ├── models.py
        ├── run.py
        ├── static/
        └── templates/
            ├── admin/
            │   ├── elemento_form.html
            │   └── login_form.html
            ├── prestamos/
            │   ├── form.html
            │   └── lista.html
            ├── personas/
            │   ├── form.html
            │   └── lista.html
            ├── usuarios/
            │   ├── form.html
            │   └── lista.html
            ├── base_template.html
            ├── elemento_view.html
            ├── index.html
            └── mis_prestamos.html
```

## Modo depuración
```
flask run --debug
```

## Notas
- Si usas PostgreSQL, asegúrate de que el servicio esté activo y que el usuario tenga permisos de creación de bases de datos si vas a usar `create_db.py`.
- Para SQLite, no se requiere servicio externo; el archivo `.db` se crea localmente.