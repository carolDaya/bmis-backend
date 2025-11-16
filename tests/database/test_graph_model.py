import pytest
from sqlalchemy.exc import IntegrityError
from database.models.graph_config import GraphConfig
from database.models.sensor import Sensor
from datetime import datetime
import time

class TestGraphConfigModel:
    """Pruebas del modelo GraphConfig"""

    def test_crear_configuracion_grafica_basica(self, session):
        sensor = Sensor(nombre="temperatura", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        graph_config = GraphConfig(
            sensor_id=sensor.id,
            tipo_grafica="linea"
        )
        session.add(graph_config)
        session.commit()

        assert graph_config.id is not None
        assert graph_config.sensor_id == sensor.id
        assert graph_config.tipo_grafica == "linea"
        assert graph_config.fecha_modificacion is not None

    def test_relacion_con_sensor(self, session):
        sensor = Sensor(nombre="ph", tipo="ph", unidad="pH")
        session.add(sensor)
        session.commit()

        graph_config = GraphConfig(
            sensor_id=sensor.id,
            tipo_grafica="barra"
        )
        session.add(graph_config)
        session.commit()

        # Verificar la relación
        assert graph_config.sensor.id == sensor.id
        assert graph_config.sensor.nombre == "ph"
        assert sensor.grafica_config.tipo_grafica == "barra"

    def test_sensor_id_unico(self, session):
        sensor = Sensor(nombre="temperatura", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        config1 = GraphConfig(sensor_id=sensor.id, tipo_grafica="linea")
        session.add(config1)
        session.commit()

        config2 = GraphConfig(sensor_id=sensor.id, tipo_grafica="barra")
        session.add(config2)

        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    def test_sensor_id_no_nulo(self, session):
        graph_config = GraphConfig(tipo_grafica="linea")
        
        session.add(graph_config)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    def test_tipo_grafica_no_nulo(self, session):
        sensor = Sensor(nombre="temperatura", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        graph_config = GraphConfig(sensor_id=sensor.id, tipo_grafica=None)
        
        session.add(graph_config)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    def test_fecha_modificacion_auto_actualizacion(self, session):
        sensor = Sensor(nombre="temperatura", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        graph_config = GraphConfig(sensor_id=sensor.id, tipo_grafica="linea")
        session.add(graph_config)
        session.commit()

        fecha_original = graph_config.fecha_modificacion
        
        # Forzar una diferencia de tiempo significativa
        time.sleep(1)  # Esperar 1 segundo completo

        # Modificar la configuración
        graph_config.tipo_grafica = "barra"
        session.commit()

        # Recargar el objeto desde la base de datos
        session.refresh(graph_config)
        
        # Verificar que la fecha se actualizó
        assert graph_config.fecha_modificacion != fecha_original
        assert graph_config.fecha_modificacion >= fecha_original

    def test_fecha_modificacion_se_establece_al_crear(self, session):
        """Test alternativo: verificar que la fecha se establece al crear"""
        sensor = Sensor(nombre="temperatura", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        graph_config = GraphConfig(sensor_id=sensor.id, tipo_grafica="linea")
        
        # Antes de commit, la fecha debería ser None (si no hay default en el modelo)
        # o tener un valor si el default se aplica antes del commit
        session.add(graph_config)
        session.commit()

        assert graph_config.fecha_modificacion is not None
        assert isinstance(graph_config.fecha_modificacion, datetime)

    def test_eliminar_configuracion(self, session):
        sensor = Sensor(nombre="temperatura", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        graph_config = GraphConfig(sensor_id=sensor.id, tipo_grafica="linea")
        session.add(graph_config)
        session.commit()

        config_id = graph_config.id
        session.delete(graph_config)
        session.commit()

        config_eliminada = session.get(GraphConfig, config_id)
        assert config_eliminada is None

    def test_configuraciones_multiples_sensores(self, session):
        sensor1 = Sensor(nombre="temp", tipo="temperatura", unidad="°C")
        sensor2 = Sensor(nombre="ph", tipo="ph", unidad="pH")
        session.add_all([sensor1, sensor2])
        session.commit()

        config1 = GraphConfig(sensor_id=sensor1.id, tipo_grafica="linea")
        config2 = GraphConfig(sensor_id=sensor2.id, tipo_grafica="barra")
        session.add_all([config1, config2])
        session.commit()

        configs = session.query(GraphConfig).all()
        assert len(configs) == 2
        assert {c.tipo_grafica for c in configs} == {"linea", "barra"}