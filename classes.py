import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'


class Device:
    def __init__(self, mac, dbm, x=None, y=None):
        self.point = Point(x, y)
        self.mac = mac
        self.dbm = dbm

    def __str__(self):
        return f'{self.mac}: {str(self.point)}, {self.dbm}.'

    def getRealDistance(self):
        return 10 ^ ((27.55 - (20 * math.log10(2437)) + abs(self.dbm))/20)

class Pi:
    devices = []
    def __init__(self, x, y, id, dbmToFoot):
        self.point = Point(x, y)
        self.id = id

    def remove(self, device):
        self.devices.remove(device)

    def __str__(self):
        return f'Pi #{self.id} at {str(self.point)}.'

    def __iter__(self):
        for device in self.devices:
            yield device