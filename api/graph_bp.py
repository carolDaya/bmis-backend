from flask import Blueprint, request, jsonify
from services.graph_service import (
    guardar_o_actualizar_config,
    obtener_todas_configs,
    obtener_config_por_sensor
)

graph_bp = Blueprint("graph", __name__)

@graph_bp.route("/graficas/update", methods=["POST"])
def update_graph():
    data = request.json
    sensor_id = data.get("sensor_id")
    tipo_grafica = data.get("tipo_grafica")

    if not sensor_id or not tipo_grafica:
        return jsonify({"error": "Faltan datos"}), 400

    config = guardar_o_actualizar_config(sensor_id, tipo_grafica)
    return jsonify({
        "message": "Configuración guardada",
        "sensor_id": config.sensor_id,
        "tipo_grafica": config.tipo_grafica
    }), 200


@graph_bp.route("/graficas", methods=["GET"])
def get_graphs():
    configs = obtener_todas_configs()
    result = [
        {
            "sensor_id": c.sensor_id,
            "tipo_grafica": c.tipo_grafica,
            "fecha_modificacion": c.fecha_modificacion
        }
        for c in configs
    ]
    return jsonify(result), 200


@graph_bp.route("/graficas/<int:sensor_id>", methods=["GET"])
def get_graph(sensor_id):
    config = obtener_config_por_sensor(sensor_id)
    if not config:
        return jsonify({"error": "No hay configuración para este sensor"}), 404

    return jsonify({
        "sensor_id": config.sensor_id,
        "tipo_grafica": config.tipo_grafica,
        "fecha_modificacion": config.fecha_modificacion
    }), 200
