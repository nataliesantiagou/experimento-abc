from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import datetime

db = SQLAlchemy()

class Healthcheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dispositivo = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Alerta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dispositivo = db.Column(db.Integer)
    fecha_registro_alerta = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class HealthcheckSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Healthcheck
        load_instance = True

class AlertaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Alerta
        load_instance = True