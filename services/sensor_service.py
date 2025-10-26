from database.models.sensor import Sensor
from database.connection import db

def crear_sensor(nombre, tipo, unidad):
    if Sensor.query.filter_by(nombre=nombre).first():
        return None, "Ya existe un sensor con ese nombre"

    sensor = Sensor(nombre=nombre, tipo=tipo, unidad=unidad)
    db.session.add(sensor)
    db.session.commit()
    return sensor, None

def obtener_sensores():
    return Sensor.query.all()

def obtener_sensor_por_id(sensor_id):
    return Sensor.query.get(sensor_id)

def actualizar_sensor(sensor_id, nombre=None, tipo=None, unidad=None, activo=None):
    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return None, "Sensor no encontrado"

    if nombre: sensor.nombre = nombre
    if tipo: sensor.tipo = tipo
    if unidad: sensor.unidad = unidad
    if activo is not None: sensor.activo = activo

    db.session.commit()
    return sensor, None

def eliminar_sensor(sensor_id):
    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return None, "Sensor no encontrado"

    sensor.activo = False
    db.session.commit()
    return sensor, None
