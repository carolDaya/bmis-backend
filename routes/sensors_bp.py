import logging
from flask import Blueprint, request, jsonify
from services.sensor_service import (
    crear_sensor, obtener_sensores, obtener_sensor_por_id
)
from utils.validators import require_json, validate_positive_number
from exceptions.custom_exceptions import (
    ValidationException
)
logger = logging.getLogger(__name__)
sensors_bp = Blueprint("sensor", __name__)

@sensors_bp.post("/sensores")
@require_json('nombre', 'tipo', 'unidad')
def create_sensor():
    """Crea sensor con validación automática"""
    data = request.json
    
    sensor = crear_sensor(
        nombre=data['nombre'],
        tipo=data['tipo'],
        unidad=data['unidad']
    )
    
    return jsonify({
        "message": "Sensor creado exitosamente",
        **sensor.to_dict()
    }), 201


@sensors_bp.get("/sensores")
def get_sensors():
    """Lista todos los sensores"""
    sensores = obtener_sensores()
    return jsonify([s.to_dict() for s in sensores]), 200


@sensors_bp.get("/sensores/<int:sensor_id>")
def get_sensor(sensor_id):
    """Obtiene un sensor por ID"""
    sensor = obtener_sensor_por_id(sensor_id)
    return jsonify(sensor.to_dict()), 200