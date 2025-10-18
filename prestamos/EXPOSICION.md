# Exposición del Proyecto: Sistema de Préstamos Audiovisuales

Documento de apoyo para presentar el sistema de forma clara y visual.

## Resumen Ejecutivo
- Permite gestionar préstamos de elementos audiovisuales (cámaras, micrófonos, etc.).
- Dos perfiles principales: usuario estándar y administrador.
- Flujo principal: explorar catálogo → solicitar/registrar préstamo → devolver → seguimiento.

## Funcionalidades (visión visual)

- Mapa de navegación (alto nivel):
  - `Login (/login)` → acceso a la aplicación.
  - `Inicio (/)` → listado de préstamos (vista general, requiere login).
  - `Catálogo (/elementos)` → exploración con filtros por `placa` y `tipo`.
  - `Detalle de elemento (/elemento/<slug>/)` → estado y acción "Solicitar préstamo" si está disponible.
  - `Mis préstamos (/prestamos)` → tabla con estados y acción "Devolver".
  - `Registrar préstamo (/prestamos/nuevo)` → formulario con buscadores de persona y elemento.
  - `Personas (/personas)` → listar, crear y editar personas.
  - `Usuarios (/usuarios)` → gestión de usuarios (solo admin), crear y editar.
  - `Nuevo elemento (/nuevo-elemento)` y `Eliminar (/elementos/eliminar/<id>)`.

- Pantallas clave (qué se ve y qué se puede hacer):
  - `Login`: formulario de email y contraseña; mensajes de validación; botón "Iniciar sesión".
  - `Inicio / Listado de Préstamos`: tabla con columnas ID, Elemento (enlace al detalle), Placa, Persona, Identificación, Rol, Registrado por, Fecha Préstamo, Estado (badge), Fecha Devolución.
  - `Catálogo de Elementos`: cabecera con contador de resultados; filtros a la izquierda (placa, tipo); tabla con Placa, Nombre, Tipo, Estado (badge), Acciones: "Solicitar préstamo" (si disponible) y "Eliminar" (según permisos).
  - `Detalle de Elemento`: título, tipo, placa, descripción, badge de disponibilidad; botón "Solicitar Préstamo" si aplica; botón "Eliminar" (si admin o propietario); enlace "Volver a la lista".
  - `Mis Préstamos`: tabla enfocada al usuario actual con Elemento, Tipo, Fecha, Estado (badge por color), Registrado por; acción "Devolver" si no está devuelto/cancelado.
  - `Registrar Préstamo`: formulario con select de Persona y Elemento; buscadores "Buscar persona" y "Buscar elemento"; notas; acciones "Cancelar" y "Guardar".
  - `Personas`: listado, formulario de alta/edición; campos básicos (nombre, apellido, identificación, email, teléfono, rol).
  - `Usuarios (admin)`: listado; formulario con nombre, email, contraseña, y check "Es administrador".
  - Navbar: accesos a Préstamos (mis préstamos, registrar), Catálogo (elementos, nuevo), Personas (lista y nueva), Administración (usuarios). Indicador "Hola, <nombre>" y "Cerrar sesión".

## Base de Datos

- Entidades principales:
  - `Usuario` (tabla `usuario`): `id`, `nombre`, `email` (único), `password_hash`, `es_admin`.
  - `ElementoAudiovisual` (tabla `elementos_audiovisuales`): `id`, `placa` (único), `nombre`, `tipo`, `descripcion`, `disponible`, `slug` (único), `user_id` (FK a `usuario`).
  - `Persona` (tabla `persona`): `id`, `nombre`, `apellido`, `identificacion` (único), `email` (opcional, validación de unicidad a nivel de formulario), `telefono`, `rol`.
  - `Prestamo` (tabla `prestamo`): `id`, `usuario_id` (FK), `elemento_id` (FK), `persona_id` (FK), `fecha_prestamo`, `fecha_devolucion`, `estado` (`pendiente`, `activo`, `devuelto`, `cancelado`), `notas`.

- Relaciones (diagrama textual):
  - `Usuario (1) ── (N) Prestamo`
  - `Persona (1) ── (N) Prestamo`
  - `ElementoAudiovisual (1) ── (N) Prestamo`
  - `Usuario (1) ── (N) ElementoAudiovisual`

- Reglas y consistencia:
  - Unicidad: `Usuario.email`, `ElementoAudiovisual.placa`, `ElementoAudiovisual.slug`, `Persona.identificacion`.
  - Validaciones de formulario: email único para `Usuario` y `Persona` (al crear/editar), identificación única en `Persona`.
  - Disponibilidad: al crear préstamo, el elemento pasa a `disponible=False`; al devolver, vuelve a `True`.

- Datos de ejemplo (seeding):
  - Admin: `admin@prestamos.com` / `admin123`.
  - Usuario: `usuario@prestamos.com` / `usuario123`.
  - Varios elementos (cámara, micrófono, proyector, trípode) y personas (estudiante, docente, administrativo).

## Código Fuente (cómo está organizado)

- Núcleo de la app
  - `src/prestamos/run.py`: configuración de Flask, registro de rutas, protección de vistas con login, flujos de préstamos.
  - `src/prestamos/models.py`: modelos SQLAlchemy (`Usuario`, `ElementoAudiovisual`, `Persona`, `Prestamo`) y helpers (p. ej. generación de `slug`).
  - `src/prestamos/forms.py`: formularios (WTForms) y validaciones de unicidad para emails e identificación.
  - `src/prestamos/config.py`: configuración (secret, conexión DB por `DATABASE_URL` o variables `POSTGRES_*`).
  - `src/prestamos/database.py`: instancia de SQLAlchemy y bootstrap de la DB.

- Plantillas (UI)
  - `templates/base_template.html`: layout principal, Navbar y contenedor.
  - `templates/index.html`: catálogo de elementos (filtros y tabla).
  - `templates/elemento_view.html`: detalle de elemento.
  - `templates/prestamos/form.html` y `templates/prestamos/lista.html`: alta/listado de préstamos.
  - `templates/mis_prestamos.html`: vista personal de préstamos.
  - `templates/personas/*` y `templates/usuarios/*`: ABM de personas y usuarios.
  - `templates/admin/login_form.html` y `admin/elemento_form.html`: autenticación y alta de elementos.

- Inicialización de base de datos
  - `src/prestamos/db_init.py`: crea tablas y carga datos de ejemplo.
  - `create_db.py`: resetea la base de datos PostgreSQL y ejecuta el seeding.

## Flujos recomendados para demo
- Ingreso con `admin@prestamos.com` → revisar `Usuarios` y `Personas` → crear un elemento → ir al `Catálogo` y solicitar o registrar un préstamo → ver `Mis préstamos` y probar "Devolver".
- Ingreso con `usuario@prestamos.com` → navegar `Catálogo`, solicitar un préstamo, y seguir el estado.

## Apuntes visuales
- Estados con badges de color (pendiente, activo, devuelto) para facilitar lectura.
- Acciones por fila en tablas (solicitar, devolver, eliminar) para minimizar clicks.
- Filtros de catálogo en la parte superior para una exploración rápida.