from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import datetime

from sqlalchemy import func

db = SQLAlchemy()


class Healthcheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dispositivo = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime(timezone=True), server_default=func.now())
    desconectado = db.Column(db.Boolean)


class Alerta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dispositivo = db.Column(db.Integer)
    fecha_registro_alerta = db.Column(db.DateTime(timezone=True), server_default=func.now())


class HealthcheckSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Healthcheck
        load_instance = True


class AlertaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Alerta
        load_instance = True
