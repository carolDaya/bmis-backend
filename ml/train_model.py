import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# --- Configuración de rutas para guardar modelos ---
# Asegúrate de que el directorio 'ml' exista en el directorio raíz de tu proyecto
if not os.path.exists("ml"):
    os.makedirs("ml")

# Cargar dataset
# Pandas usará la primera fila como encabezado por defecto.
try:
    df = pd.read_csv("sensors.csv")
except FileNotFoundError:
    print("Error: No se encontró 'sensors.csv'. Por favor, verifica la ruta.")
    exit()

# -----------------------------------------------------------
# --- PREPARACIÓN DE DATOS Y LIMPIEZA ESENCIAL ---
# -----------------------------------------------------------

# 1. Convertir la columna 'alerta_ia' (de string 'False'/'True' a entero 0/1)
# Esto soluciona los errores de 'invalid literal' y 'cannot convert float NaN'.
print("Preparando datos...")
df["alerta_ia"] = (
    df["alerta_ia"]
    .astype(str)
    .str.lower()
    .map({"true": 1, "false": 0})
    .fillna(0) # Reemplazamos cualquier NaN resultante con 0 (asumiendo no-alerta)
    .astype(int)
)

# 2. Asegurar que 'tipo_alerta' sea un string y rellenar nulos si los hay.
df["tipo_alerta"] = df["tipo_alerta"].fillna("Normal").astype(str)

# -----------------------------------------------------------
# --- Definición de Features y Targets ---
# -----------------------------------------------------------

# Features (Variables independientes)
# Usamos las columnas numéricas que has confirmado
X = df[["temperatura_celsius", "presion_biogas_kpa", "mq4_ppm", "dia_proceso"]]

# Targets (Variables a predecir)
y_alerta = df["alerta_ia"]
y_tipo = df["tipo_alerta"]

# -----------------------------------------------------------
# --- Entrenamiento del Modelo ---
# -----------------------------------------------------------

# Dividir conjunto de entrenamiento y prueba
X_train, X_test, y_alerta_train, y_alerta_test, y_tipo_train, y_tipo_test = train_test_split(
    X, y_alerta, y_tipo, test_size=0.2, random_state=42
)

# Entrenar modelo alerta (Clasificación Binaria: 0 o 1)
print("Entrenando Modelo Alerta...")
modelo_alerta = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_alerta.fit(X_train, y_alerta_train)

# Entrenar modelo tipo de alerta (Clasificación Multi-Clase)
print("Entrenando Modelo Tipo de Alerta...")
modelo_tipo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_tipo.fit(X_train, y_tipo_train)

# -----------------------------------------------------------
# --- Evaluación y Guardado ---
# -----------------------------------------------------------

# Evaluación
y_alerta_pred = modelo_alerta.predict(X_test)
y_tipo_pred = modelo_tipo.predict(X_test)

print("\n--- Resultados de Evaluación ---")
print("🔹 Precisión alerta:", accuracy_score(y_alerta_test, y_alerta_pred))
print("🔹 Precisión tipo alerta:", accuracy_score(y_tipo_test, y_tipo_pred))
print("\nReporte tipo de alerta:\n", classification_report(y_tipo_test, y_tipo_pred, zero_division=0))

# Guardar modelos en el directorio 'ml'
joblib.dump(modelo_alerta, "ml/modelo_alerta.pkl")
joblib.dump(modelo_tipo, "ml/modelo_tipo_alerta.pkl")
print("\n✅ Modelos entrenados y guardados en el directorio 'ml/'")