"""Este código usa la biblioteca Pygame para mostrar una lista de sprites en la pantalla 
y permitir que el usuario seleccione uno de ellos. 
Luego, muestra el sprite seleccionado en la pantalla y finalmente cierra Pygame"""

"""Importa la biblioteca Pygame, 
así como dos módulos personalizados llamados funciones y ControlSprite."""
import pygame
from funciones import *
from ControlSprite import *


# Define los colores en formato RGB: Negro y Blanco

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicializa pygame
pygame.init()

# Crea la pantalla con reslucion de 900*540 pixeles
screen = pygame.display.set_mode((900, 540))

"""Busca todos los sprites en la carpeta "sprites" 
utilizando una función importada del modulo funciones llamada buscarSprites. 
Luego, instancia un objeto de la clase ControlSprite para cada sprite 
y los almacena en una lista llamada listaSprites."""
rutasSprites = buscarSprites("sprites")
listaSprites = []
for ruta in rutasSprites:
    sprite = ControlSprite(ruta, screen, x=300, y=200)
    sprite.setEscala(50, 55)
    listaSprites.append(sprite)

"""Inicializa variables
La variable spriteActual (que almacena el índice del sprite actualmente seleccionado) y sprite_font 
(que contiene una fuente de letra para dibujar el símbolo ">" que indica qué sprite está seleccionado).
"""

sprite_font = pygame.font.SysFont("Arial", 24)

def sel_sprite():
    """Esta funcion permite que el usuario seleccione un sprite de una lista de sprites disponibles. 
    La función muestra una lista de sprites y resalta el sprite seleccionado actualmente con un ">" al lado. 
    El usuario puede moverse hacia arriba o hacia abajo en la 
    lista utilizando las teclas de flecha arriba y abajo, 
    y puede seleccionar el sprite presionando la tecla "Enter.
    
    No recibe ningun parametro. 
    Retorna la ruta del sprite y su imagen"""
    spriteActual = 0
    running = True
    seleccionado=False
    while running:
        if not seleccionado:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        spriteActual = (spriteActual-1)%len(listaSprites)
                    elif event.key == pygame.K_DOWN:
                        spriteActual = (spriteActual+1)%len(listaSprites)
                    elif event.key == pygame.K_LEFT:
                        spriteActual = (spriteActual-len(listaSprites)//4)%len(listaSprites)
                    elif event.key == pygame.K_RIGHT:
                        spriteActual = (spriteActual+len(listaSprites)//4)%len(listaSprites)
                    elif event.key == pygame.K_RETURN:
                        ruta_sprite_elegido = listaSprites[spriteActual].rutaImagen
                        print("La ruta es:", ruta_sprite_elegido)
                        seleccionado=True

            screen.fill(WHITE)
            for i in range(len(listaSprites)):
                # Calcula la posición vertical para cada sprite
                if i < len(listaSprites)//4:
                    y_pos = screen.get_height()/4+i*55
                    x_pos = screen.get_width()//9*3
                elif i < 2*len(listaSprites)//4:
                    y_pos = screen.get_height()/4+(i-len(listaSprites)//4)*55
                    x_pos = screen.get_width()//9*4
                elif i < 3*len(listaSprites)//4:
                    y_pos = screen.get_height()/4+(i-2*len(listaSprites)//4)*55
                    x_pos = screen.get_width()//9*5
                else:
                    y_pos = screen.get_height()/4+(i-3*len(listaSprites)//4)*55
                    x_pos = screen.get_width()//9*6
                if i == spriteActual:
                    text = sprite_font.render(">", True, BLACK)
                    # Agrega una cantidad adicional a la posición vertical del texto
                    screen.blit(text, (x_pos-50, y_pos-10))
                listaSprites[i].setXY(x_pos, y_pos)
                listaSprites[i].posInicial()
            pygame.display.flip()
        else:
            """Después de que el usuario selecciona un sprite, 
            el código entra en un bucle principal que muestra el sprite en la pantalla. 
            El bucle principal se ejecuta hasta que el usuario cierre la ventana de pygame."""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        ruta_sprite_elegido = sel_sprite()
            screen.fill(WHITE)
            sprite_elegido = pygame.image.load(ruta_sprite_elegido)
            rectSprite=sprite_elegido.get_rect()
            rectSprite.center=(screen.get_width()//2, screen.get_height()//2)
            screen.blit(sprite_elegido, rectSprite)
            pygame.display.flip()

sel_sprite()
