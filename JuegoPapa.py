import os
import time
import pygame
from random import randint
from math import sin, pi

from ControlSprite import ControlSprite
from estructuras import Queue
from funciones import calcularVerticesPoligono, nombresAleatorios, buscarSprites


class JuegoPapa:
    '''Clase que controla el funcionamiento del programa y del juego'''
    def __init__(self, ancho:int=1280, alto:int=720, distanciaJugadores:int=100, colorPapa:tuple=(191, 142, 61, 0.8), 
                radioPapa:int=10, vectores:int=40, rutaMusicaFondo:str="multimedia/music/backgroundSong.mp3", 
                rutaFondoJuego:str="multimedia/images/fondoJuego.jpg", rutaMusicaTitulo:str="multimedia/music/titleSong.wav",
                rutaMusicaDerrota:str="multimedia/music/defeatSong.mp3", rutaMusicaVictoria:str="multimedia/music/victorySong.wav"):
        '''Método constructor de la clase JuegoPapa. Establece los valores iniciales de las variables más importantes. 
        Todos sus parámetros son opcionales, para permitir una fácil modificación en caso de que se desee'''
        self._ancho=ancho
        self._alto=alto
        self.numJugadores=None
        self.nombreJugador=None
        self.nombreGanador=None
        self.rectsGanador=None
        self.textosGanador=None
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

        self.difX=0
        self.difY=0
        self.diccSprites = {}
        self.listaSprites = buscarSprites("sprites")
        self.listaPerdedores = []
        self.colaCoords = Queue()
        self.colaJugadores = Queue()

        # Inicializar Pygame
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            self.musicaEjecutable=False
        else:
            if any([not os.path.exists(self.musicaDerrota), not os.path.exists(self.musicaVictoria), 
                not os.path.exists(self.musicaFondo), not os.path.exists(self.musicaTitulo)]):
                self.musicaEjecutable=False
            else:
                self.musicaEjecutable=True
        pygame.display.set_caption("Juego de la papa caliente")
        self.pantalla = pygame.display.set_mode((self._ancho, self._alto))
        self.reloj = pygame.time.Clock()
        self.fondoJuego = pygame.image.load(rutaFondoJuego)

        self.diccFuentes={}
        self.configurarFuente("titulo", 50)
        self.configurarFuente("nombres", 30)
        self.configurarFuente("resultado", 40)
        self.configurarFuente("tituloPerdedores", 30)
        self.configurarFuente("nombrePerdedores", 25)
        self.generarTitulo()

    def llenarDiccSprites(self):
        '''Se encarga de seleccionar sprites de manera aleatoria para los jugadores'''
        colaCopia=self.colaJugadores.copy()
        for i in range(self.numJugadores):
            nombreJug=colaCopia.dequeue()
            contrldrSprite=ControlSprite(self.listaSprites[i], self.pantalla, None, None)
            self.diccSprites[nombreJug]=contrldrSprite

    def setNombreJugador(self, nombreJugador:str):
        '''Recibe como parámetro el nombre del jugador y lo asigna a un atributo de la instancia de la clase JuegoPapa'''
        self.vaciarColaJug()
        self.difX=0
        self.difY=0
        self.diccSprites={}
        self.listaPerdedores=[]
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
        '''Genera las coordenadas en las que deben ubicarse los jugadores en pantalla'''
        self.distanciaRadial = self.distanciaJugadores/(2*sin(pi/self.numJugadores))
        centroX=self._ancho/2+self.difX
        centroY=self._alto/2+self.difY
        listaCoords=calcularVerticesPoligono(self.numJugadores, centroX, centroY, self.distanciaRadial)
        self.colaCoords=Queue()
        for item in listaCoords:
            self.colaCoords.enqueue(item)
        self.colaCoordsGrafica=self.colaCoords.copy()
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
                self.listaPerdedores.append(jugador)
                self.difX=100
            else:
                self.colaJugadores.enqueue(jugador)
        print(self.listaPerdedores)
        self.numJugadores-=1
        self.generarCoordenadas()
        self.colaJugadoresGrafica=self.colaJugadores.copy()
        self.colaJugadores.show()

    def generarTiempoAleatorio(self):
        '''Genera un valor de tiempo aleatorio para que termine la ronda y salga un jugador'''
        inicioRonda=pygame.time.get_ticks()   
        duracion=randint(self.numJugadores*2, self.numJugadores*5)*1000 # Este valor debe estar en milisegundos 
        duracion=5000
        self.finRonda=inicioRonda+duracion
        print(duracion)
        self.tiempoGenerado=True

    def vaciarColaJug(self):
        '''Se encarga de vaciar la cola con los nombres de jugadores'''
        self.colaJugadores.clear()

    def llenarColaNombres(self):
        '''Se llena la cola de jugadores con nombres generados aleatoriamente'''
        listaJugadores = nombresAleatorios(self.numJugadores-self.colaJugadores.size())
        for i in range(len(listaJugadores)):
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
        for i in range(self.numJugadores):
            coordsJugActual=self.colaCoordsGrafica.dequeue()
            self.colaCoordsGrafica.enqueue(coordsJugActual)
            nombreActual=self.colaJugadoresGrafica.dequeue()
            self.colaJugadoresGrafica.enqueue(nombreActual)
            texto = self.diccFuentes["nombres"].render(nombreActual, True, (20, 20, 20)) 
            vectorDireccion=pygame.math.Vector2( [coordsJugActual[0] - (self._ancho/2+self.difX), coordsJugActual[1] - (self._alto/2)] )
            vectorDireccion=vectorDireccion.normalize()
            if abs(vectorDireccion.x)>=0.9:
                vectorDireccion.x*=90
            else:
                vectorDireccion.x*=75
            vectorDireccion.y*=60
            rectanguloTexto = texto.get_rect()
            rectanguloTexto.centerx = (coordsJugActual[0] + vectorDireccion.x)
            rectanguloTexto.centery = (coordsJugActual[1] + vectorDireccion.y)
            spriteJugador=self.diccSprites[nombreActual]
            spriteJugador.setXY(coordsJugActual[0], coordsJugActual[1])
            if self.vectoresPorGraficar>0 and nombreActual in self.jugadoresPase:
                if nombreActual==self.jugadoresPase[0]:
                    if self.vectorX>0:
                        spriteJugador.girarDerecha()
                    elif self.vectorX<0:
                        spriteJugador.girarIzquierda()
                    else:
                        spriteJugador.posInicial()
                elif nombreActual==self.jugadoresPase[1]:
                    if self.vectorX>0:
                        spriteJugador.girarIzquierda()
                    elif self.vectorX<0:
                        spriteJugador.girarDerecha()
                    else:
                        spriteJugador.posInicial()
            else:
                spriteJugador.posInicial()
            self.pantalla.blit(texto, rectanguloTexto)

    def generarGanador(self):
        '''Se encarga de generar los elementos gráficos de la sección donde se muestra al ganador'''
        self.nombreGanador=self.colaJugadores.peek()
        self.coordsGanador=((self._ancho/2+self.difX), self._alto/2)
        spriteJugador=self.diccSprites[self.nombreGanador]
        spriteJugador.setXY(self.coordsGanador[0], self.coordsGanador[1])
        textoNombre = self.diccFuentes["nombres"].render(self.nombreGanador, True, (20, 20, 20))
        subTitulo = self.diccFuentes["resultado"].render("El último jugador en pie es...", True, (20, 20, 20))
        if self.nombreJugador!=self.nombreGanador:
            resultado=self.diccFuentes["resultado"].render("¡Has perdido!", True, (20, 20, 20))
        else:
            resultado=self.diccFuentes["resultado"].render("¡Has ganado!", True, (20, 20, 20))
        self.textosGanador=(textoNombre, subTitulo, resultado)
        rectTxtNombre = textoNombre.get_rect()
        rectTxtNombre.center = ( (self._ancho/2+self.difX), (self._alto/2-100) )
        rectSubTitulo = subTitulo.get_rect()
        rectSubTitulo.center = ( (self._ancho/2+self.difX), (self._alto/2-200) )
        rectResultado = resultado.get_rect()
        rectResultado.center = ( (self._ancho/2+self.difX), (self._alto/2+150) )
        self.rectsGanador=(rectTxtNombre, rectSubTitulo, rectResultado)

    def mostrarGanador(self):
        '''Muestra los elementos gráficos de la sección del ganador en la ventana y pone la música de fondo'''
        try:
            if not pygame.mixer.music.get_busy():
                if self.nombreJugador!=self.nombreGanador:
                    self.ponerMusica(self.musicaDerrota)
                else:
                    self.ponerMusica(self.musicaVictoria)
        except pygame.error:
            pass
        self.ponerFondo()
        self.mostarPerdedores()
        self.pantalla.blit(self.textosGanador[1], self.rectsGanador[1])
        self.pantalla.blit(self.textosGanador[0], self.rectsGanador[0])
        self.pantalla.blit(self.textosGanador[2], self.rectsGanador[2])
        spriteJugador=self.diccSprites[self.nombreGanador]
        spriteJugador.posInicial()
        pygame.display.update() 

    def mostarPerdedores(self):
        '''Muestra los perdedores que han ido saliendo en orden'''
        cantPerd=len(self.listaPerdedores)
        if cantPerd>0:
            offsetY=-150+20*(self.numJugadores+cantPerd)
            tituloPerd=self.diccFuentes["tituloPerdedores"].render("Orden de salida", True, (20, 20, 20))
            rectTitPerd=tituloPerd.get_rect()
            rectTitPerd.center = ( (self._ancho/4 , self._alto/4 - offsetY) )
            self.pantalla.blit(tituloPerd, rectTitPerd)
            
            for i in range(cantPerd):
                nombreActual=self.listaPerdedores[i]
                coordY= self._alto/4 + (i+1)*50 - offsetY 
                mensaje=f"{i+1}. {nombreActual}"
                texto = self.diccFuentes["nombrePerdedores"].render(mensaje, True, (20, 20, 20))
                rectanguloTexto = texto.get_rect()
                rectanguloTexto.center = ( (self._ancho/4 - 40, coordY) )
                spriteJugador=self.diccSprites[nombreActual]
                spriteJugador.setXY(self._ancho/4 + 40, coordY)
                spriteJugador.setEscala(40,43)
                spriteJugador.posInicial()
                self.pantalla.blit(texto, rectanguloTexto)


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
        self.mostarPerdedores()
        pygame.draw.circle(self.pantalla, self.colorPapa, self.coordsPapa, self.radioPapa)
        pygame.display.update()

    def ponerMusica(self, archivo):
        if self.musicaEjecutable:
            try:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(archivo)
                pygame.mixer.music.play(-1)
            except pygame.error:
                pass

    def esperarCierre(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False

    def ponerTitulo(self):
        '''Pone en pantalla el título del juego según los parámetros definidos en el método generarTitulo()'''
        self.pantalla.blit(self.textoTitulo, self.rectanguloTitulo)

    def cicloPrincipal(self):
        '''Ciclo principal de ejecución del juego'''
        self.running=True
        self.ponerTitulo()
        self.ponerMusica(self.musicaFondo)
        while self.running:
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
                            try:
                                pygame.mixer.music.fadeout(1000)
                            except pygame.error:
                                pass
                            pygame.time.wait(500)
                            self.generarGanador()
                            self.esperarCierre()
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
                        self.running=False
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
                    self.vectorX=(self.coordsActual[0]-self.coordsPrev[0])/self.vectoresPorGraficar
                    self.vectorY=(self.coordsActual[1]-self.coordsPrev[1])/self.vectoresPorGraficar
                    vectorDireccion=pygame.Vector2(self.vectorX, self.vectorY)
                    self.jugadoresPase=[self.prevPersonaPapa, self.personaPapa]
                else:
                    self.refrescarJuego()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running=False
                
                self.mostrarGanador()
            self.reloj.tick(60)

if __name__=="__main__":
    juego=JuegoPapa()
    juego.musicaEjecutable=False
    juego.setNombreJugador("Carlitos")
    juego.setJugadores(8)
    juego.llenarDiccSprites()
    juego.cicloPrincipal()