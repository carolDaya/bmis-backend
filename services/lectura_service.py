from database.models.lectura import Lectura
from database.connection import db
from datetime import datetime

def registrar_lectura(sensor_id, valor, observaciones=None):
    """
    Registra una nueva lectura para un sensor.
    """
    lectura = Lectura(
        sensor_id=sensor_id,
        valor=valor,
        observaciones=observaciones,
        fecha_hora=datetime.now()   
    )

    db.session.add(lectura)
    db.session.commit()
    return lectura


def obtener_lecturas():
    """
    Retorna todas las lecturas registradas.
    """
    return Lectura.query.order_by(Lectura.fecha_hora.desc()).all()


def obtener_lecturas_por_sensor(sensor_id, limite=None):
    """
    Retorna las lecturas de un sensor específico.
    """
    query = Lectura.query.filter_by(sensor_id=sensor_id).order_by(Lectura.fecha_hora.desc())
    if limite:
        query = query.limit(limite)
    return query.all()


def eliminar_lecturas_sensor(sensor_id):
    """
    Elimina todas las lecturas asociadas a un sensor (por mantenimiento).
    """
    Lectura.query.filter_by(sensor_id=sensor_id).delete()
    db.session.commit()
