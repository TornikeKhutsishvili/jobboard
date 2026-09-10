import pytest

from app import app as flask_app, bcrypt
from models import User, db


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


def create_user():
    user = User(
        username='testuser',
        email='test@example.com',
        password=bcrypt.generate_password_hash('password123').decode('utf-8'),
    )

    db.session.add(user)
    db.session.commit()


def test_registration_creates_user(client, app):
    response = client.post(
        '/register',
        data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        },
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')

    with app.app_context():
        user = User.query.filter_by(email='newuser@example.com').first()

        assert user is not None
        assert user.username == 'newuser'
        assert user.image_file == 'default.png'


def test_login_authenticates_user_with_valid_credentials(client, app):
    with app.app_context():
        create_user()

    response = client.post(
        '/login',
        data={'email': 'test@example.com', 'password': 'password123'},
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')

    with client.session_transaction() as session:
        assert '_user_id' in session


def test_login_rejects_invalid_password(client, app):
    with app.app_context():
        create_user()

    response = client.post(
        '/login',
        data={'email': 'test@example.com', 'password': 'wrong-password'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert 'ელფოსტა ან პაროლი არასწორია.'.encode('utf-8') in response.data

    with client.session_transaction() as session:
        assert '_user_id' not in session