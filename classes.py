class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Device:
    def __init__(self, x, y, mac, dbm):
        self.point = Point(x, y)
        self.mac = mac
        self.dbm = dbm


class Pi:
    devices = []

    def __init__(self, x, y, id):
        self.point = Point(x, y)
        self.id = id

    def __str__(self):
        return f'Pi #{self.id} at ({x}, {y}).'
