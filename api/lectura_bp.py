from flask import Blueprint, request, jsonify
from services.lectura_service import (
    registrar_lectura, obtener_lecturas,
    obtener_lecturas_por_sensor, eliminar_lecturas_sensor
)

lectura_bp = Blueprint("lectura", __name__)

@lectura_bp.route("/lecturas", methods=["POST"])
def create_lectura():
    data = request.json
    sensor_id = data.get("sensor_id")
    valor = data.get("valor")
    observaciones = data.get("observaciones")

    if not sensor_id or valor is None:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    lectura = registrar_lectura(sensor_id, valor, observaciones)
    return jsonify({
        "message": "Lectura registrada exitosamente",
        "id": lectura.id,
        "sensor_id": lectura.sensor_id,
        "valor": lectura.valor,
        "fecha_hora": lectura.fecha_hora,
        "observaciones": lectura.observaciones
    }), 201

@lectura_bp.route("/lecturas", methods=["GET"])
def get_lecturas():
    lecturas = obtener_lecturas()
    result = [{
        "id": l.id,
        "sensor_id": l.sensor_id,
        "valor": l.valor,
        "fecha_hora": l.fecha_hora,
        "observaciones": l.observaciones
    } for l in lecturas]
    return jsonify(result), 200
# ----------------------------------------------------------------------
# 3. GET /lecturas/<sensor_id>: Obtener lecturas por Sensor
# ----------------------------------------------------------------------
@lectura_bp.route("/lecturas/<int:sensor_id>", methods=["GET"])
def get_lecturas_por_sensor_endpoint(sensor_id):
    """
    Este endpoint se mapea a 'lecturaRepo.getLecturas(sensorId)' en Android.
    Retorna los datos históricos para dibujar la gráfica.
    """
    try:
        # Llama a tu función de servicio de DB (que soporta 'limite' si lo implementaste, 
        # pero aquí usamos la versión simple para obtener todas las relevantes)
        lecturas = obtener_lecturas_por_sensor(sensor_id, limite=20) # Ejemplo: limitar a las últimas 20
        
        # Si no hay lecturas, devolvemos una lista vacía con código 200.
        if not lecturas:
            return jsonify([]), 200 
            
        result = [{
            "id": l.id,
            "sensor_id": l.sensor_id,
            "valor": l.valor,
            # Formato crucial para el frontend
            "fecha_hora": l.fecha_hora.isoformat(), 
            "observaciones": l.observaciones
        } for l in lecturas]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener lecturas del sensor {sensor_id}: {e}"}), 500