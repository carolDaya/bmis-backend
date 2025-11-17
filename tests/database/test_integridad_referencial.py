import pytest
from sqlalchemy.exc import IntegrityError
from database.models.sensor import Sensor
from database.models.lectura import Lectura
from database.models.proceso_biodigestor import ProcesoBiodigestor

class TestIntegridadReferencial:
    """Pruebas de integridad referencial"""

    def test_lectura_requiere_sensor_valido(self, session):
        proceso = ProcesoBiodigestor(estado="ACTIVO")
        session.add(proceso)
        session.commit()

        lectura = Lectura(sensor_id=9999, proceso_id=proceso.id, valor=35.5)
        session.add(lectura)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_lectura_requiere_proceso_valido(self, session):
        sensor = Sensor(nombre="temp", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        lectura = Lectura(sensor_id=sensor.id, proceso_id=9999, valor=35.5)
        session.add(lectura)

        with pytest.raises(IntegrityError):
            session.commit()
