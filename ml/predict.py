import joblib
from utils import cargar_y_procesar_datos

# Cargar modelo
modelo = joblib.load('model.pkl')

# Cargar nuevos datos
df_nuevos = cargar_y_procesar_datos('datasets/sensors.csv')

X_nuevos = df_nuevos[['Temperatura (°C)', 'Presión (kPa)', 'Fase del Proceso Numérica']]
predicciones = modelo.predict(X_nuevos)
df_nuevos['Predicción Alerta IA'] = predicciones

df_nuevos.to_csv('datasets/sensores_predicciones.csv', index=False)
print("Predicciones guardadas en datasets/sensores_predicciones.csv")
