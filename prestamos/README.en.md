# Audiovisual Loans System

Web application to manage loans of audiovisual equipment (cameras, microphones, etc.) built with Flask.

## Requirements
- Python 3.8+
- Pip
- (Optional) PostgreSQL 13+ if you use the database Option B

## Installation
1) Clone the repository
```
git clone <REPO_URL>
cd prestamos
```

2) (Optional but recommended) Create a virtual environment
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Install dependencies
```
pip install -e .
```

## Database Configuration
The application reads the database URL from `DATABASE_URL`. If it is not defined, it falls back to PostgreSQL using `POSTGRES_*` variables.

- Available variables:
  - `DATABASE_URL` (preferred). SQLite example: `sqlite:///prestamos.db`
  - `POSTGRES_USER` (default `postgres`)
  - `POSTGRES_PASSWORD` (default `Prestamos123`)
  - `POSTGRES_HOST` (default `localhost`)
  - `POSTGRES_PORT` (default `5432`)
  - `POSTGRES_DB` (default `prestamos_db`)

### Option A (quick): SQLite
```
$env:DATABASE_URL = "sqlite:///prestamos.db"
python -m src.prestamos.db_init   # creates tables and loads sample data
```

### Option B (recommended): PostgreSQL
Set credentials and run the creation script:
```
$env:POSTGRES_USER = "postgres"
$env:POSTGRES_PASSWORD = "Prestamos123"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "5432"
$env:POSTGRES_DB = "prestamos_db"

python create_db.py  # resets DB, creates tables and loads sample data
```

## Running the Application
Set Flask variables and start the server:
```
$env:FLASK_APP = "src\prestamos\run.py"
$env:FLASK_ENV = "development"
flask run
```
The app will be available at `http://127.0.0.1:5000/`.

You can also run directly:
```
python .\src\prestamos\run.py
```

## Sample Credentials
The initialization scripts create:
- Admin: `admin@prestamos.com` / `admin123`
- User: `usuario@prestamos.com` / `usuario123`

All views (except `login`) require an authenticated session.

## Key Routes
- Home (loans list): `/` (requires login)
- Login: `/login`
- Logout: `/logout`
- Elements catalog: `/elementos`
- Element detail (slug): `/elemento/<slug>/`
- Request a loan (from an element): `/solicitar-prestamo/<int:elemento_id>`
- My loans: `/prestamos`
- Register a loan: `/prestamos/nuevo`
- Loans list (admin): `/prestamos/lista`
- People: list `/personas`, new `/personas/nueva`, edit `/personas/editar/<id>`
- Users (admin only): list `/usuarios`, new `/usuarios/nuevo`, edit `/usuarios/editar/<id>`
- Elements: create `/nuevo-elemento`, delete (POST) `/elementos/eliminar/<id>`
- Return a loan: `/devolver-prestamo/<int:prestamo_id>`

## Validations and Business Rules
- User: unique email (no duplicates when creating/editing).
- Person: unique identification and unique email (no duplicates when creating/editing).
- Element: unique `placa` (database constraint) and auto-generated unique slug.
- Loans: when registering, the element becomes not available; when returning, it becomes available again.
- Access: administrative routes protected for users with `es_admin=True`.

## Project Structure (summary)
```
prestamos/
├── pyproject.toml
├── README.md
├── README.en.md
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

## Debug Mode
```
flask run --debug
```

## Notes
- If using PostgreSQL, ensure the service is running and the user has permission to create databases if you plan to use `create_db.py`.
- For SQLite, no external service is required; the `.db` file is created locally.