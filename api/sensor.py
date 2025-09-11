from flask import Blueprint, jsonify
from models.sensor import Sensor
from models.lectura import Lectura

sensors_bp = Blueprint("sensors", __name__)

# Listar todos los sensores
@sensors_bp.route("/sensors", methods=["GET"])
def listar_sensores():
    sensores = Sensor.query.all()
    result = [{"id": s.id, "nombre": s.nombre, "tipo": s.tipo, "unidad": s.unidad} for s in sensores]
    return jsonify(result), 200

# Listar lecturas de un sensor específico
@sensors_bp.route("/lecturas/<int:sensor_id>", methods=["GET"])
def listar_lecturas(sensor_id):
    lecturas = Lectura.query.filter_by(sensor_id=sensor_id).all()
    result = [{
        "sensor_id": sensor_id,                  # Aquí agregas el ID del sensor
        "fecha_hora": l.fecha_hora.isoformat(),  # Fecha en formato ISO
        "valor": l.valor                          # Valor del sensor
    } for l in lecturas]
    return jsonify(result), 200

