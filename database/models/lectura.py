from database.connection import db
from datetime import datetime

class Lectura(db.Model):
    __tablename__ = "lecturas"

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.now)
    valor = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.String(255), nullable=True)

    sensor = db.relationship("Sensor", back_populates="lecturas")
