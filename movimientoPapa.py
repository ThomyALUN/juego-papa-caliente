import pygame
import time
from math import sin, cos, pi

from estructuras import Queue
from funciones import calcularVerticesPoligono

DEFAULT_COLORS=["aqua","blueviolet","chartreuse4","chocolate2","crimson","darkorchid","darksalmon", "khaki3","lightpink4","limegreen"]

class JuegoPapa:

    def __init__(self, ancho:int=1280, alto:int=720, tamanioTitulo:int=50, tamanioNombres:int=30, 
                distanciaJugadores:int=120, colorPapa:tuple=(191, 142, 61, 0.8), radioPapa:int=10,
                rutaFondoJuego:str="multimedia/images/fondoJuego.jpg"):
        self._ancho = ancho
        self._alto = alto
        self.numJugadores = None
        self.nombreJugador = None
        self.distanciaJugadores = distanciaJugadores
        self.distanciaRadial = None
        self.coordsPapa=None
        self.personaPapa=None
        self.colorPapa=colorPapa
        self.radioPapa=radioPapa
        self.vectoresPorGraficar=0

        self.colaCoords = Queue()
        self.colaJugadores = Queue()

        # Inicializar Pygame
        pygame.init()
        pygame.display.set_caption("Juego de la papa caliente")
        self.pantalla = pygame.display.set_mode((self._ancho, self._alto))
        self.reloj = pygame.time.Clock()
        self.fondoJuego = pygame.image.load(rutaFondoJuego)

        self.diccFuentes={}
        self.configurarFuente("titulo", tamanioTitulo)
        self.configurarFuente("nombres", tamanioNombres)
        self.generarTitulo()


    def setNombreJugador(self, nombreJugador:str):
        self.vaciarCola()
        self.nombreJugador=nombreJugador
        self.colaJugadores.enqueue(nombreJugador)

    def setNumJugadores(self, numJugadores:int):
        if numJugadores>2:
            self.numJugadores=numJugadores
            self.llenarColaNombres()
            self.colaJugadores.show()
            self.distanciaRadial = self.distanciaJugadores/(2*sin(pi/self.numJugadores))
            listaCoords=calcularVerticesPoligono(self.numJugadores, self._ancho/2, self._alto/2, self.distanciaRadial)
            self.colaCoords=Queue()
            for item in listaCoords:
                self.colaCoords.enqueue(item)
            self.colaCoordsGrafica=self.colaCoords.copy()
            self.colaCoords.show()
            self.personaPapa=self.colaJugadores.peek()
            self.coordsPapa=pygame.math.Vector2(self.colaCoords.peek())
            self.coordsActual=self.colaCoords.peek()
        else:
            self.numJugadores=None

    def vaciarCola(self):
        self.colaJugadores=Queue()

    def llenarColaNombres(self):
        listaJugadores = ["Thomas2", "Pepe2", "Juan2", "Sofía2", "Carlos2", "Manuela2", "Juan2", "María2", "Aleja2", "Jose2"]
        for i in range(self.numJugadores-1):
            self.colaJugadores.enqueue(listaJugadores[i])
        self.colaJugadoresGrafica=self.colaJugadores.copy()

    def configurarFuente(self, nombreFuente:str, tamanio:int):
        self.diccFuentes[nombreFuente] = pygame.font.Font(None, tamanio)

    def ubicarJugadores(self):
        '''Ubica a cada jugador en lugar que le corresponde en la ventana'''
        radioCirculo = 30
        for i in range(self.numJugadores):
            coordsJugActual=self.colaCoordsGrafica.dequeue()
            self.colaCoordsGrafica.enqueue(coordsJugActual)
            nombreActual=self.colaJugadoresGrafica.dequeue()
            self.colaJugadoresGrafica.enqueue(nombreActual)
            texto = self.diccFuentes["nombres"].render(nombreActual, True, (20, 20, 20)) 
            vectorDireccion=pygame.math.Vector2( [coordsJugActual[0] - (self._ancho/2), coordsJugActual[1] - (self._alto/2)] )
            vectorDireccion=vectorDireccion.normalize()
            vectorDireccion.x*=70
            vectorDireccion.y*=60
            rectanguloTexto = texto.get_rect()
            rectanguloTexto.centerx = (coordsJugActual[0] + vectorDireccion.x)
            rectanguloTexto.centery = (coordsJugActual[1] + vectorDireccion.y)
            pygame.draw.circle(self.pantalla, DEFAULT_COLORS[i], coordsJugActual, radioCirculo)
            pygame.draw.circle(self.pantalla, (0,0,0), coordsJugActual, radioCirculo+4, 4)
            self.pantalla.blit(texto, rectanguloTexto)


    def refrescarJuego(self):
        '''Refresca el juego cada segundo para mantener los elementos gráficos actualizados'''
        tamanioImagen=[self.fondoJuego.get_width(), self.fondoJuego.get_height()]
        if self._ancho >= (tamanioImagen[0] + 180) and self._alto >= (tamanioImagen[1] + 180):
            posImagen = [ 
                        (self._ancho - tamanioImagen[0])/2, 
                        (self._alto - tamanioImagen[1])/2
                        ]
            self.pantalla.blit(self.fondoJuego, (posImagen))
        self.ponerTitulo()
        self.ubicarJugadores()
        pygame.draw.circle(self.pantalla, self.colorPapa, self.coordsPapa, self.radioPapa)
        pygame.display.update()

    def generarTitulo(self):
        '''Se genera el título en la pantalla donde se ejecuta el juego'''
        self.textoTitulo = self.diccFuentes["titulo"].render("Juego de la papa caliente", True, (250, 250, 250, 0.4))
        self.rectanguloTitulo = self.textoTitulo.get_rect()
        self.rectanguloTitulo.centerx = self.pantalla.get_rect().centerx
        self.rectanguloTitulo.centery = 50

    def ponerTitulo(self):
        self.pantalla.blit(self.textoTitulo, self.rectanguloTitulo)

    def cicloPrincipal(self):
        # Mantener la ventana abierta hasta que el usuario la cierre
        running=True
        self.ponerTitulo()
        while running:
            self.prevPersonaPapa=self.personaPapa
            self.coordsPrev=self.coordsActual
            if self.vectoresPorGraficar==0 and self.nombreJugador!=self.personaPapa: 
                pygame.time.wait(500)
                self.personaPapa=self.colaJugadores.dequeue()
                self.colaJugadores.enqueue(self.personaPapa)
                self.coordsActual=self.colaCoords.dequeue()
                self.colaCoords.enqueue(self.coordsActual)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                elif (self.vectoresPorGraficar==0 and self.nombreJugador==self.personaPapa 
                    and self.nombreJugador==self.prevPersonaPapa and event.type==pygame.KEYDOWN
                    and event.key==pygame.K_SPACE):
                    self.personaPapa=self.colaJugadores.dequeue()
                    self.colaJugadores.enqueue(self.personaPapa)
                    self.coordsActual=self.colaCoords.dequeue()
                    self.colaCoords.enqueue(self.coordsActual)

            if self.vectoresPorGraficar>0:
                self.vectoresPorGraficar-=1
                self.coordsPapa+=vectorDireccion
                self.refrescarJuego() 
                if self.vectoresPorGraficar==0:
                    fin=time.time()
                    print(fin-inicio)
            elif self.prevPersonaPapa!=self.personaPapa:
                inicio=time.time()
                self.vectoresPorGraficar=35
                vectorX=(self.coordsActual[0]-self.coordsPrev[0])/self.vectoresPorGraficar
                vectorY=(self.coordsActual[1]-self.coordsPrev[1])/self.vectoresPorGraficar
                vectorDireccion=pygame.Vector2(vectorX, vectorY)
            else:
                self.refrescarJuego() 
            self.reloj.tick(40)

if __name__=="__main__":
    juego=JuegoPapa()
    juego.setNombreJugador("Thomas")
    juego.setNumJugadores(5)
    juego.cicloPrincipal()

