from database.connection import db
from sqlalchemy.orm import validates
import logging

logger = logging.getLogger(__name__)

class Sensor(db.Model):
    __tablename__ = "sensores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    tipo = db.Column(db.String(50), nullable=False)
    unidad = db.Column(db.String(20), nullable=False)

    grafica_config = db.relationship("GraphConfig", back_populates="sensor", uselist=False)
    lecturas = db.relationship("Lectura", back_populates="sensor", lazy='dynamic')

    @validates('nombre')
    def validate_nombre(self, key, value):
        if not value or not value.strip():
            raise ValueError("El nombre del sensor no puede estar vacío")
        return value.strip()

    @validates('tipo')
    def validate_tipo(self, key, value):
        if not value or not value.strip():
            raise ValueError("El tipo del sensor no puede estar vacío")
        return value.strip()

    @validates('unidad')
    def validate_unidad(self, key, value):
        if not value or not value.strip():
            raise ValueError("La unidad del sensor no puede estar vacía")
        return value.strip()

    def to_dict(self):
        """Serializa el modelo a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "unidad": self.unidad
        }