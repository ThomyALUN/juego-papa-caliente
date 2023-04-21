import pygame
import sys
class Sprite:
    def __init__(self, rutaImagen, x,y):
        self.rutaImagen = rutaImagen
        self.x = x
        self.y = y
    
    def set_x_y(self,x,y):
        self.x = x
        self.y = y   
    
    def draw_sprite(self, row, column):
        # Cargar la imagen de sprites
        sprite_sheet = pygame.image.load(self.rutaImagen).convert_alpha()
        # Definir las dimensiones de cada sprite    
        sprite_width = 64
        sprite_height = 68
        sprite_rect = pygame.Rect(column * sprite_width, row * sprite_height, sprite_width, sprite_height)
        sprite_image = sprite_sheet.subsurface(sprite_rect)
        #crear objeto de sprite
        sprite = pygame.sprite.Sprite()
        sprite.image = sprite_image
        sprite.rect = sprite_image.get_rect()
        sprite.rect.x = self.x
        sprite.rect.y = self.y
        
        #Mete el sprite al grupo de sprites
        all_sprites = pygame.sprite.Group()
        all_sprites.add(sprite)
        all_sprites.draw(screen)
        # Retorna el sprite creado
        return sprite
    
    def posInicial(self):      #Dibuja el sprite en la posicion inicial
        # Incrementa la columna del sprite actual
        fila = 0
        columna = 0
        
        # Muestra el nuevo sprite en la misma posición que el anterior
        current_sprite = self.drawSprite(fila, columna)        
    
    
    def girarDerecha(self):
        # Incrementa la columna del sprite actual
        fila = 1
        columna = 1
        
        # Muestra el nuevo sprite en la misma posición que el anterior
        current_sprite = self.drawSprite(fila, columna)
        
    def girarIzquierda(self):
        # Incrementa la columna del sprite actual
        fila = 1
        columna = 3
        # Muestra el nuevo sprite en la misma posición que el anterior
        current_sprite = self.drawSprite(fila, columna)
    
if __name__ == '__main__':
    pygame.init()
    
    # Definir el tamaño de la pantalla
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    x = 100
    y = 100
    sprite = Sprite("32_Characters/Males/M_02.png",x,y)
    sprite.posInicial()

    x_2 = 300
    y_2 = 100
    sprite_2 = Sprite("32_Characters/Males/M_01.png",x_2,y_2)
    sprite_2.posInicial()
    
    # Ejecutar el ciclo del juego
    while True:
        # Manejar eventos de pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
                 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Cambia el sprite mostrado al presionar la tecla espacio
                    
                    sprite.girarIzquierda()
                    sprite_2.girarDerecha()

        # Actualizar la pantalla
        pygame.display.update()
    