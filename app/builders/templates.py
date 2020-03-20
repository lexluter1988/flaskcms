init = '''from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
'''

flaskenv = '''FLASK_APP=<app_name>.py
FLASK_DEBUG=1
FLASK_ENV=development
'''

shell_context = '''from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, }
'''

config = '''import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''

requirements = '''alembic==1.4.0
Click==7.0
decorator==4.4.1
Flask==1.1.1
Flask-Login==0.5.0
Flask-Migrate==2.5.2
Flask-SQLAlchemy==2.4.1
itsdangerous==1.1.0
Jinja2==2.11.1
Mako==1.1.1
MarkupSafe==1.1.1
pbr==5.4.4
python-dateutil==2.8.1
python-dotenv==0.11.0
python-editor==1.0.4
six==1.14.0
SQLAlchemy==1.3.13
sqlparse==0.3.0
Tempita==0.5.2
Werkzeug==1.0.0
'''

gitignore = '''*.idea
*.pyc
__pycache__
'''

base_html = '''<html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

        <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

    </head>
    {% block content %}
    <p>Hello World!</p>
        {% block app_content %}
        {% endblock %}
    {% endblock %}
</html>
'''


readme = '''Hello friend!
'''


blueprint_init = '''from flask import Blueprint

bp = Blueprint('<package>', __name__)

from app.<package> import routes
'''

blueprint_route = '''from app.<package> import bp
'''

app_init = '''from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    <blueprints>    
    return app
'''

blueprint = '''
    from app.<package> import bp as <package>_bp
    app.register_blueprint(<package>_bp)
'''


quick_script = '''#!/bin/bash
virtualenv  -p /usr/bin/python3.6 env
source env/bin/activate
pip install -r requirements.txt
'''