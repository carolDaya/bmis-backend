import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
from utils import cargar_y_procesar_datos

# Cargar y procesar datos históricos
df = cargar_y_procesar_datos('datasets/sensors.xlsx')

X = df[['Temperatura (°C)', 'Presión (kPa)', 'Fase del Proceso Numérica']]
y = df['Alerta IA']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo_arbol = DecisionTreeClassifier(random_state=42)
modelo_arbol.fit(X_train, y_train)

joblib.dump(modelo_arbol, 'model.pkl')
print("Modelo entrenado y guardado en model.pkl")

# Visualización del árbol
dot_data = export_graphviz(
    modelo_arbol,
    out_file=None,
    feature_names=X.columns,
    class_names=['Sin Alerta', 'Con Alerta'],
    filled=True,
    rounded=True,
    special_characters=True
)

graph = graphviz.Source(dot_data)
graph.render("tree_visualization")
print("Visualización generada en tree_visualization.pdf")
