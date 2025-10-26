from database.connection import db

class Sensor(db.Model):
    __tablename__ = "sensores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    tipo = db.Column(db.String(50), nullable=False)
    unidad = db.Column(db.String(20), nullable=False)

    # 🔹 Relación con GraphConfig
    grafica_config = db.relationship("GraphConfig", back_populates="sensor", uselist=False)

    # 🔹 Si tienes lecturas
    lecturas = db.relationship("Lectura", back_populates="sensor")
