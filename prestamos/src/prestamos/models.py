from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from prestamos.database import db
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from flask import url_for

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text)  # Cambiado a Text para soportar hashes de cualquier longitud
    es_admin = db.Column(db.Boolean, default=False)
    prestamos = db.relationship('Prestamo', backref='usuario', lazy='dynamic')
    elementos = db.relationship('ElementoAudiovisual', backref='usuario', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()

class ElementoAudiovisual(db.Model):
    __tablename__ = 'elementos_audiovisuales'
    
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    disponible = db.Column(db.Boolean, default=True)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    prestamos = db.relationship('Prestamo', backref='elemento', lazy=True)

    def _generate_unique_slug(self):
        base = slugify(f"{self.nombre}-{self.placa}") if self.nombre else slugify(self.placa)
        candidate = base
        index = 1
        while ElementoAudiovisual.query.filter_by(slug=candidate).first():
            candidate = f"{base}-{index}"
            index += 1
        return candidate

    def save(self):
        if not getattr(self, 'slug', None):
            self.slug = self._generate_unique_slug()
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Reintentar con slug único
            self.slug = self._generate_unique_slug()
            db.session.add(self)
            db.session.commit()

    def public_url(self):
        return url_for('ver_elemento_slug', slug=self.slug)

    @staticmethod
    def get_by_slug(slug):
        return ElementoAudiovisual.query.filter_by(slug=slug).first()

    @staticmethod
    def get_all():
        return ElementoAudiovisual.query.all()

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    identificacion = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    rol = db.Column(db.String(20), nullable=False)  # estudiante, administrativo, docente
    prestamos = db.relationship('Prestamo', backref='persona', lazy='dynamic')
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class Prestamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    elemento_id = db.Column(db.Integer, db.ForeignKey('elementos_audiovisuales.id'), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, activo, devuelto, cancelado
    notas = db.Column(db.Text)