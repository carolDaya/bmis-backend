import pytest
from main import create_app
from database.connection import db
from database.models.sensor import Sensor
from database.models.proceso_biodigestor import ProcesoBiodigestor


@pytest.fixture
def app():
    """Crea la app en modo testing con DB en memoria"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Client de pruebas para hacer peticiones HTTP"""
    return app.test_client()


@pytest.fixture
def init_sensores(app):
    """Crea sensores por defecto"""
    with app.app_context():
        sensores = [
            Sensor(nombre="temperatura", tipo="temperatura", unidad="°C"),
            Sensor(nombre="presion", tipo="presion", unidad="kPa"),
            Sensor(nombre="gas", tipo="gas", unidad="ppm")
        ]
        for s in sensores:
            db.session.add(s)
        db.session.commit()
        return sensores


@pytest.fixture
def usuario_registrado(client):
    """Registra un usuario base para pruebas de login"""
    response = client.post("/auth/register", json={
        "nombre": "Test User",
        "telefono": "3001234567",
        "password": "testpass123",
        "confirm_password": "testpass123"
    })
    return response.get_json()


@pytest.fixture
def proceso_activo(app):
    """Crea un proceso ACTIVO en la BD"""
    with app.app_context():
        p = ProcesoBiodigestor(estado="ACTIVO")
        db.session.add(p)
        db.session.commit()
        return p
