import os
import random
from math import sin, cos, pi

def calcularVerticesPoligono(numLados:int, xCentro:float, yCentro:float, distanciaRadial:float):
    '''Calcula las posiciones en que se encuentran los vertices de un polígono. 
    Recibe como parámetro el número de lados del polígono, las coordenadas de su centro y la distancia del centro a uno de los vertices.
    Retorna una lista que contiene varias tuplas de coordenadas en X y en Y'''
    listaCoords=[]
    for i in range(-1,numLados-1):
        xVertice=xCentro+distanciaRadial*(cos(2*pi*i/numLados))
        yVertice=yCentro+distanciaRadial*(sin(2*pi*i/numLados))
        listaCoords.append((xVertice,yVertice))
    return listaCoords

def nombresAleatorios(cantidadP:int):
    '''
    Crea una lista de nombres aleatorios sin repetición.

    Parámetros:
    cantidadP (int): la cantidad de personas que van a jugar.

    Retorna:
    Una lista con `cantidadP` de nombres aleatorios seleccionados al azar de la lista `nombres`.
    '''
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
    '''Se encarga de revisar las carpetas que contienen los sprites y retorna las rutas en una lista. 
    Recibe como parámetro el nombre de la carpeta donde se encuentran los sprites
    '''
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

def generarDiccColores():
    '''Se encarga de generar un diccionario de colores por defecto. 
    Cada color es la clave y su valor es una tupla de 3 valores enteros.
    No recibe parámetros y retorna un diccionario
    '''
    dicc={}
    dicc["blanco"] = (255, 255, 255)
    dicc["negro"] = (0, 0, 0)
    dicc["verdeClaro"] = (218, 247, 166)
    dicc["verdeOscuro"] = (47, 159, 129)
    dicc["celeste"] = (174, 214, 241)
    dicc["naranjaPalido"] = (255, 195, 0)
    dicc["naranja"] = (255, 87, 51)
    return dicc
