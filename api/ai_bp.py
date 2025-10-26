from flask import Blueprint, request, jsonify
from services.ai_service import predecir_alerta

# Crea el Blueprint
ai_bp = Blueprint("ai_bp", __name__)

@ai_bp.route("/analizar", methods=["POST"])
def analizar_biodigestor():
    """
    Endpoint para recibir una nueva lectura (temperatura, presión, gas, timestamp)
    y predecir el estado del biodigestor usando la IA.
    """
    data = request.get_json()

    # 1. Validación de datos de entrada
    try:
        # Se asegura que todos los campos requeridos estén presentes y sean del tipo correcto
        temperatura = float(data["temperatura"])
        presion = float(data["presion"])
        gas = float(data["gas"])
        timestamp = data["timestamp"]
    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Datos incompletos o incorrectos.",
            "detalle": "Se requieren: 'temperatura' (float), 'presion' (float), 'gas' (float) y 'timestamp' (string)."
        }), 400

    # 2. Ejecutar el servicio de IA
    try:
        resultado = predecir_alerta(temperatura, presion, gas, timestamp)
        
        # 3. Respuesta exitosa
        return jsonify(resultado), 200
        
    except Exception as e:
        # Manejo de errores internos (ej. error al cargar modelos o en la lógica)
        print(f"Error durante el procesamiento de la predicción de IA: {e}")
        return jsonify({
            "error": "Error interno del servidor al procesar la predicción.",
            "detalle": str(e)
        }), 500