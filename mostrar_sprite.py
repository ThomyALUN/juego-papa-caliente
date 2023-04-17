import pygame
import sys
# Inicializar pygame
pygame.init()

# Definir el tamaño de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Cargar la imagen de sprites
sprite_sheet = pygame.image.load("juego-papa-caliente/32_Characters/Males/M_02.png").convert_alpha()

# Definir las dimensiones de cada sprite    
sprite_width = 64
sprite_height = 68

# Función para mostrar un sprite en la pantalla
def draw_sprite(row, column):
    sprite_rect = pygame.Rect(column * sprite_width, row * sprite_height, sprite_width, sprite_height)
    sprite_image = sprite_sheet.subsurface(sprite_rect)
    screen.blit(sprite_image, (column * sprite_width, row * sprite_height)) #Copia una superficie en otra superficie

# Mostrar algunos sprites en la pantalla
draw_sprite(0, 0) # primer sprite


# Ejecutar el ciclo del juego
while True:
    # Manejar eventos de pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizar la pantalla
    pygame.display.update()