import pandas as pd
import graphviz
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score

# Cargar el archivo
df = pd.read_excel('/kaggle/input/datos-sensores/biodigestor-datosSinteticos.xlsx')

# 1. Renombrar las columnas para una mejor visualización
column_mapping = {
    'timestamp': 'Fecha y Hora',
    'dia_proceso': 'Día',
    'fase_proceso': 'Fase del Proceso',
    'temperatura_celsius': 'Temperatura (°C)',
    'presion_biogas_kpa': 'Presión (kPa)',
    'volumen_biogas_m3_dia': 'Volumen de Biogás (m3/día)',
    'alerta_ia': 'Alerta IA',
    'tipo_alerta': 'Tipo de Alerta'
}
df = df.rename(columns=column_mapping)

# 2. Preparar los datos y entrenar el modelo
# Convierte 'Fase del Proceso' de texto a un número (0 o 1)
df['Fase del Proceso Numérica'] = df['Fase del Proceso'].apply(lambda x: 1 if x == 'Activa' else 0)

# Define las variables de entrada (X) y la variable a predecir (y)
X = df[['Temperatura (°C)', 'Presión (kPa)', 'Fase del Proceso Numérica']]
y = df['Alerta IA']

# Divide los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrena el modelo de Árbol de Decisión
modelo_arbol = DecisionTreeClassifier(random_state=42)
modelo_arbol.fit(X_train, y_train)

# 3. Visualiza el modelo con los nuevos nombres
dot_data = export_graphviz(modelo_arbol, out_file=None, 
                           feature_names=X.columns,
                           class_names=['Sin Alerta', 'Con Alerta'],
                           filled=True, rounded=True, special_characters=True)

# Crea el gráfico
graph = graphviz.Source(dot_data)

# Muestra el gráfico
graph