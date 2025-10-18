from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from prestamos.models import Usuario, Persona

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')


class ElementoForm(FlaskForm):
    placa = StringField('Número de Placa', validators=[DataRequired()])
    nombre = StringField('Nombre del Elemento', validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[
        ('camara', 'Cámara'),
        ('microfono', 'Micrófono'),
        ('tripode', 'Trípode'),
        ('iluminacion', 'Equipo de Iluminación'),
        ('audio', 'Equipo de Audio'),
        ('otro', 'Otro')
    ], validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Guardar Elemento')

class PersonaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    identificacion = StringField('Identificación', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    telefono = StringField('Teléfono')
    rol = SelectField('Rol', choices=[
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('administrativo', 'Administrativo')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar Persona')
    
    def validate_identificacion(self, identificacion):
        persona = Persona.query.filter_by(identificacion=identificacion.data).first()
        if persona is not None and persona.id != getattr(self, 'id_persona', None):
            raise ValidationError('Esta identificación ya está registrada.')

    def validate_email(self, email):
        if email.data:
            persona = Persona.query.filter_by(email=email.data).first()
            if persona is not None and persona.id != getattr(self, 'id_persona', None):
                raise ValidationError('Este email ya está registrado.')

class PrestamoForm(FlaskForm):
    persona_id = SelectField('Persona', coerce=int, validators=[DataRequired()])
    elemento_id = SelectField('Elemento', coerce=int, validators=[DataRequired()])
    notas = TextAreaField('Notas o Comentarios')
    submit = SubmitField('Registrar Préstamo')
    
class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    es_admin = BooleanField('Es Administrador')
    submit = SubmitField('Guardar Usuario')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario is not None and usuario.id != getattr(self, 'id_usuario', None):
            raise ValidationError('Este email ya está registrado.')