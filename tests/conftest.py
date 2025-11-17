
"""
Configuración compartida para todos los tests
"""
import pytest
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fixtures globales
@pytest.fixture(scope='session')
def app():
    """Aplicación Flask para tests"""
    from main import create_app
    from database.connection import db
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Cliente de test"""
    return app.test_client()

@pytest.fixture(scope='function')
def session(app):
    """Sesión de BD para tests"""
    from database.connection import db
    with app.app_context():
        yield db.session
        db.session.rollback()