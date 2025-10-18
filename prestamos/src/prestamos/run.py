from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import os
from datetime import datetime
from prestamos.config import *
from prestamos.database import db
from prestamos.models import Usuario, ElementoAudiovisual, Prestamo, Persona
from urllib.parse import urlparse, urljoin
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = LOGIN_MESSAGE

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.before_request
def check_login():
    endpoint = request.endpoint
    if endpoint in ('login', 'static'):
        return
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

# Rutas principales
@app.route('/')
@login_required
def index():
    prestamos = Prestamo.query.order_by(Prestamo.fecha_prestamo.desc()).all()
    return render_template('prestamos/lista.html', prestamos=prestamos)

@app.route('/elementos')
@login_required
def listar_elementos():
    placa = request.args.get('placa', '').strip()
    tipo = request.args.get('tipo', '').strip()
    query = ElementoAudiovisual.query
    if placa:
        query = query.filter(ElementoAudiovisual.placa.ilike(f"%{placa}%"))
    if tipo:
        query = query.filter(ElementoAudiovisual.tipo.ilike(f"%{tipo}%"))
    elementos = query.all()
    tipos = [t[0] for t in db.session.query(ElementoAudiovisual.tipo).distinct().all()]
    return render_template('index.html', elementos=elementos, placa=placa, tipo=tipo, tipos=tipos)

@app.route('/elemento/<slug>/')
@login_required
def ver_elemento_slug(slug):
    elemento = ElementoAudiovisual.get_by_slug(slug)
    if not elemento:
        abort(404)
    return render_template('elemento_view.html', elemento=elemento)

@app.route('/prestamos')
@login_required
def mis_prestamos():
    prestamos = Prestamo.query.filter_by(usuario_id=current_user.id).all()
    return render_template('mis_prestamos.html', prestamos=prestamos)

@app.route('/prestamos/lista')
@login_required
def listar_prestamos():
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta sección.')
        return redirect(url_for('index'))
    prestamos = Prestamo.query.order_by(Prestamo.fecha_prestamo.desc()).all()
    return render_template('prestamos/lista.html', prestamos=prestamos)

@app.route('/prestamos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_prestamo():
    from prestamos.forms import PrestamoForm
    form = PrestamoForm()

    # Soporte de buscador por GET
    q_persona = request.args.get('q_persona', '').strip()
    q_elemento = request.args.get('q_elemento', '').strip()

    # Cargar opciones de personas con filtro
    per_query = Persona.query
    if q_persona:
        per_query = per_query.filter(or_(
            Persona.nombre.ilike(f"%{q_persona}%"),
            Persona.apellido.ilike(f"%{q_persona}%"),
            Persona.identificacion.ilike(f"%{q_persona}%")
        ))
    personas = per_query.order_by(Persona.nombre).all()
    form.persona_id.choices = [(p.id, f"{p.nombre_completo} - {p.identificacion} ({p.rol})") for p in personas]

    # Cargar opciones de elementos disponibles con filtro
    elem_query = ElementoAudiovisual.query.filter_by(disponible=True)
    if q_elemento:
        elem_query = elem_query.filter(or_(
            ElementoAudiovisual.placa.ilike(f"%{q_elemento}%"),
            ElementoAudiovisual.nombre.ilike(f"%{q_elemento}%"),
            ElementoAudiovisual.tipo.ilike(f"%{q_elemento}%")
        ))
    elementos = elem_query.all()
    form.elemento_id.choices = [(e.id, f"{e.placa} - {e.nombre}") for e in elementos]

    if form.validate_on_submit():
        elemento = ElementoAudiovisual.query.get(form.elemento_id.data)
        if elemento and elemento.disponible:
            prestamo = Prestamo(
                usuario_id=current_user.id,
                elemento_id=form.elemento_id.data,
                persona_id=form.persona_id.data,
                notas=form.notas.data,
                estado='activo',
                fecha_prestamo=datetime.utcnow()
            )
            elemento.disponible = False
            db.session.add(prestamo)
            db.session.commit()
            flash('Préstamo registrado correctamente.')
            return redirect(url_for('mis_prestamos'))
        else:
            flash('El elemento seleccionado no está disponible.')

    return render_template('prestamos/form.html', form=form, titulo='Nuevo Préstamo', q_persona=q_persona, q_elemento=q_elemento)

@app.route('/login', methods=['GET', 'POST'])
def login():
    from prestamos.forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)
            next_page = request.args.get('next')
            if next_page and urlparse(next_page).netloc == '':
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas. Inténtalo de nuevo.')
    return render_template('admin/login_form.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Rutas para gestionar personas
@app.route('/personas')
@login_required
def listar_personas():
    personas = Persona.query.all()
    return render_template('personas/lista.html', personas=personas)

@app.route('/personas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_persona():
    from prestamos.forms import PersonaForm
    form = PersonaForm()
    if form.validate_on_submit():
        persona = Persona(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            identificacion=form.identificacion.data,
            email=form.email.data,
            telefono=form.telefono.data,
            rol=form.rol.data
        )
        db.session.add(persona)
        db.session.commit()
        flash('Persona registrada correctamente.')
        return redirect(url_for('listar_personas'))
    return render_template('personas/form.html', form=form, titulo='Nueva Persona')

@app.route('/personas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_persona(id):
    persona = Persona.query.get_or_404(id)
    from prestamos.forms import PersonaForm
    form = PersonaForm(obj=persona)
    form.id_persona = id
    if form.validate_on_submit():
        persona.nombre = form.nombre.data
        persona.apellido = form.apellido.data
        persona.identificacion = form.identificacion.data
        persona.email = form.email.data
        persona.telefono = form.telefono.data
        persona.rol = form.rol.data
        db.session.commit()
        flash('Datos de la persona actualizados correctamente.')
        return redirect(url_for('listar_personas'))
    return render_template('personas/form.html', form=form, titulo='Editar Persona')

@app.post('/personas/eliminar/<int:id>')
@login_required
def eliminar_persona(id):
    if not current_user.es_admin:
        flash('No tienes permiso para eliminar personas.')
        return redirect(url_for('listar_personas'))
    persona = Persona.query.get_or_404(id)
    prestamos_count = Prestamo.query.filter_by(persona_id=id).count()
    if prestamos_count > 0:
        flash('No se puede eliminar la persona porque tiene préstamos asociados.')
        return redirect(url_for('listar_personas'))
    db.session.delete(persona)
    db.session.commit()
    flash('Persona eliminada correctamente.')
    return redirect(url_for('listar_personas'))

@app.route('/solicitar-prestamo/<int:elemento_id>', methods=['GET', 'POST'])
@login_required
def solicitar_prestamo(elemento_id):
    from prestamos.forms import PrestamoForm
    
    elemento = ElementoAudiovisual.query.get_or_404(elemento_id)
    if not elemento.disponible:
        flash('Este elemento no está disponible actualmente.')
        return redirect(url_for('ver_elemento_slug', slug=elemento.slug))
    
    form = PrestamoForm()

    q_persona = request.args.get('q_persona', '').strip()
    q_elemento = request.args.get('q_elemento', '').strip()
    
    # Cargar las opciones de personas con buscador
    per_query = Persona.query
    if q_persona:
        per_query = per_query.filter(or_(
            Persona.nombre.ilike(f"%{q_persona}%"),
            Persona.apellido.ilike(f"%{q_persona}%"),
            Persona.identificacion.ilike(f"%{q_persona}%")
        ))
    personas = per_query.order_by(Persona.nombre).all()
    form.persona_id.choices = [(p.id, f"{p.nombre} {p.apellido} - {p.rol.capitalize()}") for p in personas]
    
    # Cargar las opciones de elementos con buscador y preseleccionar el elemento actual
    elem_query = ElementoAudiovisual.query.filter_by(disponible=True)
    if q_elemento:
        elem_query = elem_query.filter(or_(
            ElementoAudiovisual.placa.ilike(f"%{q_elemento}%"),
            ElementoAudiovisual.nombre.ilike(f"%{q_elemento}%"),
            ElementoAudiovisual.tipo.ilike(f"%{q_elemento}%")
        ))
    elementos = elem_query.all()
    form.elemento_id.choices = [(e.id, f"{e.nombre} - {e.placa}") for e in elementos]
    form.elemento_id.data = elemento_id
    
    if form.validate_on_submit():
        prestamo = Prestamo(
            usuario_id=current_user.id,
            persona_id=form.persona_id.data,
            elemento_id=elemento_id,
            fecha_prestamo=datetime.now(),
            notas=form.notas.data,
            estado='pendiente'
        )
        elemento.disponible = False
        db.session.add(prestamo)
        db.session.commit()
        flash('Solicitud de préstamo realizada correctamente.')
        return redirect(url_for('mis_prestamos'))
    
    return render_template('prestamos/form.html', form=form, titulo='Solicitar Préstamo', q_persona=q_persona, q_elemento=q_elemento, elemento=elemento)

@app.post('/elementos/eliminar/<int:id>')
@login_required
def eliminar_elemento(id):
    elemento = ElementoAudiovisual.query.get_or_404(id)
    prestamos_count = Prestamo.query.filter_by(elemento_id=id).count()
    if prestamos_count > 0 or not elemento.disponible:
        flash('No se puede eliminar el elemento porque tiene préstamos asociados o está prestado.')
        return redirect(url_for('listar_elementos'))
    if elemento.user_id != current_user.id and not current_user.es_admin:
        flash('No tienes permiso para eliminar este elemento.')
        return redirect(url_for('listar_elementos'))
    db.session.delete(elemento)
    db.session.commit()
    flash('Elemento eliminado correctamente.')
    return redirect(url_for('listar_elementos'))

@app.route('/usuarios')
@login_required
def listar_usuarios():
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta sección.')
        return redirect(url_for('index'))
    
    usuarios = Usuario.query.all()
    return render_template('usuarios/lista.html', usuarios=usuarios)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_usuario():
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta sección.')
        return redirect(url_for('index'))
    
    from prestamos.forms import UsuarioForm
    form = UsuarioForm()
    
    if form.validate_on_submit():
        usuario = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            es_admin=form.es_admin.data
        )
        usuario.password_hash = generate_password_hash(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario creado exitosamente.')
        return redirect(url_for('listar_usuarios'))
    
    return render_template('usuarios/form.html', form=form, titulo='Nuevo Usuario')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta sección.')
        return redirect(url_for('index'))
    
    usuario = Usuario.query.get_or_404(id)
    from prestamos.forms import UsuarioForm
    form = UsuarioForm(obj=usuario)
    form.id_usuario = id
    
    if form.validate_on_submit():
        usuario.nombre = form.nombre.data
        usuario.email = form.email.data
        usuario.es_admin = form.es_admin.data
        if form.password.data:
            usuario.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Usuario actualizado exitosamente.')
        return redirect(url_for('listar_usuarios'))
    
    return render_template('usuarios/form.html', form=form, titulo='Editar Usuario')

@app.route('/devolver-prestamo/<int:prestamo_id>')
@login_required
def devolver_prestamo(prestamo_id):
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    if prestamo.usuario_id != current_user.id and not current_user.es_admin:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('mis_prestamos'))
    
    prestamo.fecha_devolucion = datetime.now()
    prestamo.estado = 'devuelto'
    prestamo.elemento.disponible = True
    db.session.commit()
    flash('Elemento devuelto correctamente.')
    return redirect(url_for('mis_prestamos'))

@app.route('/nuevo-elemento', methods=['GET', 'POST'])
@login_required
def nuevo_elemento():
    from prestamos.forms import ElementoForm
    form = ElementoForm()
    if form.validate_on_submit():
        elemento = ElementoAudiovisual(
            placa=form.placa.data,
            nombre=form.nombre.data,
            tipo=form.tipo.data,
            descripcion=form.descripcion.data,
            disponible=True,
            user_id=current_user.id
        )
        elemento.save()
        flash('Elemento audiovisual creado exitosamente.')
        return redirect(url_for('listar_elementos'))
    return render_template('admin/elemento_form.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)