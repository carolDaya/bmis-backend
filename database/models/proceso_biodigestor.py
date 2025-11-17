from database.connection import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class ProcesoBiodigestor(db.Model):
    """
    Modelo de Proceso del Biodigestor.
    - fecha_fin nullable significa que el proceso sigue activo.
    - lecturas relacionadas.
    """
    __tablename__ = "proceso_biodigestor"
    
    # Constraint para evitar múltiples procesos activos
    __table_args__ = (
        CheckConstraint(
            "(estado = 'ACTIVO' AND fecha_fin IS NULL) OR (estado = 'FINALIZADO' AND fecha_fin IS NOT NULL)",
            name='check_estado_fecha_fin'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False, default=datetime.now)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.Enum('ACTIVO', 'FINALIZADO'), default='ACTIVO')
    observaciones = db.Column(db.String(255), nullable=True)

    lecturas = db.relationship("Lectura", back_populates="proceso")