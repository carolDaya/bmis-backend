from datetime import datetime
from database.models.proceso_biodigestor import ProcesoBiodigestor
from database.models.sensor import Sensor
from database.models.lectura import Lectura

class TestProcesoBiodigestorModel:
    """Pruebas del modelo ProcesoBiodigestor"""

    def test_crear_proceso_activo(self, session):
        proceso = ProcesoBiodigestor(estado="ACTIVO")

        session.add(proceso)
        session.commit()

        assert proceso.id is not None
        assert proceso.estado == "ACTIVO"
        assert proceso.fecha_inicio is not None
        assert proceso.fecha_fin is None

    def test_finalizar_proceso(self, session):
        proceso = ProcesoBiodigestor(estado="ACTIVO")
        session.add(proceso)
        session.commit()

        proceso.estado = "FINALIZADO"
        proceso.fecha_fin = datetime.now()
        session.commit()

        assert proceso.estado == "FINALIZADO"
        assert proceso.fecha_fin is not None

    def test_relacion_con_lecturas(self, session):
        sensor = Sensor(nombre="temp", tipo="temperatura", unidad="°C")
        session.add(sensor)
        session.commit()

        proceso = ProcesoBiodigestor(estado="ACTIVO")
        session.add(proceso)
        session.commit()

        lectura = Lectura(
            sensor_id=sensor.id,
            proceso_id=proceso.id,
            valor=35.5
        )
        session.add(lectura)
        session.commit()

        assert len(proceso.lecturas) == 1
        assert proceso.lecturas[0].valor == 35.5
