import pytest
from database.connection import db
from main import create_app

@pytest.fixture(scope='function')
def app():
    """Fixture: Aplicación con BD de prueba"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def session(app):
    """Fixture: Sesión de BD"""
    with app.app_context():
        yield db.session
