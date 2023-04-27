import pygame
import sys
from pygame import *

# inicializar el juego
pygame.init()

# tamaño de la ventana
pantalla = pygame.display.set_mode((900, 540))

# colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
verdeClaro = (218, 247, 166)
verdeOscuro = (47, 159, 129)
celeste = (174, 214, 241)
naranjaPalido = (255, 195, 0)
naranja = (255, 87, 51)
# agregar color al fondo de pantalla
# pantalla.fill(verdeClaro)
# agregar imagen de fondo de pantalla
background = pygame.image.load("fondoJuego.jpg").convert()
# supercicie para dinujar la imagen
# background_pantalla = pygame.Surface((900, 600))
# dibujar la imagen en la supercicie
pantalla.blit(background, [0, 0])
# rectangulo (pantalla, color, (margenIzquierda,margenArriba,ancho,alto))
pygame.draw.rect(pantalla, naranja, (20, 20, 860, 10))
pygame.draw.rect(pantalla, naranja, (20, 510, 860, 10))
pygame.draw.rect(pantalla, naranja, (20, 20, 10, 500))
pygame.draw.rect(pantalla, naranja, (870, 20, 10, 500))

''' dimensiones del rectángulo de entrada de datos y mensaje '''
# Define la fuente para el texto de los rectangulos
fuente = pygame.font.Font(None, 62)

# mensaje principal
mensaje = 'JUEGO DE LA PAPA HOT'
mensaje_principal1 = pygame.font.Font(
    None, 80).render(mensaje, True, negro)

mensaje_principal2 = pygame.font.Font(
    None, 80).render(mensaje, True, naranja)

mensaje_principal3 = pygame.font.Font(
    None, 80).render(mensaje, True, naranjaPalido)


# rectangulo de numero de participantes
rectangulo_numero = pygame.Rect(700, 145, 100, 50)
# mensaje
mensajeNum = 'Digite la cantidad de jugadores que desea (2-10)'
mensaje_numero = pygame.font.Font(None, 38).render(mensajeNum, True, naranja)
# Define la cadena de texto de entrada vacía
texto_numero = ""

# rectangulo de numero de participantes
rectangulo_nombre = pygame.Rect(700, 245, 100, 50)
# mensaje
mensajeNom = 'Digite el nombre del jugador'
mensaje_nombre = pygame.font.Font(None, 38).render(mensajeNom, True, naranja)
# Define la cadena de texto de entrada vacía
texto_nombre = ""

# bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

        # Si el usuario presiona una tecla
        if evento.type == pygame.KEYDOWN:
            # Si la tecla es un número o una letra, agrega el carácter al texto de entrada
            if evento.unicode.isalnum():
                texto_numero += evento.unicode
            # Si la tecla es la tecla de retroceso, elimina el último carácter del texto de entrada
            elif evento.key == pygame.K_BACKSPACE:
                texto_numero = texto_numero[:-1]

        if evento.type == pygame.KEYDOWN:
            # Si la tecla es un número o una letra, agrega el carácter al texto de entrada
            if evento.unicode.isalnum():
                texto_nombre += evento.unicode
            # Si la tecla es la tecla de retroceso, elimina el último carácter del texto de entrada
            elif evento.key == pygame.K_BACKSPACE:
                texto_nombre = texto_nombre[:-1]

    pantalla.blit(mensaje_principal1, (80, 40))
    pantalla.blit(mensaje_principal2, (84, 44))
    pantalla.blit(mensaje_principal3, (88, 48))

    pantalla.blit(mensaje_numero, (40, 150))
    pygame.draw.rect(pantalla, negro, rectangulo_numero, 4)
    texto_superficie = fuente.render(texto_numero, True, negro)
    pantalla.blit(texto_superficie, (rectangulo_numero.x +
                  30, rectangulo_numero.y + 5))

    pantalla.blit(mensaje_nombre, (40, 250))
    pygame.draw.rect(pantalla, negro, rectangulo_nombre, 4)
    texto_superficie = fuente.render(texto_nombre, True, negro)
    pantalla.blit(texto_superficie, (rectangulo_nombre.x +
                  30, rectangulo_nombre.y + 5))

    # se va actualizando la pantalla
    pygame.display.update()
