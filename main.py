from flask import Flask
from flask.views import MethodView
app = Flask(__name__)

class AddDevicesAPI(MethodView):

    def post(self):
        return 'ok'


class GetSnapshotAPI(MethodView):

    def get(self):
        return 'ok'


app.add_url_rule('/AddDevices/', view_func=TestAPI.as_view('add_devices'))
app.add_url_rule('/GetSnapshot/', view_func=GetSnapshotAPI.as_view('get_snapshot'))
