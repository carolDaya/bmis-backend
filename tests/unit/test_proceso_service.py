"""
Pruebas Unitarias para Proceso Service
Ejecutar: pytest tests/unit/test_proceso_service.py -v
"""
import pytest
from unittest.mock import Mock, patch
from services.proceso_service import (
    iniciar_proceso, 
    finalizar_proceso, 
    hay_proceso_activo,
    proceso_to_dict
)


class TestProcesoService:
    """Pruebas para Proceso Service"""
    
    @patch('services.proceso_service.ProcesoBiodigestor')
    @patch('services.proceso_service.db.session')
    def test_iniciar_proceso_exitoso(self, mock_session, MockProceso):
        """Test: Iniciar proceso cuando no hay uno activo"""
        # Configurar mocks
        with patch('services.proceso_service.obtener_proceso_activo', return_value=None):
            mock_nuevo = Mock()
            mock_nuevo.id = 1
            MockProceso.return_value = mock_nuevo
            
            # Ejecutar
            proceso = iniciar_proceso()
            
            # Verificar
            assert proceso is not None
            mock_session.add.assert_called_once_with(mock_nuevo)
            mock_session.commit.assert_called_once()
    
    @patch('services.proceso_service.obtener_proceso_activo')
    def test_iniciar_proceso_ya_existe_activo(self, mock_obtener_activo):
        """Test: Error al iniciar proceso cuando ya hay uno activo"""
        # Simular que ya existe un proceso activo
        mock_obtener_activo.return_value = Mock()
        
        with pytest.raises(RuntimeError) as exc_info:
            iniciar_proceso()
        
        assert "Ya existe un proceso activo" in str(exc_info.value)
    
    @patch('services.proceso_service.ProcesoBiodigestor')
    @patch('services.proceso_service.db.session')
    def test_finalizar_proceso_exitoso(self, mock_session, MockProceso, mock_proceso):
        """Test: Finalizar proceso activo correctamente"""
        # Configurar mocks
        with patch('services.proceso_service.obtener_proceso_activo', return_value=mock_proceso):
            # Mock para la consulta con bloqueo
            MockProceso.query.filter_by.return_value \
                .with_for_update.return_value \
                .first.return_value = mock_proceso
            
            # Ejecutar
            proceso = finalizar_proceso()
            
            # Verificar
            assert proceso.estado == "FINALIZADO"
            assert proceso.fecha_fin is not None
            mock_session.commit.assert_called_once()
    
    @patch('services.proceso_service.obtener_proceso_activo')
    def test_finalizar_proceso_sin_proceso_activo(self, mock_obtener_activo):
        """Test: Error al finalizar cuando no hay proceso activo"""
        # Simular que no hay proceso activo
        mock_obtener_activo.return_value = None
        
        with pytest.raises(RuntimeError) as exc_info:
            finalizar_proceso()
        
        assert "No hay procesos activos para finalizar" in str(exc_info.value)
    
    @patch('services.proceso_service.obtener_proceso_activo')
    def test_hay_proceso_activo_true(self, mock_obtener_activo):
        """Test: hay_proceso_activo retorna True cuando hay proceso activo"""
        mock_obtener_activo.return_value = Mock()
        
        resultado = hay_proceso_activo()
        
        assert resultado == True
    
    @patch('services.proceso_service.obtener_proceso_activo')
    def test_hay_proceso_activo_false(self, mock_obtener_activo):
        """Test: hay_proceso_activo retorna False cuando no hay proceso activo"""
        mock_obtener_activo.return_value = None
        
        resultado = hay_proceso_activo()
        
        assert resultado == False
    
    def test_proceso_to_dict_con_fechas(self):
        """Test: proceso_to_dict con fechas completas"""
        # Crear mock de proceso con fechas
        mock_proceso = Mock()
        mock_proceso.id = 1
        mock_proceso.estado = "ACTIVO"
        mock_proceso.fecha_inicio = Mock()
        mock_proceso.fecha_inicio.isoformat.return_value = "2023-01-01T10:00:00"
        mock_proceso.fecha_fin = Mock()
        mock_proceso.fecha_fin.isoformat.return_value = "2023-01-01T12:00:00"
        
        resultado = proceso_to_dict(mock_proceso)
        
        assert resultado == {
            "id": 1,
            "estado": "ACTIVO",
            "fecha_inicio": "2023-01-01T10:00:00",
            "fecha_fin": "2023-01-01T12:00:00"
        }
    
    def test_proceso_to_dict_sin_fecha_fin(self):
        """Test: proceso_to_dict sin fecha_fin"""
        # Crear mock de proceso sin fecha_fin
        mock_proceso = Mock()
        mock_proceso.id = 1
        mock_proceso.estado = "ACTIVO"
        mock_proceso.fecha_inicio = Mock()
        mock_proceso.fecha_inicio.isoformat.return_value = "2023-01-01T10:00:00"
        mock_proceso.fecha_fin = None
        
        resultado = proceso_to_dict(mock_proceso)
        
        assert resultado == {
            "id": 1,
            "estado": "ACTIVO",
            "fecha_inicio": "2023-01-01T10:00:00",
            "fecha_fin": None
        }
    
    @patch('services.proceso_service.ProcesoBiodigestor')
    @patch('services.proceso_service.db.session')
    def test_iniciar_proceso_error_base_datos(self, mock_session, MockProceso):
        """Test: Error de base de datos al iniciar proceso"""
        with patch('services.proceso_service.obtener_proceso_activo', return_value=None):
            MockProceso.return_value = Mock()
            
            # Simular error en commit
            mock_session.commit.side_effect = Exception("DB error")
            
            with pytest.raises(RuntimeError) as exc_info:
                iniciar_proceso()
            
            assert "Error al iniciar proceso" in str(exc_info.value)
            mock_session.rollback.assert_called_once()
    
    @patch('services.proceso_service.ProcesoBiodigestor')
    @patch('services.proceso_service.db.session')
    def test_finalizar_proceso_error_base_datos(self, mock_session, MockProceso, mock_proceso):
        """Test: Error de base de datos al finalizar proceso"""
        with patch('services.proceso_service.obtener_proceso_activo', return_value=mock_proceso):
            # Mock para la consulta con bloqueo
            MockProceso.query.filter_by.return_value \
                .with_for_update.return_value \
                .first.return_value = mock_proceso
            
            # Simular error en commit
            mock_session.commit.side_effect = Exception("DB error")
            
            with pytest.raises(RuntimeError) as exc_info:
                finalizar_proceso()
            
            assert "Error al finalizar proceso" in str(exc_info.value)
            mock_session.rollback.assert_called_once()