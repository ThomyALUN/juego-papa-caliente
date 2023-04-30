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
    sprite.setEscala(40, 45)
    listaSprites.append(sprite)

"""Inicializa variables
La variable spriteActual (que almacena el índice del sprite actualmente seleccionado) y sprite_font 
(que contiene una fuente de letra para dibujar el símbolo ">" que indica qué sprite está seleccionado).
"""
spriteActual = 0
sprite_font = pygame.font.SysFont("Arial", 24)

def sel_sprite():
    """Esta funcion permite que el usuario seleccione un sprite de una lista de sprites disponibles. 
    La función muestra una lista de sprites y resalta el sprite seleccionado actualmente con un ">" al lado. 
    El usuario puede moverse hacia arriba o hacia abajo en la 
    lista utilizando las teclas de flecha arriba y abajo, 
    y puede seleccionar el sprite presionando la tecla "Enter.
    
    No recibe ningun parametro. 
    Retorna la ruta del sprite y su imagen"""
    global spriteActual
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    spriteActual = (spriteActual-1)%len(listaSprites)
                elif event.key == pygame.K_DOWN:
                    spriteActual = (spriteActual+1)%len(listaSprites)
                elif event.key == pygame.K_RETURN:
                    sprite_seleccionado = listaSprites[spriteActual].rutaImagen
                    return sprite_seleccionado

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
        for i in range(len(listaSprites)):
            # Calcula la posición vertical para cada sprite
            if i < len(listaSprites)//2:
                y_pos = 30+i*50
                x_pos = 200
            else:
                y_pos = 30+(i-len(listaSprites)//2)*50
                x_pos = 450
            if i == spriteActual:
                text = sprite_font.render(">", True, BLACK)
                # Agrega una cantidad adicional a la posición vertical del texto
                screen.blit(text, (x_pos-50, y_pos))
            listaSprites[i].setXY(x_pos, y_pos)
            listaSprites[i].posInicial()
        pygame.display.flip()


ruta_sprite_elegido = sel_sprite()
done = False
while not done:
    """Después de que el usuario selecciona un sprite, 
    el código entra en un bucle principal que muestra el sprite en la pantalla. 
    El bucle principal se ejecuta hasta que el usuario cierre la ventana de pygame."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(WHITE)
    if ruta_sprite_elegido:
        sprite_elegido = pygame.image.load(ruta_sprite_elegido)
        screen.blit(sprite_elegido, (50, 50))
    pygame.display.flip()

print("La ruta es:", ruta_sprite_elegido) #Imprime la ruta del sprite seleccionado por el usuario en la consola y cierra pygame.
          
# Cierra pygame
pygame.quit()
