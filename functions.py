from classes import *
from random import randint

def clean_data(pis):
    for pi in pis:
        for device in pi:
            for pi2 in pis:
                if pi is pi2:
                    continue
                for device2 in pi2:
                    if device.mac == device2.mac:
                        pi.remove(device) if device.dbm < device2.dbm else pi2.remove(device2)
                        break
    return pis

def randomMAC():
    return ':'.join(map(lambda x: "%02x" % x, [0x00, 0x16, 0x3e, randint(0x00, 0x7f), randint(0x00, 0xff), randint(0x00, 0xff) ]))

def gen_test_case(pis=3, devices=1000):
    pis = [Pi(randint(0, 100), randint(0, 100), i, randint(0, 10)) for i in range(pis)]
    for pi in pis:
        pi.devices = [Device(randomMAC(), randint(-200, 0), randint(0, 100), randint(0, 100)) for i in range(devices)]
    return pis


def normalize_snapshot(snapshot):
    if len(snapshot) < 2:
        return snapshot
    x_max = x_min = snapshot[0]['x']
    y_max = y_min = snapshot[0]['y']
    intensity_max = intensity_min = snapshot[0]['intensity']
    diameter_max = diameter_min = snapshot[0]['diameter']
    for snap in snapshot[1:]:
        if snap['x'] > x_max:
            x_max = snap['x']
        elif snap['x'] < x_min:
            x_min = snap['x']
        if snap['y'] > y_max:
            y_max = snap['y']
        elif snap['y'] < y_min:
            y_min = snap['y']
        if snap['intensity'] > intensity_max:
            intensity_max = snap['intensity']
        elif snap['intensity'] < intensity_min:
            intensity_min = snap['intensity']
        if snap['diameter'] > diameter_max:
            diameter_max = snap['diameter']
        elif snap['diameter'] < diameter_min:
            diameter_min = snap['diameter']
    normalized_snapshot = []
    if intensity_max == intensity_min:
        intensity_max = intensity_max + 1
    if diameter_max == diameter_min:
        diameter_max = diameter_max + 1
    for snap in snapshot:
        normalized_snapshot.append({'x': (snap['x'] - x_min) / (x_max - x_min),
                                    'y': (snap['y'] - y_min) / (y_max - y_min),
                                    'intensity': (snap['intensity'] - intensity_min) / (intensity_max - intensity_min),
                                    'diameter': (snap['diameter'] - diameter_min) / (diameter_max - diameter_min)})
    return normalized_snapshot
