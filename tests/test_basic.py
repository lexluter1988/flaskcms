import os

import pytest


from app import create_app, db
from app.models import User
from config import basedir


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='module')
def client():
    app = create_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    client = app.test_client()

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URL') \
                                            or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    db.create_all()

    u = User(username='admin', email='admin@example.com', confirmed=True)
    u.set_password('1q2w3e')

    db.session.add(u)
    db.session.commit()

    yield client
    db.session.remove()
    db.drop_all()
    os.remove(os.path.join(basedir, 'data-test.sqlite'))
    ctx.pop()


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_feedback_page(client):
    response = client.get('/feedback')
    assert b'Submit your feedback' in response.data
    assert response.status_code == 200

