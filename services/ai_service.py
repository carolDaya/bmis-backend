import pandas as pd
import joblib
import os
from datetime import datetime
from ml.utils import obtener_recomendacion 

# --- Rutas de Modelos ---
# 1. Obtener la ruta del directorio actual (services/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Navegar al directorio 'ml' (desde services/ subir un nivel y bajar a ml/)
ML_DIR = os.path.join(BASE_DIR, '..', 'ml')

# Cargar modelos
try:
    modelo_alerta = joblib.load(os.path.join(ML_DIR, "modelo_alerta.pkl"))
    modelo_tipo = joblib.load(os.path.join(ML_DIR, "modelo_tipo_alerta.pkl"))
except FileNotFoundError:
    # Este error se debe manejar si no se ha ejecutado el entrenamiento
    print("FATAL ERROR: No se pudieron cargar los modelos de IA. Ejecute el script de entrenamiento.")
    modelo_alerta = None
    modelo_tipo = None


# Fecha de inicio de tu dataset
FECHA_INICIO = datetime.strptime("01/01/2025 00:00", "%d/%m/%Y %H:%M")

def calcular_dia_proceso(timestamp_str):
    """
    Calcula el día del proceso basándose en el timestamp de la lectura.
    """
    try:
        # Asume formato ISO (YYYY-MM-DD HH:MM:SS) o el formato de tu CSV
        # 💡 Importante: Asegúrate de que el formato coincida con el dato de entrada
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            timestamp = datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M")
        except:
            # Fallback en caso de formato incorrecto
            return 1 

    delta = timestamp - FECHA_INICIO
    return delta.days + 1  # día 1 = primer día

def predecir_alerta(temperatura, presion, gas, timestamp):
    """
    Realiza la predicción de alerta usando los modelos cargados.
    
    :param temperatura: Temperatura actual (°C).
    :param presion: Presión actual (kPa).
    :param gas: Concentración de gas actual (ppm).
    :param timestamp: Fecha y hora de la lectura.
    :return: Diccionario con predicciones y recomendaciones.
    """
    if modelo_alerta is None or modelo_tipo is None:
        return {
            "alerta_ia": 0,
            "tipo_estado": "Error de Sistema",
            "mensaje_lectura": "Modelos de IA no cargados. Revisar logs del servidor.",
            "recomendacion": "Ejecute el script de entrenamiento de modelos.",
            "dia_proceso": 0
        }

    # 1. Calcular el día del proceso
    dia_proceso = calcular_dia_proceso(timestamp)

    # 2. Preparar la entrada para los modelos (debe coincidir con X del entrenamiento)
    entrada = pd.DataFrame([{
        "temperatura_celsius": temperatura,
        "presion_biogas_kpa": presion,
        "mq4_ppm": gas,
        "dia_proceso": dia_proceso
    }])

    # 3. Realizar predicciones
    alerta_pred = modelo_alerta.predict(entrada)[0]
    tipo_pred = modelo_tipo.predict(entrada)[0]

    # 4. Generar la recomendación completa usando la función de utilidad
    recomendacion_data = obtener_recomendacion(
        estado=int(alerta_pred),
        temperatura=temperatura,
        presion=presion,
        gas=gas
    )

    # 5. Combinar resultados
    resultado = {
        "alerta_ia": int(alerta_pred),
        "tipo_alerta_modelo": str(tipo_pred), # La predicción de tipo del modelo
        "tipo_estado": recomendacion_data["tipo"], # El tipo de la utilidad (Normal o Alerta: [Tipo])
        "mensaje_lectura": recomendacion_data["mensaje"],
        "recomendacion": recomendacion_data["recomendacion"],
        "dia_proceso": dia_proceso
    }

    return resultado