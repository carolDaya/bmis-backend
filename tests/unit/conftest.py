"""
Fixtures comunes para pruebas unitarias
"""
import pytest
from unittest.mock import Mock, patch
from flask import Flask
from database.connection import db


@pytest.fixture
def app():
    """Crear aplicación Flask para tests"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        yield app


@pytest.fixture
def mock_db_session():
    """Mock de la sesión de base de datos"""
    with patch('database.connection.db.session') as mock_session:
        yield mock_session


@pytest.fixture
def mock_user():
    """Mock de un usuario válido"""
    user = Mock()
    user.id = 1
    user.nombre = "Juan Pérez"
    user.telefono = "3001234567"
    user.conectado = False
    user.estado = "activo"
    user.check_password = Mock(return_value=True)
    user.set_password = Mock()
    user.to_dict = Mock(return_value={
        "id": 1,
        "nombre": "Juan Pérez",
        "telefono": "3001234567"
    })
    return user


@pytest.fixture
def mock_sensor():
    """Mock de un sensor válido"""
    sensor = Mock()
    sensor.id = 1
    sensor.nombre = "temperatura"
    sensor.tipo = "temperatura"
    sensor.unidad_medida = "°C"
    sensor.estado = "activo"
    sensor.to_dict = Mock(return_value={
        "id": 1,
        "nombre": "temperatura",
        "tipo": "temperatura",
        "unidad_medida": "°C"
    })
    return sensor


@pytest.fixture
def mock_proceso():
    """Mock de un proceso activo"""
    proceso = Mock()
    proceso.id = 1
    proceso.estado = "ACTIVO"
    proceso.fecha_inicio = Mock()
    proceso.fecha_fin = None
    return proceso