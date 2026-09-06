import pytest

from app import app as flask_app, bcrypt
from models import Job, User, db


@pytest.fixture()
def app():
    flask_app.config.update(
        TESTING=True, WTF_CSRF_ENABLED=False, SQLALCHEMY_DATABASE_URI='sqlite://'
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


def create_user(email, username):
    user = User(
        username=username, email=email, password=bcrypt.generate_password_hash('password123').decode('utf-8')
    )

    db.session.add(user)
    db.session.commit()

    return user


def login(client, email):
    return client.post('/login', data={'email': email, 'password': 'password123'}, follow_redirects=False)


def test_public_routes_are_available(client):
    assert client.get('/').status_code == 200
    assert client.get('/about').status_code == 200
    assert client.get('/missing-page').status_code == 404


def test_login_authenticates_registered_user(client, app):
    with app.app_context():
        create_user('member@example.com', 'member')

    response = login(client, 'member@example.com')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')

    with client.session_transaction() as session:
        assert '_user_id' in session


def test_cannot_edit_or_delete_another_users_job(client, app):
    with app.app_context():
        owner = create_user('owner@example.com', 'owner')
        intruder = create_user('intruder@example.com', 'intruder')
        job = Job(
            title='Python Developer', summary='Build reliable Flask applications.',
            description='Develop and maintain a production Flask application with a collaborative team.',
            company='Acme', salary='3000 GEL', location='Tbilisi', category='IT', author_id=owner.id,
        )

        db.session.add(job)
        db.session.commit()
        job_id = job.id

        assert intruder.id != owner.id

    login(client, 'intruder@example.com')
    assert client.get(f'/jobs/{job_id}/edit').status_code == 403
    assert client.post(f'/jobs/{job_id}/delete').status_code == 403

    with app.app_context():
        assert db.session.get(Job, job_id) is not None