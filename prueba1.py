import pygame

pygame.init()
# colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
verdeClaro = (218, 247, 166)
verdeOscuro = (47, 159, 129)
celeste = (174, 214, 241)
naranjaPalido = (255, 195, 0)
naranja = (255, 87, 51)

# Configurar la ventana
window = pygame.display.set_mode((900, 540))
pygame.display.set_caption("Entradas de Texto")
background = pygame.image.load("fondoJuego.jpg").convert()
# dibujar la imagen en la supercicie
window.blit(background, [0, 0])


# boton play
def botonPlay(x, y, z, h):
    # crear rectangulos y agregar texto
    _play = pygame.draw.rect(window, naranjaPalido, (x, y, z, h))
    # cambiar color cuando haga click
    if _play.collidepoint(pygame.mouse.get_pos()):
        _play = pygame.draw.rect(window, verdeClaro, (x, y, z, h))
        play_ = pygame.font.Font(None, 80).render('PLAY', True, negro)
        window.blit(play_, ((x+(_play.width-play_.get_width())/2),
                    (y+(_play.height-play_.get_height())/2)))
    else:
        _play = pygame.draw.rect(window, naranjaPalido, (x, y, z, h))
        play_ = pygame.font.Font(None, 80).render('PLAY', True, negro)
        window.blit(play_, ((x+(_play.width-play_.get_width())/2),
                    (y+(_play.height-play_.get_height())/2)))
    return _play


# mensajes


def mensajes(mensaje, color, cordenadaX, cordenadaY, tamañoDeLetra):
    mensaje_final = pygame.font.Font(
        None, tamañoDeLetra).render(mensaje, True, color)
    return window.blit(mensaje_final, (cordenadaX, cordenadaY))


# rectangulo (pantalla, color, (margenIzquierda,margenArriba,ancho,alto))
def hacerRectMargen():
    pygame.draw.rect(window, naranja, (20, 20, 860, 10))
    pygame.draw.rect(window, naranja, (20, 510, 860, 10))
    pygame.draw.rect(window, naranja, (20, 20, 10, 500))
    pygame.draw.rect(window, naranja, (870, 20, 10, 500))


# Clase para la entrada de texto
class CajaTexto:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color(naranja)
        self.color_active = pygame.Color(negro)
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 60)
        self.active = False

    def manejarEvento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en la entrada de texto, activarla
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Cambiar el color de la entrada de texto
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pygame.KEYDOWN:
            # Si la entrada de texto está activa, agregar la tecla presionada al texto
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def actualizar(self):
        # Crear la superficie de texto y actualizar el rectángulo de la entrada de texto
        self.textoRenderizado = self.font.render(self.text, True, self.color)

    def dibujar(self):
        # Dibujar la entrada de texto en la superficie dada con su respectivo rectangulo
        pygame.draw.rect(window, (20, 20, 20), self.rect, 4)
        window.blit(self.textoRenderizado, (self.rect.x+(self.rect.width -
                    self.textoRenderizado.get_width())/2, self.rect.y+(self.rect.height-self.textoRenderizado.get_height())/2))


# Inicializar las entradas de texto
cajasTexto = [
    CajaTexto(600, 175, 220, 60),
    CajaTexto(600, 300, 220, 60),
]

y = 0
incrementoY = 0.3
x = 0
incremento = 0.1

# Bucle principal del juego
while True:
    # Manejar los eventos del juego
    for event in pygame.event.get():
        # Si el usuario hace clic en la X para cerrar la ventana
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Manejar eventos de entrada de teclado para cada entrada de texto
        for caja in cajasTexto:
            caja.manejarEvento(event)

        # chick en el boton
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if boton.collidepoint(pygame.mouse.get_pos()):
                print("funciona el click")

    # Actualizar las entradas de texto
    for caja in cajasTexto:
        caja.actualizar()

    # Dibujar la pantalla
    window.blit(background, [0, 0])
    hacerRectMargen()
    for caja in cajasTexto:
        caja.dibujar()
    x += incremento
    y += incrementoY
    if x < 0 or x > 35:
        incremento *= -1
    if y < 0 or y > 15:
        incrementoY *= -1
    mensajes('JUEGO DE LA PAPA HOT', negro, 50+x, 50+y, 90)
    mensajes('JUEGO DE LA PAPA HOT', naranja, 54+x, 54+y, 90)
    mensajes('JUEGO DE LA PAPA HOT', naranjaPalido, 58+x, 58+y, 90)
    mensajes('Jugadores que desea (3-10)',
             negro, 40, 178, 60)
    mensajes('Jugadores que desea (3-10)',
             negro, 41, 178, 60)
    mensajes('Nombre de su personaje',
             negro, 40, 303, 60)
    mensajes('Nombre de su personaje',
             negro, 40, 303, 60)
    pygame.draw.rect(window, negro, (326+x, 391+y, 200, 70))
    pygame.draw.rect(window, naranja, (320+x, 395+y, 200, 70))
    boton = botonPlay(314+x, 399+y, 200, 70)

    pygame.display.update()
