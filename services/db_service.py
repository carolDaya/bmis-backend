from database.models.lectura import Lectura
from database.connection import db
from sqlalchemy import desc
from datetime import datetime

def obtener_ultima_lectura_combinada():
    """
    Obtiene la última lectura registrada de cada sensor (gas, temperatura y presión)
    usando SQLAlchemy ORM, sin escribir SQL manual.
    Retorna una tupla: (temperatura, presion, gas, timestamp)
    """

    try:
        # 🔹 Buscar la última lectura por cada sensor_id
        ultima_temp = Lectura.query.filter_by(sensor_id=2).order_by(desc(Lectura.fecha_hora)).first()
        ultima_pres = Lectura.query.filter_by(sensor_id=3).order_by(desc(Lectura.fecha_hora)).first()
        ultima_gas = Lectura.query.filter_by(sensor_id=1).order_by(desc(Lectura.fecha_hora)).first()

        # 🔹 Obtener el timestamp más reciente en general
        ultima_fecha = (
            db.session.query(Lectura.fecha_hora)
            .order_by(desc(Lectura.fecha_hora))
            .first()
        )

        # 🔹 Verificar si existen datos
        if not (ultima_temp and ultima_pres and ultima_gas and ultima_fecha):
            print("⚠️ No se encontraron lecturas suficientes para los sensores.")
            return None

        temperatura = float(ultima_temp.valor)
        presion = float(ultima_pres.valor)
        gas = float(ultima_gas.valor)
        timestamp = str(ultima_fecha[0])

        return (temperatura, presion, gas, timestamp)

    except Exception as e:
        print(f"❌ Error al obtener lecturas combinadas: {e}")
        return None
