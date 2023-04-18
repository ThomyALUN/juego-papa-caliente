import pygame
import time
from random import randint
from math import sin, pi

from estructuras import Queue
from funciones import calcularVerticesPoligono

DEFAULT_COLORS=["aqua","blueviolet","chartreuse4","chocolate2","crimson","darkorchid","darksalmon", "khaki3","lightpink4","limegreen"]

class JuegoPapa:
    '''Clase que controla el funcionamiento del programa y del juego'''
    def __init__(self, ancho:int=1280, alto:int=720, tamanioTitulo:int=50, tamanioNombres:int=30, distanciaJugadores:int=120, 
                colorPapa:tuple=(191, 142, 61, 0.8), radioPapa:int=10, vectores=40, rutaMusicaFondo:str="multimedia/music/backgroundSong.mp3", 
                rutaFondoJuego:str="multimedia/images/fondoJuego.jpg", rutaMusicaTitulo:str="multimedia/music/titleSong.wav",
                rutaMusicaDerrota:str="multimedia/music/defeatSong.mp3", rutaMusicaVictoria:str="multimedia/music/victorySong.mp3"):
        '''Método constructor de la clase JuegoPapa. Establece los valores iniciales de las variables más importantes. 
        Todos sus parámetros son opcionales, para permitir una fácil modificación en caso de que se desee'''
        self._ancho=ancho
        self._alto=alto
        self.numJugadores=None
        self.nombreJugador=None
        self.distanciaJugadores=distanciaJugadores
        self.distanciaRadial=None
        self.coordsPapa=None
        self.personaPapa=None
        self.colorPapa=colorPapa
        self.radioPapa=radioPapa
        self.finRonda=None
        self.tiempoGenerado=False
        self.jugadorEliminado=None
        self.vectores=vectores
        self.vectoresPorGraficar=0
        self.musicaFondo=rutaMusicaFondo
        self.musicaTitulo=rutaMusicaTitulo
        self.musicaDerrota=rutaMusicaDerrota
        self.musicaVictoria=rutaMusicaVictoria

        self.colaCoords = Queue()
        self.colaJugadores = Queue()

        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Juego de la papa caliente")
        self.pantalla = pygame.display.set_mode((self._ancho, self._alto))
        self.reloj = pygame.time.Clock()
        self.fondoJuego = pygame.image.load(rutaFondoJuego)

        self.diccFuentes={}
        self.configurarFuente("titulo", tamanioTitulo)
        self.configurarFuente("nombres", tamanioNombres)
        self.generarTitulo()


    def setNombreJugador(self, nombreJugador:str):
        '''Recibe como parámetro el nombre del jugador y lo asigna a un atributo de la instancia de la clase JuegoPapa'''
        self.vaciarCola()
        self.nombreJugador=nombreJugador
        self.colaJugadores.enqueue(nombreJugador)

    def setJugadores(self, numJugadores:int):
        '''Recibe como parámetro el número de jugadores, lo guarda como un atributo 
        y genera nombres aleatorios para los jugadores extra (diferentes al personaje del jugador)'''
        if numJugadores>2:
            self.numJugadores=numJugadores
            self.llenarColaNombres()
            self.colaJugadores.show()
            self.generarCoordenadas()
        else:
            self.numJugadores=None

    def generarCoordenadas(self):
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

    def sacarJugador(self):
        '''Se encarga de eliminar a un jugador en el momento en que la papa deja de moverse'''
        print(f"El jugador a eliminar es {self.jugadorEliminado}")
        for i in range(self.numJugadores):
            self.colaJugadores.show()
            jugador=self.colaJugadores.dequeue()
            self.colaJugadores.show()
            if jugador==self.jugadorEliminado:
                pass
            else:
                self.colaJugadores.enqueue(jugador)
        self.numJugadores-=1
        self.generarCoordenadas()
        self.colaJugadoresGrafica=self.colaJugadores.copy()
        self.colaJugadores.show()

    def generarTiempoAleatorio(self):
        inicioRonda=pygame.time.get_ticks()   
        duracion=randint(self.numJugadores*2, self.numJugadores*4)*1000 # Este valor debe estar en milisegundos 
        self.finRonda=inicioRonda+duracion
        print(duracion)
        self.tiempoGenerado=True

    def vaciarCola(self):
        '''Se encarga de vaciar la cola con los nombres de jugadores'''
        self.colaJugadores.clear()

    def llenarColaNombres(self):
        '''Se llena la cola de jugadores con nombres generados aleatoriamente'''
        listaJugadores = ["Thomas2", "Pepe2", "Juan2", "Sofía2", "Carlos2", "Manuela2", "Juanita2", "María2", "Aleja2", "Jose2"]
        for i in range(self.numJugadores-self.colaJugadores.size()):
            self.colaJugadores.enqueue(listaJugadores[i])
        self.colaJugadoresGrafica=self.colaJugadores.copy()

    def configurarFuente(self, nombreFuente:str, tamanio:int):
        '''Genera una nueva fuente y la almacena en un diccionario.
        Recibe como parámetro el nombre y el tamaño que se le asignarán a la fuente'''
        self.diccFuentes[nombreFuente] = pygame.font.Font(None, tamanio)

    def generarTitulo(self):
        '''Se genera el título en la pantalla donde se ejecuta el juego'''
        self.textoTitulo = self.diccFuentes["titulo"].render("Juego de la papa caliente", True, (250, 250, 250, 0.4))
        self.rectanguloTitulo = self.textoTitulo.get_rect()
        self.rectanguloTitulo.centerx = self.pantalla.get_rect().centerx
        self.rectanguloTitulo.centery = 50

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

    def mostrarGanador(self):
        radioCirculo=30
        nombreActual=self.colaJugadores.peek()
        coordsJugActual=(self._ancho/2, self._alto/2)
        texto = self.diccFuentes["nombres"].render(nombreActual, True, (20, 20, 20))
        rectanguloTexto = texto.get_rect()
        rectanguloTexto.centerx = (self._ancho/2)
        rectanguloTexto.centery = (self._alto/2-100)
        if not pygame.mixer.music.get_busy():
            if self.nombreJugador!=nombreActual:
                self.ponerMusica(self.musicaDerrota)
            else:
                self.ponerMusica(self.musicaVictoria)
        self.ponerFondo()
        self.pantalla.blit(texto, rectanguloTexto)
        pygame.draw.circle(self.pantalla, DEFAULT_COLORS[0], coordsJugActual, radioCirculo)
        pygame.draw.circle(self.pantalla, (0,0,0), coordsJugActual, radioCirculo+4, 4)
        pygame.display.update() 

    def ponerFondo(self):
        tamanioImagen=[self.fondoJuego.get_width(), self.fondoJuego.get_height()]
        if self._ancho >= (tamanioImagen[0] + 180) and self._alto >= (tamanioImagen[1] + 180):
            posImagen = [ 
                        (self._ancho - tamanioImagen[0])/2, 
                        (self._alto - tamanioImagen[1])/2
                        ]
            self.pantalla.blit(self.fondoJuego, (posImagen))

    def refrescarJuego(self):
        '''Refresca el juego cada segundo para mantener los elementos gráficos actualizados'''
        self.ponerFondo()
        self.ubicarJugadores()
        pygame.draw.circle(self.pantalla, self.colorPapa, self.coordsPapa, self.radioPapa)
        pygame.display.update()

    def ponerMusica(self, archivo):
        pygame.mixer.music.unload()
        pygame.mixer.music.load(archivo)
        pygame.mixer.music.play(-1)


    def ponerTitulo(self):
        '''Pone en pantalla el título del juego según los parámetros definidos en el método generarTitulo()'''
        self.pantalla.blit(self.textoTitulo, self.rectanguloTitulo)

    def cicloPrincipal(self):
        '''Ciclo principal de ejecución del juego'''
        running=True
        self.ponerTitulo()
        self.ponerMusica(self.musicaFondo)
        while running:
            if self.numJugadores>1:
                if not self.tiempoGenerado:
                    self.generarTiempoAleatorio()
                elif self.vectoresPorGraficar==0:
                    tiempoActual=pygame.time.get_ticks()
                    if tiempoActual>self.finRonda:
                        self.jugadorEliminado=self.personaPapa
                        self.colaJugadores.show()
                        pygame.time.wait(3000)
                        self.sacarJugador()
                        self.jugadorEliminado=None
                        self.tiempoGenerado=False
                        self.finRonda=None
                        if self.numJugadores==1:
                            pygame.mixer.music.fadeout(1000)
                            pygame.time.wait(500)
                            continue

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
                    self.vectoresPorGraficar=self.vectores
                    vectorX=(self.coordsActual[0]-self.coordsPrev[0])/self.vectoresPorGraficar
                    vectorY=(self.coordsActual[1]-self.coordsPrev[1])/self.vectoresPorGraficar
                    vectorDireccion=pygame.Vector2(vectorX, vectorY)
                else:
                    self.refrescarJuego()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running=False
                
                self.mostrarGanador()
            self.reloj.tick(40)

if __name__=="__main__":
    juego=JuegoPapa()
    juego.setNombreJugador("Carlitos")
    juego.setJugadores(3)
    juego.cicloPrincipal()