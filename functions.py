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
