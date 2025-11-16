"""
Pruebas Unitarias para Voice Service
Ejecutar: pytest tests/unit/test_voice_service.py -v
"""
import pytest
from unittest.mock import Mock, patch
from services.voice_service import VoiceService
from exceptions.custom_exceptions import ValidationException, DatabaseException


class TestVoiceService:
    """Pruebas para Voice Service"""

    @patch('services.voice_service.VoiceConfig')
    def test_obtener_configuracion_existente(self, MockVoiceConfig):
        """Test: Obtener configuración existente"""
        mock_config = Mock()
        MockVoiceConfig.query.get.return_value = mock_config
        
        config = VoiceService.obtener_configuracion()
        
        assert config == mock_config
        MockVoiceConfig.query.get.assert_called_once_with(1)

    @patch('services.voice_service.VoiceConfig')
    def test_obtener_configuracion_por_defecto(self, MockVoiceConfig):
        """Test: Obtener configuración por defecto cuando no existe"""
        MockVoiceConfig.query.get.return_value = None
        mock_default = Mock()
        MockVoiceConfig.return_value = mock_default
        
        config = VoiceService.obtener_configuracion()
        
        assert config == mock_default
        MockVoiceConfig.assert_called_once()

    @patch('services.voice_service.VoiceConfig')
    @patch('services.voice_service.db.session')
    def test_guardar_configuracion_nueva(self, mock_session, MockVoiceConfig):
        """Test: Guardar nueva configuración"""
        # CORREGIDO: Configurar VALID_GENDERS en el mock
        MockVoiceConfig.VALID_GENDERS = ('FEMALE', 'MALE', 'ROBOTIC')
        MockVoiceConfig.query.get.return_value = None
        mock_config = Mock()
        MockVoiceConfig.return_value = mock_config
        
        config = VoiceService.guardar_configuracion("FEMALE", 1.0)
        
        assert config == mock_config
        mock_session.add.assert_called_once_with(mock_config)
        mock_session.commit.assert_called_once()

    @patch('services.voice_service.VoiceConfig')
    @patch('services.voice_service.db.session')
    def test_guardar_configuracion_actualizar(self, mock_session, MockVoiceConfig):
        """Test: Actualizar configuración existente"""
        # CORREGIDO: Configurar VALID_GENDERS en el mock
        MockVoiceConfig.VALID_GENDERS = ('FEMALE', 'MALE', 'ROBOTIC')
        mock_config = Mock()
        MockVoiceConfig.query.get.return_value = mock_config
        
        config = VoiceService.guardar_configuracion("MALE", 1.5)
        
        assert config == mock_config
        assert mock_config.voice_gender == "MALE"
        assert mock_config.voice_pitch == 1.5
        mock_session.commit.assert_called_once()

    def test_guardar_configuracion_genero_invalido(self):
        """Test: Error con género de voz inválido"""
        # CORREGIDO: Usar patch para configurar VALID_GENDERS
        with patch('services.voice_service.VoiceConfig.VALID_GENDERS', ('FEMALE', 'MALE', 'ROBOTIC')):
            with pytest.raises(ValidationException) as exc_info:
                VoiceService.guardar_configuracion("INVALID", 1.0)
            
            assert "voice_gender inválido" in str(exc_info.value.message)

    def test_guardar_configuracion_pitch_invalido(self):
        """Test: Error con pitch de voz inválido"""
        with patch('services.voice_service.VoiceConfig.VALID_GENDERS', ('FEMALE', 'MALE', 'ROBOTIC')):
            with pytest.raises(ValidationException) as exc_info:
                VoiceService.guardar_configuracion("FEMALE", "not_a_number")
            
            assert "voice_pitch debe ser un número válido" in str(exc_info.value.message)

    def test_guardar_configuracion_pitch_fuera_de_rango(self):
        """Test: Error con pitch fuera de rango"""
        with patch('services.voice_service.VoiceConfig.VALID_GENDERS', ('FEMALE', 'MALE', 'ROBOTIC')):
            with pytest.raises(ValidationException) as exc_info:
                VoiceService.guardar_configuracion("FEMALE", 0.1)
            
            assert "voice_pitch debe estar entre 0.5 y 2.0" in str(exc_info.value.message)

    def test_guardar_configuracion_campos_vacios(self):
        """Test: Error con campos vacíos"""
        with patch('services.voice_service.VoiceConfig.VALID_GENDERS', ('FEMALE', 'MALE', 'ROBOTIC')):
            with pytest.raises(ValidationException) as exc_info:
                VoiceService.guardar_configuracion("", 1.0)
            
            assert "obligatorios" in str(exc_info.value.message)

    @patch('services.voice_service.VoiceConfig')
    @patch('services.voice_service.db.session')
    def test_guardar_configuracion_error_base_datos(self, mock_session, MockVoiceConfig):
        """Test: Error de base de datos al guardar configuración"""
        # CORREGIDO: Configurar VALID_GENDERS
        MockVoiceConfig.VALID_GENDERS = ('FEMALE', 'MALE', 'ROBOTIC')
        MockVoiceConfig.query.get.return_value = None
        MockVoiceConfig.return_value = Mock()
        
        # Simular error en commit
        mock_session.commit.side_effect = Exception("DB error")
        
        with pytest.raises(DatabaseException) as exc_info:
            VoiceService.guardar_configuracion("FEMALE", 1.0)
        
        assert "Error al guardar la configuración de voz" in str(exc_info.value.message)
        mock_session.rollback.assert_called_once()