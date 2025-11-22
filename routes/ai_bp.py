from flask import Blueprint, jsonify
from services.ai_service import predecir_alerta
from database.db_service import obtener_ultima_lectura_combinada, hay_proceso_activo, LecturaException 

ai_bp = Blueprint("ai_bp", __name__)

@ai_bp.get("/analizar")
def analizar_biodigestor():
    """
    Endpoint principal de análisis del biodigestor.
    Maneja:
      - Sin proceso
      - Sin lecturas
      - Predicción exitosa
      - Errores internos
    """
    try:
        proceso = hay_proceso_activo()
        print(f"DEBUG LOG: Proceso activo → {proceso}")

        # --- SIN PROCESO ACTIVO ---
        if proceso is None:
            return jsonify({
                "alerta_ia": 0,
                "dia_proceso": 0,
                "mensaje_lectura": "No hay proceso activo. No se generan predicciones.",
                "recomendacion": "Inicie un nuevo proceso biodigestor.",
                "tipo_estado": "Proceso finalizado"
            }), 200

        # --- PROCESO ACTIVO PERO SIN LECTURAS ---
        try:
            lectura = obtener_ultima_lectura_combinada()
        except LecturaException as le:
            return jsonify({
                "alerta_ia": 0,
                "dia_proceso": 0,
                "mensaje_lectura": "Proceso activo, pero aún no hay lecturas completas.",
                "recomendacion": "Espere a que se registren datos.",
                "tipo_estado": "Proceso activo",
                "detalle": str(le)
            }), 200

        # --- LECTURA COMPLETA → PREDICCIÓN ---
        presion_leida, temperatura_leida, gas_leido, timestamp = lectura
        
        # predecir_alerta en el orden que espera: (temperatura, presion, gas, timestamp)
        resultado = predecir_alerta(temperatura_leida, presion_leida, gas_leido, timestamp)
        return jsonify(resultado), 200

    except Exception as e:
        print(f"ERROR FATAL EN /analizar → {e}")
        return jsonify({
            "alerta_ia": 0,
            "dia_proceso": 0,
            "mensaje_lectura": "Error interno del servidor al procesar la predicción.",
            "recomendacion": "Revise logs.",
            "tipo_estado": "Error",
            "detalle": str(e)
        }), 500