from flask import Flask
from prestamos.database import db
from prestamos.models import Usuario, ElementoAudiovisual, Prestamo, Persona
from werkzeug.security import generate_password_hash
from prestamos import config

def create_app():
    """Crea una instancia de la aplicación para inicializar la base de datos"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    return app

def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente.")

def add_sample_data():
    """Agrega datos de ejemplo a la base de datos"""
    app = create_app()
    with app.app_context():
        # Crear usuarios de ejemplo
        admin = Usuario.query.filter_by(email='admin@prestamos.com').first()
        if admin is None:
            admin = Usuario(
                nombre='Administrador',
                email='admin@prestamos.com',
                es_admin=True
            )
            admin.password_hash = generate_password_hash('admin123')
            db.session.add(admin)
        
        usuario = Usuario.query.filter_by(email='usuario@prestamos.com').first()
        if usuario is None:
            usuario = Usuario(
                nombre='Usuario Regular',
                email='usuario@prestamos.com',
                es_admin=False
            )
            usuario.password_hash = generate_password_hash('usuario123')
            db.session.add(usuario)

        # Asegurar IDs disponibles
        db.session.flush()
        
        # Crear elementos audiovisuales de ejemplo
        if not ElementoAudiovisual.query.first():
            elementos = [
                ElementoAudiovisual(
                    placa='CAM001',
                    nombre='Cámara Sony HD',
                    tipo='Cámara',
                    descripcion='Cámara de video de alta definición para grabaciones profesionales',
                    user_id=admin.id,
                    disponible=True
                ),
                ElementoAudiovisual(
                    placa='MIC001',
                    nombre='Micrófono Inalámbrico',
                    tipo='Audio',
                    descripcion='Micrófono inalámbrico para entrevistas y grabaciones en exteriores',
                    user_id=admin.id,
                    disponible=True
                ),
                ElementoAudiovisual(
                    placa='PRY001',
                    nombre='Proyector Epson',
                    tipo='Video',
                    descripcion='Proyector de alta luminosidad para presentaciones',
                    user_id=admin.id,
                    disponible=True
                ),
                ElementoAudiovisual(
                    placa='TRP001',
                    nombre='Trípode Profesional',
                    tipo='Accesorio',
                    descripcion='Trípode estable para cámaras de video y fotografía',
                    user_id=admin.id,
                    disponible=True
                )
            ]
            
            for elemento in elementos:
                elemento.save()
                
        # Crear personas de ejemplo
        if not Persona.query.first():
            personas = [
                Persona(
                    nombre='Juan',
                    apellido='Pérez',
                    identificacion='1234567890',
                    email='juan.perez@ejemplo.com',
                    telefono='3001234567',
                    rol='estudiante'
                ),
                Persona(
                    nombre='María',
                    apellido='González',
                    identificacion='0987654321',
                    email='maria.gonzalez@ejemplo.com',
                    telefono='3109876543',
                    rol='docente'
                ),
                Persona(
                    nombre='Carlos',
                    apellido='Rodríguez',
                    identificacion='5678901234',
                    email='carlos.rodriguez@ejemplo.com',
                    telefono='3205678901',
                    rol='administrativo'
                )
            ]
            
            for persona in personas:
                db.session.add(persona)
        
        db.session.commit()
        print("Datos de ejemplo agregados correctamente.")

if __name__ == '__main__':
    init_db()
    add_sample_data()