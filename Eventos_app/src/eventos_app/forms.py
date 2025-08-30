from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email

class EventForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    date = DateField('Fecha', validators=[DataRequired()])
    time = TimeField('Hora', validators=[DataRequired()])
    location = StringField('Ubicación', validators=[DataRequired()])
    category = SelectField('Categoría', choices=[])
    max_attendees = IntegerField('Máximo de asistentes', validators=[DataRequired()])
    featured = SelectField('Destacado', choices=[('True', 'Sí'), ('False', 'No')])
    submit = SubmitField('Crear Evento')

class RegistrationForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrarse')
