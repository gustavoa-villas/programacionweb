# src/eventos_app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import StringField, TextAreaField, DateField, TimeField, IntegerField, SelectField, BooleanField

class RegistrationForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = EmailField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrarse')
    

class EventForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    date = DateField('Fecha', validators=[DataRequired()])
    time = TimeField('Hora', validators=[DataRequired()])
    location = StringField('Ubicación', validators=[DataRequired()])
    category = SelectField('Categoría', choices=[])
    max_attendees = IntegerField('Máximo de asistentes', validators=[DataRequired()])
    featured = BooleanField('¿Evento destacado?')
    submit = SubmitField('Crear evento')

