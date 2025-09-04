# src/eventos_app/data.py

events = [
    {
        'id': 1,
        'title': 'Conferencia de Python',
        'slug': 'conferencia-python',
        'description': 'Descripción del evento...',
        'date': '2025-09-15',
        'time': '14:00',
        'location': 'Auditorio Principal',
        'category': 'Tecnología',
        'max_attendees': 50,
        'attendees': [],
        'featured': True
    }
,
    {
        'id': 2,
        'title': 'Festival de Cine Independiente',
        'slug': 'festival-cine-independiente',
        'description': 'Una muestra de cine alternativo y cultural.',
        'date': '2025-09-20',
        'time': '18:00',
        'location': 'Teatro Municipal',
        'category': 'Cultural',
        'max_attendees': 120,
        'attendees': [],
        'featured': False
    },
    {
        'id': 3,
        'title': 'Congreso de Educación Superior',
        'slug': 'congreso-educacion-superior',
        'description': 'Encuentro académico sobre innovación educativa.',
        'date': '2025-09-25',
        'time': '09:00',
        'location': 'Centro de Convenciones',
        'category': 'Académico',
        'max_attendees': 200,
        'attendees': [],
        'featured': True
    },
    {
        'id': 4,
        'title': 'Torneo de Fútbol Universitario',
        'slug': 'torneo-futbol-universitario',
        'description': 'Competencia deportiva entre facultades.',
        'date': '2025-09-30',
        'time': '16:00',
        'location': 'Cancha Deportiva UTP',
        'category': 'Deportivo',
        'max_attendees': 300,
        'attendees': [],
        'featured': False
    },
    {
        'id': 5,
        'title': 'Fiesta de Integración Estudiantil',
        'slug': 'fiesta-integracion-estudiantil',
        'description': 'Evento social para fortalecer la comunidad estudiantil.',
        'date': '2025-10-05',
        'time': '20:00',
        'location': 'Zona Verde Campus',
        'category': 'Social',
        'max_attendees': 150,
        'attendees': [],
        'featured': True
    }

]

categories = ['Tecnología', 'Académico', 'Cultural', 'Deportivo', 'Social']
