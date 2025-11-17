import pytest
from database.models.lectura import Lectura
from database.models.sensor import Sensor
from database.models.proceso_biodigestor import ProcesoBiodigestor

class TestLecturaModel:
    """Pruebas del modelo Lectura"""

    def test_crear_lectura_basica(self, session):
        sensor = Sensor(nombre="temp", tipo="temperatura", unidad="°C")
        proceso = ProcesoBiodigestor(estado='ACTIVO')
        session.add_all([sensor, proceso])
        session.commit()

        lectura = Lectura(
            sensor_id=sensor.id,
            proceso_id=proceso.id,
            valor=35.5,
            observaciones="Normal"
        )
        session.add(lectura)
        session.commit()

        assert lectura.id is not None
        assert lectura.valor == 35.5
        assert lectura.fecha_hora is not None

    def test_validacion_valor_no_nulo(self):
        lectura = Lectura()
        with pytest.raises(ValueError) as exc_info:
            lectura.valor = None  # Esto activará el validador
        assert "El valor de la lectura no puede ser nulo" in str(exc_info.value)

    def test_validacion_valor_numerico(self):
        lectura = Lectura()
        with pytest.raises(ValueError) as exc_info:
            lectura.valor = "invalid"  # Esto activará el validador
        assert "El valor debe ser un número válido" in str(exc_info.value)

    def test_to_dict_serializa_correctamente(self, session):
        sensor = Sensor(nombre="temp", tipo="temperatura", unidad="°C")
        proceso = ProcesoBiodigestor(estado='ACTIVO')
        session.add_all([sensor, proceso])
        session.commit()

        lectura = Lectura(
            sensor_id=sensor.id,
            proceso_id=proceso.id,
            valor=35.5
        )
        session.add(lectura)
        session.commit()

        lectura_dict = lectura.to_dict()

        assert lectura_dict['sensor_id'] == sensor.id
        assert lectura_dict['proceso_id'] == proceso.id
        assert lectura_dict['valor'] == 35.5
        assert 'fecha_hora' in lectura_dict
        assert 'observaciones' in lectura_dict

    def test_lectura_sin_proceso(self, session):
        sensor = Sensor(nombre="temp", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        lectura = Lectura(
            sensor_id=sensor.id,
            proceso_id=None,  # Lectura sin proceso asociado
            valor=25.0
        )
        session.add(lectura)
        session.commit()

        assert lectura.proceso_id is None
        assert lectura.valor == 25.0

    def test_lectura_con_observaciones(self, session):
        sensor = Sensor(nombre="temp", tipo="temperatura", unidad="°C")
        proceso = ProcesoBiodigestor(estado='ACTIVO')
        session.add_all([sensor, proceso])
        session.commit()

        observaciones = "Lectura fuera de rango normal"
        lectura = Lectura(
            sensor_id=sensor.id,
            proceso_id=proceso.id,
            valor=40.0,
            observaciones=observaciones
        )
        session.add(lectura)
        session.commit()

        assert lectura.observaciones == observaciones
        assert lectura.to_dict()['observaciones'] == observaciones

    def test_crear_lectura_valida(self, session):
        """Test para crear una lectura con datos válidos"""
        sensor = Sensor(nombre="ph", tipo="ph", unidad="pH")
        proceso = ProcesoBiodigestor(estado='ACTIVO')
        session.add_all([sensor, proceso])
        session.commit()

        lectura = Lectura(
            sensor_id=sensor.id,
            proceso_id=proceso.id,
            valor=7.2
        )
        
        session.add(lectura)
        session.commit()
        
        # Verificar que se creó correctamente
        lectura_db = session.query(Lectura).filter_by(sensor_id=sensor.id).first()
        assert lectura_db is not None
        assert lectura_db.valor == 7.2
        assert lectura_db.proceso_id == proceso.id