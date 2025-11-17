import pytest
from unittest.mock import patch, Mock
from services.graph_service import (
    guardar_o_actualizar_config,
    obtener_todas_configs,
    obtener_config_por_sensor
)
from database.models.graph_config import GraphConfig


class TestGraphService:

    @patch("services.graph_service.GraphConfig")
    @patch("services.graph_service.db.session")
    def test_guardar_configuracion_nueva(self, mock_session, MockGraphConfig):
        """Debe crear nueva configuración si no existe una para ese sensor."""
        MockGraphConfig.query.filter_by.return_value.first.return_value = None
        
        mock_config = Mock()
        MockGraphConfig.return_value = mock_config

        result = guardar_o_actualizar_config(1, "line")

        assert result == mock_config
        mock_session.add.assert_called_once_with(mock_config)
        mock_session.commit.assert_called_once()

    @patch("services.graph_service.GraphConfig")
    @patch("services.graph_service.db.session")
    def test_actualizar_configuracion_existente(self, mock_session, MockGraphConfig):
        """Debe actualizar una configuración existente."""
        mock_existing = Mock()
        MockGraphConfig.query.filter_by.return_value.first.return_value = mock_existing

        result = guardar_o_actualizar_config(5, "bar")

        assert result == mock_existing
        assert mock_existing.tipo_grafica == "bar"
        mock_session.commit.assert_called_once()

    @patch("services.graph_service.GraphConfig")
    @patch("services.graph_service.db.session")
    def test_error_guardar_configuracion(self, mock_session, MockGraphConfig):
        """Debe lanzar error y hacer rollback si ocurre una excepción al guardar."""
        MockGraphConfig.query.filter_by.return_value.first.return_value = None
        mock_session.commit.side_effect = Exception("DB Error")

        with pytest.raises(RuntimeError) as exc_info:
            guardar_o_actualizar_config(10, "area")

        assert "Error al guardar/actualizar configuración" in str(exc_info.value)
        mock_session.rollback.assert_called_once()

    @patch("services.graph_service.GraphConfig")
    def test_obtener_todas_configs(self, MockGraphConfig):
        """Debe retornar todas las configuraciones."""
        mock_data = [Mock(), Mock()]
        MockGraphConfig.query.all.return_value = mock_data

        result = obtener_todas_configs()

        assert result == mock_data
        MockGraphConfig.query.all.assert_called_once()

    @patch("services.graph_service.GraphConfig")
    def test_obtener_config_por_sensor(self, MockGraphConfig):
        """Debe retornar una configuración si existe."""
        mock_config = Mock()
        MockGraphConfig.query.filter_by.return_value.first.return_value = mock_config

        result = obtener_config_por_sensor(3)

        assert result == mock_config
        MockGraphConfig.query.filter_by.assert_called_once_with(sensor_id=3)

    @patch("services.graph_service.GraphConfig")
    def test_obtener_config_por_sensor_no_existe(self, MockGraphConfig):
        """Debe retornar None si no existe la configuración."""
        MockGraphConfig.query.filter_by.return_value.first.return_value = None

        result = obtener_config_por_sensor(99)

        assert result is None
        MockGraphConfig.query.filter_by.assert_called_once_with(sensor_id=99)
