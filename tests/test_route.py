import pytest

from app import app as flask_app
from models import db


@pytest.fixture()
def app():
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI='sqlite://'
    )
    with flask_app.app_context():
        db.drop_all()
        db.create_all()

        yield flask_app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_public_routes_are_available(client):
    assert client.get('/').status_code == 200
    assert client.get('/about').status_code == 200
    assert client.get('/jobs/9999').status_code == 404


def test_protected_routes_require_login(client):
    new_job_response = client.get('/jobs/new')
    profile_response = client.get('/profile')

    assert new_job_response.status_code == 302
    assert '/login' in new_job_response.headers['Location']
    assert profile_response.status_code == 302
    assert '/login' in profile_response.headers['Location']
