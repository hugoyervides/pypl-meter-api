#Script para calcular las cordenadas de los dispositivos dentro del plano con la senal
from classes import Point
import math
import random

#Function de trilateration
def trilateration(point1,r1,point2,r2,point3,r3):
    A = 2*point2.x - 2*point1.x
    B = 2*point2.y - 2*point1.y
    C = r1**2 - r2**2 - point1.x**2 + point2.x**2 - point1.y**2 + point2.y**2
    D = 2*point3.x - 2*point2.x
    E = 2*point3.y - 2*point2.y
    F = r2**2 - r3**2 - point2.x**2 + point3.x**2 - point2.y**2 + point3.y**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    return Point(x,y)


def magnitude_to_vector(magnitude, angle):
    return Point(magnitude * math.cos(angle), magnitude * math.sin(angle))


def get_vector_magnitude(point):
    return math.sqrt(point.x ** 2 + point.y ** 2)


def bilateration(point1, r1, point2, r2):
    diff = point2 - point1
    angle = math.atan2(diff.y, diff.x)
    limit1 = point1 + magnitude_to_vector(r1, angle)
    limit2 = point2 - magnitude_to_vector(r2, angle)
    half_point = (limit1 + limit2) / 2
    distance = get_vector_magnitude(half_point - point1)
    x_freedom = abs(get_vector_magnitude(limit1) - get_vector_magnitude(limit2)) / 2
    y_freedom = math.sqrt(r1 ** 2 - distance ** 2)
    final_x = half_point + magnitude_to_vector((random.random() - 0.5) * 2 * x_freedom, angle)
    final_y = half.point + magnitude_to_vector((random.random() - 0.5) * 2 * y_freedom, angle + math.radians(90))
    return Point(final_x, final_y)


def unilateration(point, r):
    angle = 2 * math.pi * random.random()
    r2 = r * random.random()
    return point + Point(r2 * math.cos(angle), r2 * math.sin(angle))


#Fuction to find device in the list of pis
def findDevicesOnPis(pis,device):
    devices = []
    #for para navegar por las Pis
    for pi in pis:
        for device in pi.devices:
            if device == device:
                devices.append({'device':device,'pi':pi})
    return devices


def div_loc(point, x_max, y_max):
    x = point.x / x_max
    if x > 1:
        x = 1 - random.random() * 0.2
    elif x < 0:
        x = 0 + random.random() * 0.2
    y = point.y / y_max
    if y > 1:
        y = 1 - random.random() * 0.2
    elif y < 0:
        y = 0 + random.random() * 0.2
    return Point(x, y)


#Funcion para
def calculateCordinates(pis):
    #declaracion de variables
    visited =[]
    returnDevices = []
    x_max = 150
    y_max = 150
    #Condicion para ver si tenemos mas de 3 puntos de centro
    if len(pis) > 3:
        return None
    #Calculamos los puntos de las Pis
    for pi in pis:
        for device in pi.devices:
            #ver si no visitamos ya este device
            if not device in visited:
                visited.append(device)
                result = findDevicesOnPis(pis,device)
                #ver cual algoritmo usar
                if len(result) == 2:
                    #ALGORITMO PARA DOS PUNTOS
                    loc = bilateration(result[0]['pi'].point, result[0]['device'].getRealDistance(),
                                       result[1]['pi'].point, result[0]['device'].getRealDistance())
                    device.point = div_loc(loc, x_max, y_max)
                    returnDevices.append({'x': device.point.x, 'y': device.point.y})
                elif len(result) == 3:
                    #ALGORITMO PARA TRES PUNTOS
                    loc = trilateration(result[0]['pi'].point, result[0]['device'].getRealDistance(),
                                        result[1]['pi'].point,
                                        result[1]['device'].getRealDistance(),
                                        result[2]['pi'].point,
                                        result[2]['device'].getRealDistance())
                    #Actualizar la loc del device para meterla en el resultado
                    device.point = div_loc(loc, x_max, y_max)
                    returnDevices.append({'x': device.point.x, 'y': device.point.y})
                else:
                    #ALGORITMO PARA UN PUNTO
                    loc = unilateration(result[0]['pi'].point, result[0]['device'].getRealDistance())
                    device.point = div_loc(loc, x_max, y_max)
                    returnDevices.append({'x': device.point.x, 'y': device.point.y})
    #regresar el resultado
    return returnDevices
