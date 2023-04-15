import pygame
import time
from math import sin, cos, pi

def calcularVerticesPoligono(numLados:int, xCentro:float, yCentro:float, distanciaRadial:float):
    listaCoords=[]
    for i in range(numLados):
        xVertice=xCentro+distanciaRadial*(cos(2*pi*i/numLados))
        yVertice=yCentro+distanciaRadial*(sin(2*pi*i/numLados))
        listaCoords.append([xVertice,yVertice])
    return listaCoords

def ubicarJugadores(numJugadores:int, listaCoords:list):
    # Dibujar los círculos en la ventana
    color = (220, 30, 120)
    radioCirculo = 40
    for i in range(numJugadores):
        pygame.draw.circle(screen, color, listaCoords[i], radioCirculo)
    # Actualizar la ventana
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
screen = pygame.display.set_mode((ancho, alto))

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
        screen.fill("darkgray")
        ubicarJugadores(numJugadores, listaCoords)
        coordsPapa+=vectorDireccion
        pygame.draw.circle(screen, colorPapa, coordsPapa, radioPapa)
        pygame.display.update()
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
        print(vectorDireccion.magnitude())
    else:
        screen.fill("darkgray")
        ubicarJugadores(numJugadores, listaCoords)
        pygame.draw.circle(screen, colorPapa, coordsPapa, radioPapa)
        pygame.display.update()

    reloj.tick(30)

