import joblib
import pandas as pd

class IAService:
    def __init__(self, modelo_path='ml/model.pkl'):
        # Cargar modelo entrenado
        self.modelo = joblib.load(modelo_path)

    def inferir(self, dato_sensor: dict) -> dict:
        """
        Recibe un solo dato y devuelve un mensaje y los datos.
        """
        df = pd.DataFrame([dato_sensor])
        pred = self.modelo.predict(df)[0]  # 0 = normal, 1 = alerta

        if pred == 0:
            mensaje = f"Todo está normal. Valores: {dato_sensor}"
        else:
            mensaje = f"Alerta: producción baja. Valores: {dato_sensor}"

        return {
            "prediccion": int(pred),
            "mensaje": mensaje
        }

