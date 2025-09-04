# src/eventos_app/app.py

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from eventos_app.data import events, categories
from eventos_app.forms import RegistrationForm, EventForm

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  # Necesaria para Flask-WTF


@app.route("/")
def index():
    featured_events = [e for e in events if e.get('featured')]
    upcoming_events = events  # Aquí luego puedes filtrar por fecha si lo deseas
    return render_template("index.html", events=upcoming_events, featured=featured_events)


@app.route("/event/<slug>/")
def event_detail(slug):
    event = next((e for e in events if e['slug'] == slug), None)
    if event is None:
        abort(404)
    return render_template("event_detail.html", event=event)


@app.route("/event/<slug>/register/", methods=["GET", "POST"])
def register(slug):
    event = next((e for e in events if e['slug'] == slug), None)
    if event is None:
        abort(404)

    form = RegistrationForm()
    if form.validate_on_submit():
        if len(event['attendees']) >= event['max_attendees']:
            flash("Este evento ya alcanzó el número máximo de asistentes.")
        else:
            attendee = {
                'name': form.name.data,
                'email': form.email.data
            }
            event['attendees'].append(attendee)
            flash("Registro exitoso.")
            return redirect(url_for('event_detail', slug=slug))

    return render_template("register.html", event=event, form=form)


@app.route("/admin/event/", methods=["GET", "POST"])
def create_event():
    form = EventForm()
    form.category.choices = [(c, c) for c in categories]

    if form.validate_on_submit():
        new_event = {
            'id': len(events) + 1,
            'title': form.title.data,
            'slug': form.slug.data,
            'description': form.description.data,
            'date': form.date.data.strftime("%Y-%m-%d"),
            'time': form.time.data.strftime("%H:%M"),
            'location': form.location.data,
            'category': form.category.data,
            'max_attendees': form.max_attendees.data,
            'attendees': [],
            'featured': form.featured.data
        }
        events.append(new_event)
        flash("Evento creado exitosamente.")
        return redirect(url_for('index'))

    return render_template("create_event.html", form=form)

@app.route("/events/category/<category>/")
def events_by_category(category):
    filtered_events = [e for e in events if e['category'].lower() == category.lower()]
    if not filtered_events:
        flash("No hay eventos en esta categoría.")
    return render_template("category_events.html", events=filtered_events, category=category)
