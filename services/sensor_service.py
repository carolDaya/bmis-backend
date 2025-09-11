from database.connection import db
from models.sensor import Sensor
from models.lectura import Lectura
from datetime import datetime, timedelta
import random

def crear_sensores_base():
    sensores = [
        {"nombre": "Temperatura", "tipo": "Temperatura del biogás", "unidad": "°C"},
        {"nombre": "Presion", "tipo": "Presión del biogás", "unidad": "kPa"},
        {"nombre": "Volumen", "tipo": "Volumen de biogás", "unidad": "m³"}
    ]
    for s in sensores:
        if not Sensor.query.filter_by(nombre=s["nombre"]).first():
            db.session.add(Sensor(**s))
    db.session.commit()
    print("Sensores base creados")

def generar_datos_sinteticos(dias=30):
    sensores = {s.nombre: s for s in Sensor.query.all()}
    registros = []
    fecha_inicio = datetime.now() - timedelta(days=dias)

    for dia in range(dias):
        for hora in range(24):
            fecha = fecha_inicio + timedelta(days=dia, hours=hora)
            registros.append(Lectura(sensor_id=sensores["Temperatura"].id, fecha_hora=fecha, valor=round(random.uniform(35, 40),2)))
            registros.append(Lectura(sensor_id=sensores["Presion"].id, fecha_hora=fecha, valor=round(random.uniform(200, 250),2)))
            registros.append(Lectura(sensor_id=sensores["Volumen"].id, fecha_hora=fecha, valor=round(random.uniform(0.03,0.06),3)))

    db.session.bulk_save_objects(registros)
    db.session.commit()
    print(f"{len(registros)} registros insertados")
