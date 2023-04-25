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
    
    def dibujarSprite(self, row, column):
        # Cargar la imagen de sprites
        hojaSprite = pygame.image.load(self.rutaImagen).convert_alpha()
        # Definir las dimensiones de cada sprite
        rutaSinFmt=self.rutaImagen.split(".")[0]
        if row==column==0 and rutaSinFmt[-1].lower()=="c":
            anchoSprite = 60
        else:
            anchoSprite = 64
        alturaSprite = 68
        rectSprite = pygame.Rect(column * anchoSprite, row * alturaSprite, anchoSprite, alturaSprite)
        imagenSprite = hojaSprite.subsurface(rectSprite)
        imagenSprite = pygame.transform.scale(imagenSprite, (self.escalaX, self.escalaY))
        # Crear objeto de sprite
        sprite = pygame.sprite.Sprite()
        sprite.image = imagenSprite
        sprite.rect = imagenSprite.get_rect()

        sprite.rect.centerx = self.x
        sprite.rect.centery = self.y
        
        #Mete el sprite al grupo de sprites   
        self.grupoSprite = pygame.sprite.Group()
        self.grupoSprite.add(sprite)
        self.grupoSprite.draw(self.pantalla)
    
    def posInicial(self):      #Dibuja el sprite en la posicion inicial
        fila = 0
        columna = 0
        self.dibujarSprite(fila, columna)        
    
    def girarDerecha(self):
        fila = 1
        columna = 1
        self.dibujarSprite(fila, columna)  
        
    def girarIzquierda(self):
        fila = 1
        columna = 3
        self.dibujarSprite(fila, columna)  
    
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