from math import sin, cos, pi

def calcularVerticesPoligono(numLados:int, xCentro:float, yCentro:float, distanciaRadial:float):
    '''Calcula las posiciones en que se encuentran los vertices de un polígono. 
    Recibe como parámetro el número de lados del polígono, las coordenadas de su centro y la distancia del centro a uno de los vertices'''
    listaCoords=[]
    for i in range(numLados):
        xVertice=xCentro+distanciaRadial*(cos(2*pi*i/numLados))
        yVertice=yCentro+distanciaRadial*(sin(2*pi*i/numLados))
        listaCoords.append([xVertice,yVertice])
    if numLados<4:
        return listaCoords
    else:
        ajuste=(numLados-4)//2
        return listaCoords[-ajuste:]+listaCoords[0:-ajuste]