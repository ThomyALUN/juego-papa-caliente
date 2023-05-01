import os
import time
import pygame
from random import randint, shuffle
from math import sin, pi

from estructuras import Queue
from subClasesPG import CajaTexto, Boton, ControlSprite
from funciones import calcularVerticesPoligono, nombresAleatorios, buscarSprites, generarDiccColores



class JuegoPapa:
    '''Clase que controla el funcionamiento del programa y del juego'''
    def __init__(self, ancho:int=900, alto:int=540, distanciaJugadores:int=100, colorPapa:tuple=(191, 142, 61, 0.8), 
                radioPapa:int=10, rutaMusicaFondo:str="multimedia/music/backgroundSong.mp3", 
                rutaFondoPpal:str="multimedia/images/fondoPpal.jpg",
                rutaFondoJuego:str="multimedia/images/fondoPtJuego.jpg", rutaMusicaTitulo:str="multimedia/music/titleSong.mp3",
                rutaMusicaDerrota:str="multimedia/music/defeatSong.mp3", rutaMusicaVictoria:str="multimedia/music/victorySong.mp3"):
        '''Método constructor de la clase JuegoPapa. Establece los valores iniciales de las variables más importantes. 
        Todos sus parámetros son opcionales, para permitir una fácil modificación en caso de que se desee'''
        self.debug=False
        self.dificultad=0
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
        self.vectores=50
        self.vectoresPorGraficar=0
        self.musicaFondo=rutaMusicaFondo
        self.musicaTitulo=rutaMusicaTitulo
        self.musicaDerrota=rutaMusicaDerrota
        self.musicaVictoria=rutaMusicaVictoria

        self.modo=0 # 0 -> Pantalla inicio, 1 -> Jugando, 2 -> Pantalla de pausa

        self.difX=0
        self.difY=0
        self.diccColores=generarDiccColores()
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
        self.fondoPpal = pygame.image.load(rutaFondoPpal)
        self.textoSelector = pygame.font.SysFont("Arial", 24).render(">", True, (0,0,0))

        self.cajaNumJug=CajaTexto(600, 175, 220, 60, self.pantalla)
        self.cajaNombre=CajaTexto(600, 300, 220, 60, self.pantalla)
        self.cajasTexto = [self.cajaNumJug, self.cajaNombre]

        self.diccFuentes={}
        self.configurarFuente("titulo", 50)
        self.configurarFuente("nombres", 30)
        self.configurarFuente("resultado", 40)
        self.configurarFuente("tituloPerdedores", 30)
        self.configurarFuente("nombrePerdedores", 25)
        self.configurarFuente("indicaciones", 28)
        self.generarTitulos()
        self.generarBotones()
        self.generarIndicaciones()


    def configDificultad(self, nivel:int):
        '''Cambia el nivel de dificultad del juego. Recibe como parámetro el nuevo nivel de dificultad.'''
        # 0 -> Fácil,
        # 1 -> Estándar/Normal,
        # 2 -> Díficil
        self.dificultad=nivel
        if self.dificultad==0:
            self.vectores=50
        elif self.dificultad==1:
            self.vectores=35
        else:
            self.vectores=20

    def iniciarJuego(self):
        '''Se encarga de iniciar el funcionamiento del juego como tal, mostrando los personajes,
        la papa y sus respectivas animaciones'''
        nombre=self.cajaNombre.texto
        numJug=self.cajaNumJug.texto
        if nombre!="" and numJug!="":
            try:
                int(numJug)
            except ValueError:
                pass
            else:
                if int(numJug)>=3 and int(numJug)<=10:
                    self._ancho=1280
                    self._alto=720
                    self.setNombreJugador(nombre)
                    self.numJugadores=int(numJug)
                    self.pantSelecSprite()
                    self.setSpriteJug(self.rutaSpriteElegido)
                    if self.spriteSeleccionado:
                        self.selecNivel()
                        if self.nivelSeleccionado:
                            self.modo=1
                            self.setJugadores(self.numJugadores)
                            self.llenarDiccSprites()
                            pygame.display.set_mode((1280,720))
                            self.ponerMusica(self.musicaFondo)
                            self.ponerFondo(self.fondoJuego)
                            
                            self.ponerTitulo(0)
                            pygame.display.update()

    def pausarJuego(self):
        '''Se encarga de poner el juego en un estado de pausa'''
        self.modo=2
        if self.musicaEjecutable:
            pygame.mixer.music.pause()
        self.duracionRest=self.finRonda-pygame.time.get_ticks()
        print(self.duracionRest)

    def reanudarJuego(self):
        '''Se encarga de reanudar el juego desde el estado de pausa'''
        self.modo=1
        if self.musicaEjecutable:
            pygame.mixer.music.unpause()
        self.finRonda=pygame.time.get_ticks()+self.duracionRest+100
        print(self.finRonda)

    def volverMenuPpal(self):
        '''Se encarga de cerrar la sesión de juego y volver al menú principal'''
        self.modo=0
        self.ponerMusica(self.musicaTitulo)
        self.cajaNombre.texto=""
        self.cajaNumJug.texto=""
        self._ancho=900
        self._alto=540
        self.tiempoGenerado=False
        self.vectoresPorGraficar=0
        pygame.display.set_mode((900, 540))

    def generarBotones(self):
        '''Se encarga de cargar en memoria la información de varios de los botones 
        que serán mostrados durante el funcionamiento del programa'''
        self.botonPlay=Boton(314, 399, 200, 70, "Jugar", self.pantalla)
        self.botonPausa=Boton(1280/2-300, 720*3.65/4, 200, 30, "Pausa", self.pantalla, 30)
        self.botonPausa.centerx=1280/2-300
        self.botonReanudar=Boton(1280/4+200, 720*3.65/4, 200, 30, "Reanudar", self.pantalla, 30)
        self.botonReanudar.centerx=1280/2-300
        self.botonMenuPpal=Boton(1280/2+200, 720*3.65/4, 200, 30, "Menú principal", self.pantalla, 30)
        self.botonMenuPpal.centerx=1280/2+300
        self.botonFacil=Boton(375, 120, 150, 50, "Facil", self.pantalla, 30, "Calibri", (70,189,34), (237,128,19))
        self.botonEstandar=Boton(375, 220, 150, 50, "Estandar", self.pantalla, 30, "Calibri", (70,189,34), (237,128,19))
        self.botonDificil=Boton(375, 320, 150, 50, "Díficil", self.pantalla, 30, "Calibri", (70,189,34), (237,128,19))

    def setSpriteJug(self, rutaSprite:str):
        '''Se selecciona el sprite del jugador. 
        Recibe como parámetro la ruta del archivo que contiene el mapa del sprite'''
        self.spriteJugador=rutaSprite
        contrldrSprite=ControlSprite(self.spriteJugador, self.pantalla, None, None)
        self.diccSprites[self.nombreJugador]=contrldrSprite

    def selecNivel(self):
        '''Genera la interfaz en la cuál el usuario puede seleccionar el nivel de dificultad deseado'''
        running=True
        self.nivelSeleccionado=False
        botonesNivel=[self.botonFacil, self.botonEstandar, self.botonDificil]
        botonSeleccionado=0
        while running and not self.nivelSeleccionado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.botonFacil.collidepoint(pygame.mouse.get_pos()):
                        self.nivelSeleccionado=True
                        self.configDificultad(0)
                    elif self.botonEstandar.collidepoint(pygame.mouse.get_pos()):
                        self.nivelSeleccionado=True
                        self.configDificultad(1)
                    elif self.botonDificil.collidepoint(pygame.mouse.get_pos()):
                        self.nivelSeleccionado=True
                        self.configDificultad(2)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        running=False
                    elif event.key == pygame.K_UP:
                        botonSeleccionado=(botonSeleccionado - 1)%len(botonesNivel)
                    elif event.key == pygame.K_DOWN:
                        botonSeleccionado=(botonSeleccionado + 1)%len(botonesNivel)
                    elif event.key == pygame.K_RETURN:
                        self.nivelSeleccionado=True
                        self.configDificultad(botonSeleccionado)
            self.ponerFondo(self.fondoPpal)
            self.ponerTitulo(3)
            self.ponerIndicacion(0)
            self.ponerIndicacion(1)
            for i, boton in enumerate(botonesNivel):
                boton.mostrarBoton()
                if botonSeleccionado==i:
                    self.pantalla.blit(self.textoSelector, (boton.x-20, boton.y+10))
            pygame.display.flip()

    def llenarDiccSprites(self):
        '''Se encarga de seleccionar sprites de manera aleatoria para los jugadores'''
        colaCopia=self.colaJugadores.copy()
        colaCopia.dequeue()
        spritesRandom=self.listaSprites[:]
        spritesRandom.remove(self.spriteJugador)
        shuffle(spritesRandom)
        for i in range(self.numJugadores-1):
            nombreJug=colaCopia.dequeue()
            contrldrSprite=ControlSprite(spritesRandom[i], self.pantalla, None, None)
            self.diccSprites[nombreJug]=contrldrSprite

    def setNombreJugador(self, nombreJugador:str):
        '''Recibe como parámetro el nombre del jugador y lo asigna a un atributo de la instancia de la clase JuegoPapa'''
        self.vaciarColaJug()
        self.colaCoords.clear()
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

    def pantSelecSprite(self):
        """Esta funcion permite que el usuario seleccione un sprite de una lista de sprites disponibles. 
        La función muestra una lista de sprites y resalta el sprite seleccionado actualmente con un ">" al lado. 
        El usuario puede moverse hacia arriba o hacia abajo en la 
        lista utilizando las teclas de flecha arriba y abajo, 
        y puede seleccionar el sprite presionando la tecla "Enter.
        
        No recibe ningun parametro. 
        Retorna la ruta del sprite y su imagen"""

        ctrlsSprites=[]
        for ruta in self.listaSprites:
            sprite = ControlSprite(ruta, self.pantalla, x=300, y=200)
            sprite.setEscala(50, 55)
            ctrlsSprites.append(sprite)

        spriteActual = 0
        running = True
        self.spriteSeleccionado=False
        while running:
            if not self.spriteSeleccionado:
                for event in pygame.event.get():
                    if event.type== pygame.QUIT:
                        running = False
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            spriteActual = (spriteActual-1)%len(ctrlsSprites)
                        elif event.key == pygame.K_DOWN:
                            spriteActual = (spriteActual+1)%len(ctrlsSprites)
                        elif event.key == pygame.K_LEFT:
                            spriteActual = (spriteActual-len(ctrlsSprites)//4)%len(ctrlsSprites)
                        elif event.key == pygame.K_RIGHT:
                            spriteActual = (spriteActual+len(ctrlsSprites)//4)%len(ctrlsSprites)
                        elif event.key == pygame.K_RETURN:
                            self.rutaSpriteElegido = ctrlsSprites[spriteActual].rutaImagen
                            print("La ruta es:", self.rutaSpriteElegido)
                            self.spriteSeleccionado=True
                        elif event.key == pygame.K_BACKSPACE:
                            running=False

                self.ponerFondo(self.fondoPpal)
                self.ponerTitulo(1)
                self.ponerIndicacion(0)
                self.ponerIndicacion(1)
                for i in range(len(ctrlsSprites)):
                    # Calcula la posición vertical para cada sprite
                    if i < len(ctrlsSprites)//4:
                        y_pos = self.pantalla.get_height()/4+i*55
                        x_pos = self.pantalla.get_width()//9*3
                    elif i < 2*len(ctrlsSprites)//4:
                        y_pos = self.pantalla.get_height()/4+(i-len(ctrlsSprites)//4)*55
                        x_pos = self.pantalla.get_width()//9*4
                    elif i < 3*len(ctrlsSprites)//4:
                        y_pos = self.pantalla.get_height()/4+(i-2*len(ctrlsSprites)//4)*55
                        x_pos = self.pantalla.get_width()//9*5
                    else:
                        y_pos = self.pantalla.get_height()/4+(i-3*len(ctrlsSprites)//4)*55
                        x_pos = self.pantalla.get_width()//9*6
                    if i == spriteActual:
                        # Agrega una cantidad adicional a la posición vertical del texto
                        self.pantalla.blit(self.textoSelector, (x_pos-50, y_pos-10))
                    ctrlsSprites[i].setXY(x_pos, y_pos)
                    ctrlsSprites[i].posInicial()
                pygame.display.flip()
            else:
                """Después de que el usuario selecciona un sprite, 
                el código entra en un bucle que muestra el sprite en la pantalla."""
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running=False
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.spriteSeleccionado=False
                        elif event.key == pygame.K_RETURN:
                            running=False
                self.ponerFondo(self.fondoPpal)
                self.ponerTitulo(2)
                self.ponerIndicacion(1)
                sprite_elegido = pygame.image.load(self.rutaSpriteElegido)
                rectSprite=sprite_elegido.get_rect()
                rectSprite.center=(self.pantalla.get_width()//2, self.pantalla.get_height()//2)
                self.pantalla.blit(sprite_elegido, rectSprite)
                pygame.display.flip()

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
            jugador=self.colaJugadores.dequeue()
            if jugador==self.jugadorEliminado:
                self.listaPerdedores.append(jugador)
                self.difX=100
            else:
                self.colaJugadores.enqueue(jugador)
        print(self.listaPerdedores)
        self.numJugadores-=1
        self.generarCoordenadas()
        self.colaJugadoresGrafica=self.colaJugadores.copy()

    def generarTiempoAleatorio(self):
        '''Genera un valor de tiempo aleatorio para que termine la ronda y salga un jugador'''
        inicioRonda=pygame.time.get_ticks()   
        if not self.debug:
            duracion=randint(self.numJugadores*2, self.numJugadores*(5-self.dificultad))*1000 # Este valor debe estar en milisegundos 
        else:
            duracion=5000
        print(duracion)
        self.finRonda=inicioRonda+duracion
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

    def generarTitulos(self):
        '''Se generan varios de los títulos que serán mostrados a lo largo del juego, 
        estableciendo su texto y espacio en pantalla'''
        tituloPtJuego = self.diccFuentes["titulo"].render("Juego de la papa caliente", True, (250, 250, 250, 0.4))
        tituloSprites1 = self.diccFuentes["titulo"].render("Selecciona un sprite", True, (0, 0, 0, 0.4))
        tituloSprites2 = self.diccFuentes["titulo"].render("¿Estas seguro?", True, (0, 0, 0, 0.4))
        tituloDificultad = self.diccFuentes["titulo"].render("Selecciona una dificultad", True, (0, 0, 0, 0.4))
        self.listaTxtTit = [tituloPtJuego, tituloSprites1, tituloSprites2, tituloDificultad]

        rectTitPtJuego = tituloPtJuego.get_rect()
        rectTitPtJuego.centerx = 720
        rectTitPtJuego.centery = 50
        self.listaRectTit = [rectTitPtJuego]
        for i, texto in enumerate(self.listaTxtTit[1:]):
            rectTitulo = texto.get_rect()
            rectTitulo.centerx = 450
            rectTitulo.centery = 50
            self.listaRectTit.append(rectTitulo)

    def generarIndicaciones(self):
        mensaje1="Desplazate con las flechas direccionales"
        indicSprite1 = self.diccFuentes["indicaciones"].render(mensaje1, True, (0, 0, 0, 0.4))
        mensaje2="Si deseas continuar presiona ENTER y si deseas volver presiona RETORNO"
        indicSprite2 = self.diccFuentes["indicaciones"].render(mensaje2, True, (0, 0, 0, 0.4))
        self.listaIndic=[indicSprite1, indicSprite2]
        self.listaRectIndic=[]
        for i, texto in enumerate(self.listaIndic):
            rectIndic = texto.get_rect()
            rectIndic.centerx = 450
            rectIndic.centery = 440+40*i
            self.listaRectIndic.append(rectIndic)

    def ponerTitulo(self, numIndic:int):
        '''Pone en pantalla el título del juego según los parámetros definidos en el método generarTitulos()'''
        self.pantalla.blit(self.listaTxtTit[numIndic], self.listaRectTit[numIndic])

    def ponerIndicacion(self, numIndic:int):
        self.pantalla.blit(self.listaIndic[numIndic], self.listaRectIndic[numIndic])

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
            if nombreActual==self.nombreJugador:
                rectNombreJug = texto.get_rect()
                rectNombreJug.width+=10
                rectNombreJug.height+=8
                rectNombreJug.centerx = (coordsJugActual[0] + vectorDireccion.x)
                rectNombreJug.centery = (coordsJugActual[1] + vectorDireccion.y)
                pygame.draw.rect(self.pantalla, (200, 10, 10), rectNombreJug, 0, 10)
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
        self.ponerFondo(self.fondoJuego)
        self.ponerTitulo(0)
        self.mostarPerdedores()
        self.pantalla.blit(self.textosGanador[1], self.rectsGanador[1])
        self.pantalla.blit(self.textosGanador[0], self.rectsGanador[0])
        self.pantalla.blit(self.textosGanador[2], self.rectsGanador[2])
        spriteJugador=self.diccSprites[self.nombreGanador]
        spriteJugador.posInicial()
        pygame.display.update() 

    def mostarPerdedores(self):
        '''Muestra los perdedores en orden de salida'''
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
                if nombreActual==self.nombreJugador:
                    rectNombreJug = texto.get_rect()
                    rectNombreJug.width+=10
                    rectNombreJug.height+=4
                    rectNombreJug.center=(self._ancho/4 - 40, coordY)
                    pygame.draw.rect(self.pantalla, (200, 10, 10), rectNombreJug, 0, 10)
                self.pantalla.blit(texto, rectanguloTexto)

    def hacerRectMargenPpal(self):
        naranja=self.diccColores["naranja"]
        pygame.draw.rect(self.pantalla, naranja, (20, 20, 860, 10))
        pygame.draw.rect(self.pantalla, naranja, (20, 510, 860, 10))
        pygame.draw.rect(self.pantalla, naranja, (20, 20, 10, 500))
        pygame.draw.rect(self.pantalla, naranja, (870, 20, 10, 500))

    def mostrarMensaje(self, mensaje, color, cordenadaX, cordenadaY, tamañoDeLetra):
        mensaje_final = pygame.font.Font(None, tamañoDeLetra).render(mensaje, True, color)
        self.pantalla.blit(mensaje_final, (cordenadaX, cordenadaY))

    def ponerFondo(self, imagen:str):
        '''Carga la imagen de fondo y la pone en pantalla. 
        Recibe como parámetro la ruta de la imagen'''
        self.pantalla.fill((0,0,0))
        tamanioImagen=[imagen.get_width(), imagen.get_height()]
        posImagen = [ (self._ancho - tamanioImagen[0])/2, (self._alto - tamanioImagen[1])/2 ]
        self.pantalla.blit(imagen, (posImagen))

    def refrescarJuego(self):
        '''Refresca el juego cada segundo para mantener los elementos gráficos actualizados'''
        self.ponerFondo(self.fondoJuego)
        self.ponerTitulo(0)
        self.ubicarJugadores()
        self.mostarPerdedores()
        self.mostrarBotonesJuego() if self.modo==1 else self.mostrarBotonesPausa()
        print(f"Coordenadas papa: {self.coordsPapa}")
        pygame.draw.circle(self.pantalla, self.colorPapa, self.coordsPapa, self.radioPapa)
        pygame.draw.circle(self.pantalla, (0,0,0), self.coordsPapa, self.radioPapa, self.radioPapa//6)
        pygame.display.update()

    def mostrarMenuPpal(self):
        '''Se encarga de mostrar en pantalla varios de los elementos importantes
        de la pantalla de inicio del juego, como el titulo y el boton de jugar'''
        self.movX += self.incrementoMovX
        self.movY += self.incrementoMovY
        if self.movX < 0 or self.movX > 35:
            self.incrementoMovX *= -1
        if self.movY < 0 or self.movY > 15:
            self.incrementoMovY *= -1
        self.hacerRectMargenPpal()
        self.mostrarMensaje('JUEGO DE LA PAPA HOT', self.diccColores["negro"], 50+self.movX, 50+self.movY, 90)
        self.mostrarMensaje('JUEGO DE LA PAPA HOT', self.diccColores["naranja"], 54+self.movX, 54+self.movY, 90)
        self.mostrarMensaje('JUEGO DE LA PAPA HOT', self.diccColores["naranjaPalido"], 58+self.movX, 58+self.movY, 90)
        self.mostrarMensaje('Jugadores que desea (3-10)', self.diccColores["negro"], 40, 178, 60)
        self.mostrarMensaje('Nombre de su personaje', self.diccColores["negro"], 40, 303, 60)
        pygame.draw.rect(self.pantalla, self.diccColores["negro"], (326+self.movX, 391+self.movY, 200, 70),0,20)
        pygame.draw.rect(self.pantalla, self.diccColores["naranja"], (320+self.movX, 395+self.movY, 200, 70),0,20)
        self.botonPlay.desplazar(self.movX, self.movY)
        self.botonPlay.mostrarBoton()
        pygame.display.update()

    def mostrarBotonesJuego(self):
        '''Muestra en pantalla los botones de pausa y de menú principal mientras el usuario esta jugando'''
        self.botonPausa.mostrarBoton()
        self.botonMenuPpal.mostrarBoton()
    
    def mostrarBotonesPausa(self):
        '''Muestra en pantalla los botones de reanudar y de menú principal cuando se pausa el juego'''
        self.botonReanudar.mostrarBoton()
        self.botonMenuPpal.mostrarBoton()

    def ponerMusica(self, archivo:str):
        '''Pone la música de fondo.
        Recibe como parámetro la ruta donde se encuentra el archivo 
        que contiene el recurso de audio'''
        if self.musicaEjecutable:
            try:
                pygame.mixer.music.unload()
                pygame.mixer.music.load(archivo)
                pygame.mixer.music.play(-1)
            except pygame.error:
                pass

    def cicloPrincipal(self):
        '''Ciclo principal de ejecución del juego, en este suceden todos los eventos 
        y se muestran todas las ventanas relacionadas con el funcionamiento del juego.
        También se encarga de manejar los eventos generados por el usuario'''
        self.running=True
        self.modo=0
        self.ponerMusica(self.musicaTitulo)

        self.movY = 0
        self.incrementoMovY = 0.3
        self.movX = 0
        self.incrementoMovX = 0.1


        while self.running:
            self.reloj.tick(60)
            if self.modo==0:
                self.ponerFondo(self.fondoPpal)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running=False
                    for caja in self.cajasTexto:
                        caja.manejarEvento(event)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.botonPlay.collidepoint(pygame.mouse.get_pos()):
                            self.iniciarJuego()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.iniciarJuego()
                for caja in self.cajasTexto:
                    caja.actualizar()
                for caja in self.cajasTexto:
                    caja.dibujar()
                self.mostrarMenuPpal()
            elif self.modo==1:
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
                                    if self.musicaEjecutable:
                                        pygame.mixer.music.fadeout(1000)
                                except pygame.error:
                                    pass
                                pygame.time.wait(500)
                                self.generarGanador()
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
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if self.botonPausa.collidepoint(pygame.mouse.get_pos()):
                                self.pausarJuego()
                            if self.botonMenuPpal.collidepoint(pygame.mouse.get_pos()):
                                self.volverMenuPpal()
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
            elif self.modo==2:
                self.ponerFondo(self.fondoJuego)
                self.ponerTitulo(0)
                self.refrescarJuego()
                self.botonReanudar.mostrarBoton()
                self.botonMenuPpal.mostrarBoton()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running=False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.botonReanudar.collidepoint(pygame.mouse.get_pos()):
                            self.reanudarJuego()
                        if self.botonMenuPpal.collidepoint(pygame.mouse.get_pos()):
                            self.volverMenuPpal()