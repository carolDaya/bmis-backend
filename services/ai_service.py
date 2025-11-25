import os
import joblib
import pandas as pd
from datetime import datetime
from ml.utils import obtener_recomendacion
from database.db_service import obtener_fecha_inicio_proceso_activo

# --- Rutas de Modelos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, '..', 'ml')

# --- Carga de modelos ---
try:
    modelo_alerta = joblib.load(os.path.join(ML_DIR, "modelo_alerta.pkl"))
    modelo_tipo = joblib.load(os.path.join(ML_DIR, "modelo_tipo_alerta.pkl"))
except FileNotFoundError:
    print("FATAL ERROR: No se pudieron cargar los modelos de IA. Ejecute el script de entrenamiento.")
    modelo_alerta = None
    modelo_tipo = None


def calcular_dia_proceso(timestamp_str):
    """
    Calcula el día del proceso según el timestamp.
    Devuelve 0 si no hay proceso activo.
    Maneja múltiples formatos de fecha.
    """
    fecha_inicio = obtener_fecha_inicio_proceso_activo()
    if fecha_inicio is None:
        return 0

    # Intentar formatos
    formatos_admitidos = ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M")

    for fmt in formatos_admitidos:
        try:
            timestamp = datetime.strptime(timestamp_str, fmt)
            break
        except ValueError:
            continue
    else:
        # Timestamp inválido
        return 1

    delta = timestamp - fecha_inicio
    return delta.days + 1


def predecir_alerta(temperatura, presion, gas, timestamp):
    """
    Realiza predicción IA.
    Maneja errores comunes, modelos no cargados, no proceso activo, etc.
    Retorna un dict estandarizado.
    """
    try:

        # --- SI NO HAY MODELOS CARGADOS ---
        if modelo_alerta is None or modelo_tipo is None:
            return {
                "alerta_ia": 0,
                "tipo_estado": "Error de Sistema",
                "mensaje_lectura": "Modelos de IA no cargados.",
                "recomendacion": "Ejecute el script de entrenamiento.",
                "dia_proceso": 0
            }

        dia_proceso = calcular_dia_proceso(timestamp)

        if dia_proceso == 0:
            return {
                "alerta_ia": 0,
                "tipo_estado": "Proceso finalizado",
                "mensaje_lectura": "No hay proceso activo. No se generan predicciones.",
                "recomendacion": "Inicie un nuevo proceso biodigestor.",
                "dia_proceso": 0
            }

        # --- Construcción del DataFrame ---
        entrada = pd.DataFrame([{
            "temperatura_celsius": temperatura,
            "presion_biogas_kpa": presion,
            "mq4_ppm": gas,
            "dia_proceso": dia_proceso
        }])

        alerta_pred = int(modelo_alerta.predict(entrada)[0])
        tipo_pred = str(modelo_tipo.predict(entrada)[0])

        # Obtener recomendaciones según lectura
        recomendacion_data = obtener_recomendacion(
            estado=alerta_pred,
            temperatura=temperatura,
            presion=presion,
            gas=gas
        )

        return {
            "alerta_ia": alerta_pred,
            "tipo_alerta_modelo": tipo_pred,
            "tipo_estado": recomendacion_data.get("tipo", ""),
            "mensaje_lectura": recomendacion_data.get("mensaje", ""),
            "recomendacion": recomendacion_data.get("recomendacion", ""),
            "dia_proceso": dia_proceso
        }

    except Exception as e:
        # Error interno del modelo o datos
        return {
            "alerta_ia": 0,
            "tipo_estado": "Error interno IA",
            "mensaje_lectura": "Ocurrió un error durante la predicción.",
            "recomendacion": "Revise los logs del servidor.",
            "dia_proceso": 0,
            "detalle_error": str(e)
        }
