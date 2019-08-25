from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_cors import CORS
from celery_config import make_celery
from datetime import timedelta
from functions import *
from classes import Device, Pi
from calculateDistances import calculateCordinates
import netifaces as nif
import time
import requests
import jsonpickle


ip = '10.22.136.21'
app = Flask(__name__)
CORS(app)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)
celery = make_celery(app)

# pis = gen_test_case(4, 100)
pis = [Pi(75, 75, '10.22.145.185'), Pi(10, 75, '10.22.147.139'), Pi(10, 10, '10.22.159.173')]
snapshot = []

class DevicesAPI(MethodView):

    def post(self):
        global pis
        data = request.json
        devices = []
        for device in data:
            mac = device[0]
            dbm = 0 if device[1] == '' else int(device[1])
            devices.append(Device(mac, dbm))
        ip = request.remote_addr
        for pi in pis:
            if pi.id == ip:
                pi.devices = devices
                break
        return 'Grax x tu apoyo prro'


class PisAPI(MethodView):

    def post(self):
        global pis
        data = request.json
        mac = data['mac']
        x = data['x']
        y = data['y']
        pis.append(Pi(x=x, y=y, id=mac))
        return 'Kreado'

    def get(self):
        return jsonpickle.encode(pis)


class SnapshotAPI(MethodView):

    def get(self):
        return jsonify(snapshot)

    def post(self):
        global snapshot
        snapshot = request.get_json()
        return 'posteado'

def mac_for_ip(ip):
    'Returns a list of MACs for interfaces that have given IP, returns None if not found'
    for i in nif.interfaces():
        addrs = nif.ifaddresses(i)
        try:
            if_mac = addrs[nif.AF_LINK][0]['addr']
            if_ip = addrs[nif.AF_INET][0]['addr']
        except (IndexError, KeyError): #ignore ifaces that dont have MAC or IP
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return None


@celery.task(name='main.update_snapshot')
def update_snapshot():
    while True:
        pis = jsonpickle.decode(requests.get(f'http://{ip}:5000/Pi/').text)
        # snapshot = [{'x': pi.point.x, 'y': pi.point.y, 'intensity': len(pi.devices), 'diameter': 5} for pi in local_pis]
        # snapshot = list(itertools.chain.from_iterable([[{'x': device.point.x / x_max, 'y': device.point.y / y_max} for device in pi] for pi in pis]))
        snapshot = calculateCordinates(pis)
        requests.post(url=f'http://{ip}:5000/Snapshot/', json=snapshot)
        time.sleep(15)

update_snapshot.delay()

app.add_url_rule('/AddDevices/', view_func=DevicesAPI.as_view('add_devices'))
app.add_url_rule('/Snapshot/', view_func=SnapshotAPI.as_view('snapshot'))
app.add_url_rule('/Pi/', view_func=PisAPI.as_view('pis'))

if __name__ == '__main__':
    app.run(host=ip)

# b8:27:eb:6c:fb:4e
