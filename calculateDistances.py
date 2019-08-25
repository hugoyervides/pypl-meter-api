#Script para calcular las cordenadas de los dispositivos dentro del plano con la senal

#Function de trilateration
def trilateration(point1,r1,point2,r2,point3,r3):
  A = 2*point2.x - 2*point1.x
  B = 2*point2.y - 2*point1.y
  C = r1**2 - r2**2 - pont1.x**2 + point2.x**2 - point1.y**2 + point2.y**2
  D = 2*point3.x - 2*point2.x
  E = 2*point3.y - 2*point2.y
  F = r2**2 - r3**2 - point2.x**2 + point3.x**2 - point2.y**2 + point3.y**2
  x = (C*E - F*B) / (E*A - B*D)
  y = (C*D - A*F) / (B*D - A*E)
  return Point(x,y)

#Fuction to find device in the list of pis
def findDevicesOnPis(pis,device):
    devices = []
    #for para navegar por las Pis
    for pi in pis:
        for device in pi.devices:
            if device == device:
                devices.append({'device':device,'pi':pi})
    return devices
#Funcion para 
def calculateCordinates(pis):
    #declaracion de variables
    visited =[]
    returnDevices = []
    #Condicion para ver si tenemos mas de 3 puntos de centro
    if pis.len() > 3:
        return None
    #Calculamos los puntos de las Pis
    for pi in pis:
        for device in pi.devices:
            #ver si no visitamos ya este device
            if not device in visited:
                visited.append(device)
                result = findDevicesOnPis(pis,device)
                #ver cual algoritmo usar
                if result.len() == 2:
                    #ALGORITMO PARA DOS PUNTOS

                else if result.len() == 3:
                    #ALGORITMO PARA TRES PUNTOS
                    loc = trilateration(result[0]['pi'].point,
                                        result[0]['pi'].getRealDistance(result[0]['device'],
                                        result[1]['pi'].point,
                                        result[1]['pi'].getRealDistance(result[1]['device'],
                                        result[2]['pi'].point,
                                        result[2]['pi'].getRealDistance(result[2]['device'])
                    #Actualizar la loc del device para meterla en el resultado
                    device.point = loc
                    returnDevices.append(device)
    #regresar el resultado
    return returnDevices           