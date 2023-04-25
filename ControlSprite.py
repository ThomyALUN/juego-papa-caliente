import pygame

class ControlSprite:
    def __init__(self, rutaImagen:str, pantalla:pygame.surface.Surface, x:int, y:int, escalaX:int=64, escalaY:int=68):
        self.rutaImagen = rutaImagen
        self.pantalla=pantalla
        self.x = x
        self.y = y
        self.escalaX=escalaX
        self.escalaY=escalaY
    
    def setEscala(self, escalaX, escalaY):
        self.escalaX=escalaX
        self.escalaY=escalaY

    def setXY(self, x, y):
        self.x = x
        self.y = y   
    
    def drawSprite(self, row, column):
        # Cargar la imagen de sprites
        sprite_sheet = pygame.image.load(self.rutaImagen).convert_alpha()
        # Definir las dimensiones de cada sprite
        rutaSinFmt=self.rutaImagen.split(".")[0]
        if row==column==0 and rutaSinFmt[-1].lower()=="c":
            sprite_width = 60
        else:
            sprite_width = 64
        sprite_height = 68
        sprite_rect = pygame.Rect(column * sprite_width, row * sprite_height, sprite_width, sprite_height)
        sprite_image = sprite_sheet.subsurface(sprite_rect)
        sprite_image = pygame.transform.scale(sprite_image, (self.escalaX, self.escalaY))
        #crear objeto de sprite
        sprite = pygame.sprite.Sprite()
        sprite.image = sprite_image
        sprite.rect = sprite_image.get_rect()

        sprite.rect.centerx = self.x
        sprite.rect.centery = self.y
        
        #Mete el sprite al grupo de sprites   
        self.grupoSprite = pygame.sprite.Group()
        self.grupoSprite.add(sprite)
        self.grupoSprite.draw(self.pantalla)
    
    def posInicial(self):      #Dibuja el sprite en la posicion inicial
        # Incrementa la columna del sprite actual
        fila = 0
        columna = 0
        
        # Muestra el nuevo sprite en la misma posición que el anterior
        self.drawSprite(fila, columna)        
    
    
    def girarDerecha(self):
        # Incrementa la columna del sprite actual
        fila = 1
        columna = 1
        
        # Muestra el nuevo sprite en la misma posición que el anterior
        self.drawSprite(fila, columna)  
        
    def girarIzquierda(self):
        # Incrementa la columna del sprite actual
        fila = 1
        columna = 3
        # Muestra el nuevo sprite en la misma posición que el anterior
        self.drawSprite(fila, columna)  
    
if __name__ == '__main__':
    pygame.init()
    
    # Definir el tamaño de la pantalla
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    x = 100
    y = 100
    sprite = ControlSprite("sprites/Males/M_02.png", screen, x,y)
    sprite.posInicial()

    x_2 = 300
    y_2 = 100
    sprite_2 = ControlSprite("sprites/Males/M_01.png",screen,x_2,y_2)
    sprite_2.posInicial()
    
    # Ejecutar el ciclo del juego
    while True:
        # Manejar eventos de pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Cambia el sprite mostrado al presionar la tecla espacio
                    
                    sprite.girarIzquierda()
                    sprite_2.girarDerecha()
                elif event.key == pygame.K_1:
                    sprite.posInicial()
                    sprite_2.posInicial()

        # Actualizar la pantalla
        pygame.display.update()
    