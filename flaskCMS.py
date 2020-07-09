from app import create_app, db
from app.models import User, Project, Event

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Project': Project, 'Event': Event}


@app.cli.command('bootstrap')
def bootstrap():
    db.create_all()

    u = User(username='admin', email='admin@example.com', confirmed=True)
    u.set_password('1q2w3e')

    db.session.add(u)
    db.session.commit()
