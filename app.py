from flask import Flask
import os
from flask_restful import Api, Resource
import datetime
from modelos import db, Healthcheck, HealthcheckSchema, Alerta
from flask_cors import CORS
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

healthcheck_schema = HealthcheckSchema()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)


class VistaMonitor(Resource):

    # se cambio a GET porque los heltChek son mas comunes en una peticion simple de tipo get
    def get(self, id_dispositivo):
        # consulto si existe el dispositivo
        dispositivo: Healthcheck = db.session.query(Healthcheck).filter(
            Healthcheck.id_dispositivo == id_dispositivo).first()
        if dispositivo:
            # si ya esxiste solo registro la fecha y el estado conectado
            dispositivo.fecha_registro = datetime.datetime.utcnow()
            dispositivo.desconectado = False
            db.session.add(dispositivo)
            db.session.commit()
        else:
            # si no existe lo registro en el sistema
            nuevo_healthcheck = Healthcheck(id_dispositivo=id_dispositivo, desconectado=False)
            db.session.add(nuevo_healthcheck)
            db.session.commit()

        return {"ok": True,
                "mensaje": "Registro healthcheck guardado exitosamente",
                "id": id_dispositivo}


# hilo para revisar las desconexiones y generar alertas
def revisar_desconexiones():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    with app.app_context():
        # TODO: sumar fechas para poder hacer el filtro en la consulta
        # Consulta para filtrar dispositivosn con un tiempo mayor al pemritodo de desconexion
        current_time = datetime.datetime.utcnow()
        one_min_ago = current_time - datetime.timedelta(seconds=15)

        dispositivos = db.session.query(Healthcheck).filter(Healthcheck.desconectado.is_(False)).filter(
            Healthcheck.fecha_registro < one_min_ago).all()
        for dispositivo in dispositivos:
            # se cambia el estado para ponerlo desconectado
            dispositivo.desconectado = True
            db.session.add(dispositivo)
            # Se registra la alerta
            alerta = Alerta(id_dispositivo=dispositivo.id)
            db.session.add(alerta)
            db.session.commit()


# creacion del hilo
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=revisar_desconexiones, trigger="interval", seconds=1)
# Para que no genere varios hilos en ambientes de desarrollo o en debug
if not (app.debug or os.environ.get('FLASK_ENV') == 'development') or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

api = Api(app)
api.add_resource(VistaMonitor, '/monitor/<string:id_dispositivo>')
