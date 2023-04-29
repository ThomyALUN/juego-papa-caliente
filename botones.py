import pygame

pygame.init()
window = pygame.display.set_mode((900, 540))
pygame.display.set_caption("Entradas de Texto")


def crearVentana():
    # Configurar la ventana
    pygame.display.set_caption("Entradas de Texto")
    background = pygame.image.load("fondoJuego.jpg").convert()
    # dibujar la imagen en la supercicie
    window.blit(background, [0, 0])


def opacarVentana():
    # opaca la pantalla
    background = pygame.image.load("fondoJuego.jpg")
    backgroundClaro = background.convert_alpha()
    backgroundClaro.set_alpha(100)
    window.blit(backgroundClaro, [0, 0])


def crearRectangulo(x, y, w, h):
    rectangulo = pygame.draw.rect(window, self.naranjaPalido, (x, y, z, h))


class Boton:
    def __init__(self, x, y, w, h, mensaje, tamañoLetra):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mensaje = mensaje
        self.tamañoLetra = 80
        self.naranjaPalido = (255, 195, 0)
        self.naranja = (255, 87, 51)
        self.verdeClaro = (218, 247, 166)
        self.verdeOscuro = (47, 159, 129)
        self.negro = (0, 0, 0)

    def botonConTexto(self):
        # crear rectangulos y agregar texto
        self.boton = pygame.draw.rect(
            window, self.naranjaPalido, (self.x, self.y, self.w, self.h))
        # cambiar color cuando haga click
        if self.boton.collidepoint(pygame.mouse.get_pos()):
            self.boton = pygame.draw.rect(
                window, self.verdeClaro, (self.x, self.y, self.w, self.h))
            boton_ = pygame.font.Font(None, self.tamañoLetra).render(
                self.mensaje, True, self.negro)
            window.blit(boton_, ((self.x+(self.boton.width-boton_.get_width())/2),
                        (self.y+(self.boton.height-boton_.get_height())/2)))
        else:
            self.boton = pygame.draw.rect(
                window, self.naranjaPalido, (self.x, self.y, self.w, self.h))
            boton_ = pygame.font.Font(None, self.tamañoLetra).render(
                self.mensaje, True, self.negro)
            window.blit(boton_, ((self.x+(self.boton.width-boton_.get_width())/2),
                        (self.y+(self.boton.height-boton_.get_height())/2)))
        return self.boton


while True:
    opacarVentana()
    # Manejar los eventos del juego
    for event in pygame.event.get():
        # Si el usuario hace clic en la X para cerrar la ventana
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # chick en el boton
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if boton1.collidepoint(pygame.mouse.get_pos()):
                print("funciona el click")

    boton1 = Boton(400, 250, 300, 150, 'PLAY', 80).botonConTexto()

    pygame.display.update()
