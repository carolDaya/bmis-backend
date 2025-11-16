from flask import Blueprint, request, jsonify
from services.lectura_service import (
    registrar_lectura, obtener_lecturas,
    obtener_lecturas_por_sensor, eliminar_lecturas_sensor
)
from exceptions.custom_exceptions import ValidationException

lectura_bp = Blueprint("lectura", __name__)

"""
Registra una nueva lectura para un sensor.
"""
@lectura_bp.post("/lecturas")
def create_lectura():
    data = request.json
    sensor_id = data.get("sensor_id")
    valor = data.get("valor")
    observaciones = data.get("observaciones")

    if not sensor_id or valor is None:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        lectura = registrar_lectura(sensor_id, valor, observaciones)
    except ValidationException as e:
        return jsonify({"error": str(e)}), e.status_code

    return jsonify({
        "message": "Lectura registrada exitosamente",
        "id": lectura.id,
        "sensor_id": lectura.sensor_id,
        "valor": lectura.valor,
        "fecha_hora": lectura.fecha_hora.isoformat(),
        "observaciones": lectura.observaciones
    }), 201


@lectura_bp.get("/lecturas")
def get_lecturas():
    """
    Agregada paginación para evitar memory overflow
    Query params: ?page=1&per_page=50
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Limitar máximo de registros por página
        per_page = min(per_page, 100)
        
        # Obtener lecturas paginadas
        from database.models.lectura import Lectura
        from sqlalchemy import desc
        
        pagination = Lectura.query.order_by(desc(Lectura.fecha_hora))\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        result = {
            "lecturas": [{
                "id": l.id,
                "sensor_id": l.sensor_id,
                "valor": l.valor,
                "fecha_hora": l.fecha_hora.isoformat(),
                "observaciones": l.observaciones
            } for l in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page,
            "per_page": per_page
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener lecturas: {e}"}), 500


@lectura_bp.get("/lecturas/<int:sensor_id>")
def get_lecturas_por_sensor_endpoint(sensor_id):
    """
    Obtiene las últimas lecturas de un sensor específico del PROCESO ACTIVO.
    Query param: ?limit=20 (default: 20, max: 100)
    """
    try:
        limite = request.args.get('limit', 20, type=int)
        limite = min(limite, 100) #Máximo 100 registros
        
        lecturas = obtener_lecturas_por_sensor(sensor_id, limite=limite)
        
        if not lecturas:
            return jsonify([]), 200 
        
        result = [{
            "id": l.id,
            "sensor_id": l.sensor_id,
            "valor": l.valor,
            "fecha_hora": l.fecha_hora.isoformat(),
            "observaciones": l.observaciones
        } for l in lecturas]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener lecturas del sensor {sensor_id}: {e}"}), 500