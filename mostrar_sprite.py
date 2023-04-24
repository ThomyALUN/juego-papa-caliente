import pygame
import sys

# Inicializar pygame
pygame.init()

# Definir el tamaño de la pantalla
screen_width = 150
screen_height = 150
screen = pygame.display.set_mode((screen_width, screen_height))

# Cargar la imagen de sprites
sprite_sheet = pygame.image.load("32_Characters/Males/M_02.png").convert_alpha()

# Definir las dimensiones de cada sprite    
sprite_width = 64
sprite_height = 68

# Función para mostrar un sprite en la pantalla
def draw_sprite(row, column):
    sprite_rect = pygame.Rect(column * sprite_width, row * sprite_height, sprite_width, sprite_height)
    sprite_image = sprite_sheet.subsurface(sprite_rect)
    #crear objeto de sprite
    sprite = pygame.sprite.Sprite()
    sprite.image = sprite_image
    sprite.rect = sprite_image.get_rect()
    sprite.rect.center = (screen_width // 2, screen_height // 2)
    #Mete el sprite al grupo de sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(sprite)
    all_sprites.draw(screen)
    # Retorna el sprite creado
    return sprite

def girar_derecha():
    global current_row, current_column, current_sprite
    # Incrementa la columna del sprite actual
    current_row = 1
    current_column = 1
    current_sprite.kill()
    # Muestra el nuevo sprite en la misma posición que el anterior
    current_sprite = draw_sprite(current_row, current_column)

def girar_izquierda():
    global current_row, current_column, current_sprite
    # Incrementa la columna del sprite actual
    current_row = 1
    current_column = 3
    current_sprite.kill()
    # Muestra el nuevo sprite en la misma posición que el anterior
    current_sprite = draw_sprite(current_row, current_column)

    
# Variables para llevar el seguimiento del sprite actual
current_row = 0
current_column = 0
current_sprite = draw_sprite(current_row, current_column)

# Configurar temporizador para volver al sprite inicial
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 2000) # 2000 milisegundos = 2 segundos



# Ejecutar el ciclo del juego
while True:
    # Manejar eventos de pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == TIMER_EVENT:
            # Volver al sprite inicial después del temporizador
            current_row = 0
            current_column = 0
            current_sprite = draw_sprite(current_row, current_column)
            # Mostrar el sprite inicial en la pantalla    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Cambia el sprite mostrado al presionar la tecla espacio
                girar_izquierda()

    # Actualizar la pantalla
    pygame.display.update()