import pytest
from sqlalchemy.exc import IntegrityError
from database.models.sensor import Sensor

class TestSensorModel:
    """Pruebas del modelo Sensor"""

    def test_crear_sensor_basico(self, session):
        sensor = Sensor(nombre="temperatura", tipo="temperatura", unidad="°C")

        session.add(sensor)
        session.commit()

        assert sensor.id is not None
        assert sensor.nombre == "temperatura"

    def test_nombre_sensor_unique(self, session):
        sensor1 = Sensor(nombre="temperatura", tipo="temperatura", unidad="°C")
        session.add(sensor1)
        session.commit()

        sensor2 = Sensor(nombre="temperatura", tipo="otro", unidad="K")
        session.add(sensor2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_validacion_campos_vacios(self):
        with pytest.raises(ValueError):
            Sensor(nombre="", tipo="temperatura", unidad="°C")

        with pytest.raises(ValueError):
            Sensor(nombre="temp", tipo="", unidad="°C")

        with pytest.raises(ValueError):
            Sensor(nombre="temp", tipo="temperatura", unidad="")

    def test_to_dict_serializa_correctamente(self, session):
        sensor = Sensor(nombre="presion", tipo="presion", unidad="kPa")
        session.add(sensor)
        session.commit()

        sensor_dict = sensor.to_dict()

        assert sensor_dict["nombre"] == "presion"
        assert sensor_dict["tipo"] == "presion"
        assert sensor_dict["unidad"] == "kPa"
        assert "id" in sensor_dict
