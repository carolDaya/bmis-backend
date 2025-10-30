from flask import Blueprint, request, jsonify
from services.sensor_service import (
    crear_sensor, obtener_sensores, obtener_sensor_por_id,
    actualizar_sensor, eliminar_sensor
)

sensors_bp = Blueprint("sensor", __name__)

@sensors_bp.route("/sensores", methods=["POST"])
def create_sensor():
    data = request.json
    nombre = data.get("nombre")
    tipo = data.get("tipo")
    unidad = data.get("unidad")

    if not nombre or not tipo or not unidad:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    sensor, error = crear_sensor(nombre, tipo, unidad)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "Sensor creado exitosamente",
        "id": sensor.id,
        "nombre": sensor.nombre,
        "tipo": sensor.tipo,
        "unidad": sensor.unidad
    }), 201


@sensors_bp.route("/sensores", methods=["GET"])
def get_sensors():
    sensores = obtener_sensores()
    result = [{"id": s.id, "nombre": s.nombre, "tipo": s.tipo, "unidad": s.unidad} for s in sensores]
    return jsonify(result), 200

@sensors_bp.route("/sensores/<int:id>", methods=["PUT"])
def update_sensor(id):
    data = request.json
    nombre = data.get("nombre")
    tipo = data.get("tipo")
    unidad = data.get("unidad")

    sensor, error = actualizar_sensor(id, nombre, tipo, unidad)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "Sensor actualizado exitosamente",
        "id": sensor.id,
        "nombre": sensor.nombre,
        "tipo": sensor.tipo,
        "unidad": sensor.unidad
    }), 200
