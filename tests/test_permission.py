import pytest

from app import app as flask_app, bcrypt
from models import Job, User, db


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


def create_user(username, email):
    user = User(
        username=username,
        email=email,
        password=bcrypt.generate_password_hash('password123').decode('utf-8'),
    )
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email):
    return client.post(
        '/login',
        data={'email': email, 'password': 'password123'},
        follow_redirects=False,
    )


def test_user_cannot_edit_or_delete_another_users_job(client, app):
    with app.app_context():
        owner = create_user('owner', 'owner@example.com')
        intruder = create_user('intruder', 'intruder@example.com')
        job = Job(
            title='Python Developer',
            summary='Build reliable Flask applications.',
            description='Develop and maintain a production Flask application with a team.',
            company='Acme',
            salary='3000 GEL',
            location='Tbilisi',
            category='IT',
            author_id=owner.id,
        )

        db.session.add(job)
        db.session.commit()
        job_id = job.id

        assert owner.id != intruder.id

    login(client, 'intruder@example.com')

    assert client.get(f'/jobs/{job_id}/edit').status_code == 403
    assert client.post(f'/jobs/{job_id}/delete').status_code == 403

    with app.app_context():
        assert db.session.get(Job, job_id) is not None


def test_authenticated_user_can_create_own_job(client, app):
    with app.app_context():
        user = create_user('author', 'author@example.com')
        user_id = user.id

    login(client, 'author@example.com')
    response = client.post(
        '/jobs/new',
        data={
            'title': 'Backend Developer',
            'summary': 'Create and maintain reliable backend services.',
            'description': 'Build, test, and maintain backend services for our platform.',
            'company': 'Example Company',
            'salary': '4000 GEL',
            'location': 'Tbilisi',
            'category': 'IT',
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    with app.app_context():
        job = Job.query.filter_by(title='Backend Developer').one()
        assert job.author_id == user_id
