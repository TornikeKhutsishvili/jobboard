import pytest

from app import app as flask_app
from config import Config
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


def test_config_attributes():
    assert Config.SECRET_KEY is not None
    assert isinstance(Config.SECRET_KEY, str)
    assert len(Config.SECRET_KEY) > 0
    assert Config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert Config.SQLALCHEMY_DATABASE_URI is not None


def test_app_testing_configuration(app):
    assert app.config['TESTING'] is True
    assert app.config['WTF_CSRF_ENABLED'] is False
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://'
