from . import create_app
from flask_restful import Api, Resource

app = create_app('default')
app_context = app.app_context()
app_context.push()


class VistaMonitor(Resource):

    def get(self):
        return 'respuesta desde monitor'


api = Api(app)
api.add_resource(VistaMonitor, '/monitor')
