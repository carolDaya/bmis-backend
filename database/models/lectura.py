from datetime import datetime, timezone
from database.connection import db
from sqlalchemy.orm import validates

class Lectura(db.Model):
    __tablename__ = "lecturas"

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.id'), nullable=False)
    proceso_id = db.Column(db.Integer, db.ForeignKey('proceso_biodigestor.id'), nullable=True)
    fecha_hora = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    valor = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.String(255), nullable=True)

    sensor = db.relationship("Sensor", back_populates="lecturas")
    proceso = db.relationship("ProcesoBiodigestor", back_populates="lecturas")

    @validates('valor')
    def validate_valor(self, key, value):
        if value is None:
            raise ValueError("El valor de la lectura no puede ser nulo")
        try:
            float_value = float(value)
            return float_value
        except (ValueError, TypeError):
            raise ValueError("El valor debe ser un número válido")

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "proceso_id": self.proceso_id,
            "valor": self.valor,
            "fecha_hora": self.fecha_hora.isoformat(),
            "observaciones": self.observaciones
        }