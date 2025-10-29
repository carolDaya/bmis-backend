from flask import Blueprint, jsonify
from services.ai_service import predecir_alerta
from services.db_service import obtener_ultima_lectura_combinada 

ai_bp = Blueprint("ai_bp", __name__)

@ai_bp.route("/analizar", methods=["GET"]) 
def analizar_biodigestor():
    """
    Endpoint llamado por la App Móvil. 
    Llama a la DB para obtener los últimos datos reales y los pasa a la IA.
    """
    try:
        # 1. Obtener la última lectura de la Base de Datos (¡El código real que acabas de ver!)
        lectura = obtener_ultima_lectura_combinada()

        if not lectura:
            return jsonify({
                "error": "No se puede obtener la última lectura de la DB.",
                "detalle": "Revisar la configuración y el código de db_service.py"
            }), 404

        temperatura, presion, gas, timestamp = lectura 
        
        # 2. Ejecutar el servicio de IA con los datos REALES
        resultado = predecir_alerta(temperatura, presion, gas, timestamp)
        
        # 3. Respuesta exitosa
        return jsonify(resultado), 200
        
    except Exception as e:
        print(f"Error durante el procesamiento de la predicción de IA: {e}")
        return jsonify({
            "error": "Error interno del servidor al procesar la predicción.",
            "detalle": str(e)
        }), 500