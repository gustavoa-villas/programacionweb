#Gustavo Villa
#Jose Hidalgo

from flask import Flask, render_template, redirect, url_for, request
import uuid
from anuncios_app.forms import EventForm, RegistrationForm
from anuncios_app.data import events, categories



app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'

@app.route('/')
def index():
    upcoming_events = [e for e in events if e['featured']]
    return render_template('index.html', events=upcoming_events)

@app.route('/event/<slug>/')
def event_detail(slug):
    event = next((e for e in events if e['slug'] == slug), None)
    return render_template('event_detail.html', event=event)

@app.route('/admin/event/', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    form.category.choices = [(c, c) for c in categories]
    if form.validate_on_submit():
        new_event = {
            'id': uuid.uuid4().int,
            'title': form.title.data,
            'slug': form.title.data.lower().replace(' ', '-'),
            'description': form.description.data,
            'date': str(form.date.data),
            'time': str(form.time.data),
            'location': form.location.data,
            'category': form.category.data,
            'max_attendees': form.max_attendees.data,
            'attendees': [],
            'featured': form.featured.data == 'True'
        }
        events.append(new_event)
        return redirect(url_for('index'))
    return render_template('create_event.html', form=form)

@app.route('/event/<slug>/register/', methods=['GET', 'POST'])
def register_event(slug):
    event = next((e for e in events if e['slug'] == slug), None)
    form = RegistrationForm()
    if form.validate_on_submit():
        if len(event['attendees']) < event['max_attendees']:
            event['attendees'].append({
                'name': form.name.data,
                'email': form.email.data
            })
            return redirect(url_for('event_detail', slug=slug))
    return render_template('register_event.html', form=form, event=event)

@app.route('/events/category/<category>/')
def category_events(category):
    filtered = [e for e in events if e['category'] == category]
    return render_template('category_events.html', events=filtered, category=category)
