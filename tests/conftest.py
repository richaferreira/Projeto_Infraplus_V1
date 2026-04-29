import os
import tempfile

import pytest

os.environ['SECRET_KEY'] = 'test-secret-key'

from backend.app import create_app
from backend.app.extensions import db as _db
from backend.app.models import User


@pytest.fixture(scope='session')
def app():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
    application = create_app()
    application.config['TESTING'] = True
    application.config['WTF_CSRF_ENABLED'] = False
    yield application
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as c:
        yield c


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def auth_client(client, app):
    """Client logged in as admin."""
    with app.app_context():
        user = User.query.filter_by(email='admin@infra.plus').first()
        assert user is not None
    client.post('/login', data={
        'email': 'admin@infra.plus',
        'password': '123',
    }, follow_redirects=True)
    return client
