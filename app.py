from flask import Flask
from . import create_app
from flask import request
from flask_restful import Api, Resource
from .modelos import db, Healthcheck, Alerta

app = create_app('default')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

class VistaMonitor(Resource):

    def get(self):
        return 'respuesta desde monitor'

    def post(self):
        nuevo_healthcheck = Healthcheck(id_dispositivo=request.json['id_dispositivo'])
        db.session.add(nuevo_healthcheck)
        db.session.commit()

        alerta = Alerta(id_dispositivo=nuevo_healthcheck.id)
        db.session.add(alerta)
        db.session.commit()
        return {"ok": True,
                "mensaje": "Registro healthcheck guardado exitosamente",
                "id": nuevo_healthcheck.id}


api = Api(app)
api.add_resource(VistaMonitor, '/monitor')
