import pygame
import time
from math import sin, cos, pi

def calcularVerticesPoligono(numLados:int, xCentro:float, yCentro:float, distanciaRadial:float):
    '''Calcula las posiciones en que se encuentran los vertices de un polígono. 
    Recibe como parámetro el número de lados del polígono, las coordenadas de su centro y la distancia del centro a uno de los vertices'''
    listaCoords=[]
    for i in range(numLados):
        xVertice=xCentro+distanciaRadial*(cos(2*pi*i/numLados))
        yVertice=yCentro+distanciaRadial*(sin(2*pi*i/numLados))
        listaCoords.append([xVertice,yVertice])
    return listaCoords

def ubicarJugadores(listaCoords:list, pantalla:pygame.surface.Surface):
    '''Ubica a cada jugador en lugar que le corresponde en la ventana. 
    Recibe las coordenadas en que debe ir ubicado cada uno de los jugadores'''
    # Dibujar los círculos en la ventana
    color = (220, 30, 120)
    radioCirculo = 40
    for i in range(numJugadores):
        pygame.draw.circle(pantalla, color, listaCoords[i], radioCirculo)
    # Actualizar la ventana
    pygame.display.update()

def refrescarJuego(listaCoords:list, pantalla:pygame.surface.Surface, colorPapa:tuple, coordsPapa:pygame.math.Vector2, radioPapa: float):
    '''Refresca el juego cada segundo para mantener los elementos gráficos actualizados'''
    pantalla.fill("darkgray")
    ubicarJugadores(listaCoords,pantalla)
    pygame.draw.circle(pantalla, colorPapa, coordsPapa, radioPapa)
    pygame.display.update()

# Valores iniciales
numJugadores = 8
distanciaEntreJugadores = 170
distanciaRadial = distanciaEntreJugadores/(2*sin(pi/numJugadores))
ancho = 1280
alto = 720
listaCoords=calcularVerticesPoligono(numJugadores, ancho/2, alto/2, distanciaRadial)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ancho, alto))

# Definir funcionamiento del reloj
reloj = pygame.time.Clock()

vectoresPorGraficar=0

personaPapa=0
coordsPapa=pygame.math.Vector2(listaCoords[personaPapa])
colorPapa=(191, 142, 61, 0.8)
radioPapa=20

# Mantener la ventana abierta hasta que el usuario la cierre
running=True
while running:

    prevPersonaPapa=personaPapa

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif vectoresPorGraficar==0 and event.type ==pygame.KEYDOWN:
            personaPapa+=1
            if personaPapa>=numJugadores:
                personaPapa%=numJugadores

    if vectoresPorGraficar>0:
        vectoresPorGraficar-=1
        coordsPapa+=vectorDireccion
        refrescarJuego(listaCoords, pantalla, colorPapa, coordsPapa, radioPapa) 
        if vectoresPorGraficar==0:
            fin=time.time()
            print(fin-inicio)
    elif prevPersonaPapa!=personaPapa:
        inicio=time.time()
        vectoresPorGraficar=30
        coordsPrev=listaCoords[prevPersonaPapa]
        coordsActual=listaCoords[personaPapa]
        vectorX=(coordsActual[0]-coordsPrev[0])/vectoresPorGraficar
        vectorY=(coordsActual[1]-coordsPrev[1])/vectoresPorGraficar
        vectorDireccion=pygame.Vector2(vectorX, vectorY)
    else:
        refrescarJuego(listaCoords, pantalla, colorPapa, coordsPapa, radioPapa) 

    reloj.tick(30)

