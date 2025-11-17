"""
Pruebas Unitarias para Sensor Service
Ejecutar: pytest tests/unit/test_sensor_service.py -v
"""
import pytest
from unittest.mock import Mock, patch
from services.sensor_service import crear_sensor, obtener_sensores, obtener_sensor_por_id
from exceptions.custom_exceptions import ValidationException, DatabaseException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class TestSensorService:
    """Pruebas para Sensor Service"""
    
    @patch('services.sensor_service.Sensor')
    @patch('services.sensor_service.db.session')
    def test_crear_sensor_exitoso(self, mock_session, MockSensor):
        """Test: Crear sensor con datos válidos"""
        # Configurar mocks
        MockSensor.query.filter_by.return_value.first.return_value = None
        mock_sensor = Mock()
        mock_sensor.id = 1
        MockSensor.return_value = mock_sensor
        
        # Ejecutar
        sensor = crear_sensor("temperatura", "temperatura", "°C")
        
        # Verificar
        assert sensor is not None
        mock_session.add.assert_called_once_with(mock_sensor)
        mock_session.commit.assert_called_once()
    
    @patch('services.sensor_service.Sensor')
    def test_crear_sensor_nombre_duplicado(self, MockSensor):
        """Test: Error al crear sensor con nombre duplicado"""
        # Simular que ya existe un sensor con ese nombre
        MockSensor.query.filter_by.return_value.first.return_value = Mock()
        
        with pytest.raises(ValidationException) as exc_info:
            crear_sensor("temperatura", "temperatura", "°C")
        
        assert "Ya existe un sensor con el nombre 'temperatura'" in str(exc_info.value.message)
    
    @patch('services.sensor_service.Sensor')
    def test_obtener_sensores_lista_vacia(self, MockSensor):
        """Test: Obtener sensores cuando no hay ninguno"""
        MockSensor.query.all.return_value = []
        
        sensores = obtener_sensores()
        
        assert sensores == []
    
    @patch('services.sensor_service.Sensor')
    def test_obtener_sensores_con_datos(self, MockSensor):
        """Test: Obtener lista de sensores"""
        # Crear mocks de sensores con el método to_dict
        mock_sensor1 = Mock()
        mock_sensor1.to_dict.return_value = {'id': 1, 'nombre': 'Temp'}
        
        mock_sensor2 = Mock()
        mock_sensor2.to_dict.return_value = {'id': 2, 'nombre': 'PH'}
        
        mock_sensores = [mock_sensor1, mock_sensor2]
        MockSensor.query.all.return_value = mock_sensores
        
        sensores = obtener_sensores()
        
        # Verificar que se retornan los mocks correctamente
        assert len(sensores) == 2
        assert sensores[0] == mock_sensor1
        assert sensores[1] == mock_sensor2
    
    @patch('services.sensor_service.Sensor')
    def test_obtener_sensor_por_id_exitoso(self, MockSensor):
        """Test: Obtener sensor por ID existente"""
        # Configurar mock
        mock_sensor = Mock()
        mock_sensor.id = 1
        mock_sensor.nombre = "temperatura"
        MockSensor.query.get.return_value = mock_sensor
        
        # Ejecutar
        sensor = obtener_sensor_por_id(1)
        
        # Verificar
        assert sensor == mock_sensor
        MockSensor.query.get.assert_called_once_with(1)
    
    @patch('services.sensor_service.Sensor')
    def test_obtener_sensor_por_id_no_existe(self, MockSensor):
        """Test: Error al obtener sensor con ID inexistente"""
        # Simular que no se encuentra el sensor
        MockSensor.query.get.return_value = None
        
        with pytest.raises(ValidationException) as exc_info:
            obtener_sensor_por_id(999)
        
        assert "Sensor con ID 999 no encontrado" in str(exc_info.value.message)
    
    @patch('services.sensor_service.Sensor')
    @patch('services.sensor_service.db.session')
    def test_crear_sensor_error_integridad(self, mock_session, MockSensor):
        """Test: Error de integridad al crear sensor"""
        MockSensor.query.filter_by.return_value.first.return_value = None
        MockSensor.return_value = Mock()
        
        # CORREGIDO: Usar IntegrityError específico en lugar de Exception genérica
        mock_session.commit.side_effect = IntegrityError("Integrity error", None, None)
        
        with pytest.raises(DatabaseException) as exc_info:
            crear_sensor("temperatura", "temperatura", "°C")
        
        assert "Error de integridad al crear el sensor" in str(exc_info.value.message)
        mock_session.rollback.assert_called_once()
    
    @patch('services.sensor_service.Sensor')
    @patch('services.sensor_service.db.session')
    def test_crear_sensor_error_base_datos(self, mock_session, MockSensor):
        """Test: Error de base de datos al crear sensor"""
        MockSensor.query.filter_by.return_value.first.return_value = None
        MockSensor.return_value = Mock()
        
        # Simular error de SQLAlchemy
        mock_session.commit.side_effect = SQLAlchemyError("DB error")
        
        with pytest.raises(DatabaseException) as exc_info:
            crear_sensor("temperatura", "temperatura", "°C")
        
        assert "Error al guardar el sensor en la base de datos" in str(exc_info.value.message)
        mock_session.rollback.assert_called_once()
    
    @patch('services.sensor_service.Sensor')
    @patch('services.sensor_service.db.session')
    def test_crear_sensor_error_generico(self, mock_session, MockSensor):
        """Test: Error genérico inesperado al crear sensor"""
        MockSensor.query.filter_by.return_value.first.return_value = None
        MockSensor.return_value = Mock()
        
        # Simular error genérico
        mock_session.commit.side_effect = Exception("Unexpected error")
        
        with pytest.raises(DatabaseException) as exc_info:
            crear_sensor("temperatura", "temperatura", "°C")
        
        assert "Error inesperado: Unexpected error" in str(exc_info.value.message)
        mock_session.rollback.assert_called_once()