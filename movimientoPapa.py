import pygame
import time
from math import sin, cos, pi

ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
DEFAULT_COLORS=["aqua","blueviolet","chartreuse4","chocolate2","crimson","darkorchid","darksalmon", "khaki3","lightpink4","limegreen"]

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

def ubicarJugadores(listaCoords:list, listaNombres:list, pantalla:pygame.surface.Surface):
    '''Ubica a cada jugador en lugar que le corresponde en la ventana. 
    Recibe las coordenadas en que debe ir ubicado cada uno de los jugadores'''
    radioCirculo = 30
    for i in range(numJugadores):
        coordsJugActual=listaCoords[i]
        texto = fuenteNombres.render(listaJugadores[i], True, (20, 20, 20)) 
        vectorDireccion=pygame.math.Vector2( [coordsJugActual[0] - (ANCHO_PANTALLA/2), coordsJugActual[1] - (ALTO_PANTALLA/2)] )
        vectorDireccion=vectorDireccion.normalize()
        vectorDireccion.x*=70
        vectorDireccion.y*=60
        rectanguloTexto = texto.get_rect()
        rectanguloTexto.centerx = (coordsJugActual[0] + vectorDireccion.x)
        rectanguloTexto.centery = (coordsJugActual[1] + vectorDireccion.y)
        pygame.draw.circle(pantalla, DEFAULT_COLORS[i], coordsJugActual, radioCirculo)
        pygame.draw.circle(pantalla, (0,0,0), coordsJugActual, radioCirculo+4, 4)
        pantalla.blit(texto, rectanguloTexto)


def refrescarJuego(listaCoords:list, listaNombres:list, pantalla:pygame.surface.Surface, colorPapa:tuple, coordsPapa:pygame.math.Vector2, radioPapa: float):
    '''Refresca el juego cada segundo para mantener los elementos gráficos actualizados'''
    tamanioImagen=[background_image.get_width(), background_image.get_height()]
    if ANCHO_PANTALLA >= (tamanioImagen[0] + 180) and ALTO_PANTALLA >= (tamanioImagen[1] + 180):
        posImagen = [ 
                    (ANCHO_PANTALLA - tamanioImagen[0])/2, 
                    (ALTO_PANTALLA - tamanioImagen[1])/2
                    ]
        pantalla.blit(background_image, (posImagen))
    titulo(pantalla)
    ubicarJugadores(listaCoords, listaNombres, pantalla)
    pygame.draw.circle(pantalla, colorPapa, coordsPapa, radioPapa)
    pygame.display.update()

def titulo(pantalla:pygame.surface.Surface, titulo:str="Juego de la papa caliente"):
    '''Se genera el título en la pantalla donde se ejecuta el juego'''
    texto = fuenteTitulo.render(titulo, True, (250, 250, 250, 0.4))    # El segundo parámetro activa o desactiva el AntiAliasing
    # Obtiene el rectángulo que delimita el área ocupada por el texto
    rectanguloTexto = texto.get_rect()

    rectanguloTexto.centerx = pantalla.get_rect().centerx
    rectanguloTexto.centery = 50

    pantalla.blit(texto, rectanguloTexto)

# Valores iniciales
numJugadores = 4
listaJugadores = ["Thomas", "Pepe", "Juan", "Sofía", "Carlos", "Manuela", "Juan", "María", "Aleja", "Jose"]
distanciaEntreJugadores = 120
distanciaRadial = distanciaEntreJugadores/(2*sin(pi/numJugadores))
tamanioTitulo = 50
tamanioNombres = 30
listaCoords=calcularVerticesPoligono(numJugadores, ANCHO_PANTALLA/2, ALTO_PANTALLA/2, distanciaRadial)

# Inicializar Pygame
pygame.init()
background_image = pygame.image.load("multimedia/images/parque.jpg")
pygame.display.set_caption("Juego de la papa caliente")
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
fuenteTitulo = pygame.font.Font(None, tamanioTitulo)
fuenteNombres = pygame.font.Font(None, tamanioNombres)

# Definir funcionamiento del reloj
reloj = pygame.time.Clock()

vectoresPorGraficar=0

personajeUsuario=0
personaPapa=0
coordsPapa=pygame.math.Vector2(listaCoords[personaPapa])
colorPapa=(191, 142, 61, 0.8)
radioPapa=10

# Mantener la ventana abierta hasta que el usuario la cierre
running=True
titulo(pantalla)
while running:

    prevPersonaPapa=personaPapa
    if vectoresPorGraficar==0 and personajeUsuario!=personaPapa: 
        pygame.time.wait(500)
        personaPapa+=1
        personaPapa%=numJugadores

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif vectoresPorGraficar==0 and personajeUsuario==personaPapa and personajeUsuario==prevPersonaPapa and event.type ==pygame.KEYDOWN:
            personaPapa+=1
            personaPapa%=numJugadores

    if vectoresPorGraficar>0:
        vectoresPorGraficar-=1
        coordsPapa+=vectorDireccion
        refrescarJuego(listaCoords, listaJugadores, pantalla, colorPapa, coordsPapa, radioPapa) 
        if vectoresPorGraficar==0:
            fin=time.time()
            print(fin-inicio)
    elif prevPersonaPapa!=personaPapa:
        inicio=time.time()
        vectoresPorGraficar=35
        coordsPrev=listaCoords[prevPersonaPapa]
        coordsActual=listaCoords[personaPapa]
        vectorX=(coordsActual[0]-coordsPrev[0])/vectoresPorGraficar
        vectorY=(coordsActual[1]-coordsPrev[1])/vectoresPorGraficar
        vectorDireccion=pygame.Vector2(vectorX, vectorY)
    else:
        refrescarJuego(listaCoords, listaJugadores, pantalla, colorPapa, coordsPapa, radioPapa) 

    reloj.tick(40)

