import os
import random
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
    

def nombresAleatorios(cantidadP:int):
    """
    Crea una lista de nombres aleatorios sin repetición.

    Parámetros:
    cantidadP (int): la cantidad de personas que van a jugar.

    Retorna:
    Una lista con `cantidadP` de nombres aleatorios seleccionados al azar de la lista `nombres`.
    """
    nombres=["Thomas", "María", "Alejandra", "Ana", "Jeronimo", "Juan", "Brahian", "Pedro", 
            "Gabriela", "Camilo", "Sofia", "Andres", "Valery", "Pepe", "Juanita", "Luis",
            "Clara", "Adrian", "Veronica", "Santiago", "Valentina", "Miguel", "Manuela",
            "Manuel", "Gina", "Stiven", "Dana", "Sara", "Jessica", "Jhon", "Esteban", "David"]
    lista=[]
    i=cantidadP
    while i != 0:
        aleatorio = random.choice(nombres)
        if aleatorio not in lista: 
            lista.append(aleatorio)
            i-=1
    return lista

def buscarSprites(carpetaPpal:str):

    listaRutas = []

    rutaHombres = os.path.join(carpetaPpal, "Males")
    rutaMujeres = os.path.join(carpetaPpal, "Females")

    spritesHombres = os.listdir(rutaHombres)
    spritesMujeres = os.listdir(rutaMujeres)

    for elemento in spritesHombres:
        rutaCompleta = os.path.join(rutaHombres, elemento)
        listaRutas.append(rutaCompleta)
    for elemento in spritesMujeres:
        rutaCompleta = os.path.join(rutaMujeres, elemento)
        listaRutas.append(rutaCompleta)

    return listaRutas

print(buscarSprites("sprites"))