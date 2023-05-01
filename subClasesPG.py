import pygame

class ControlSprite:
    '''Clase creada para facilitar el control de los sprites y su dibujado en pantalla'''
    def __init__(self, rutaImagen:str, pantalla:pygame.surface.Surface, x:int, y:int, escalaX:int=64, escalaY:int=68):
        '''Constructor de la clase ControlSprite. Recibe varios parámetros: la ruta donde esta el mapa del sprite,
        la pantalla o superficie de pygame, sus coordenadas en X y en Y, y su escala horizontal y vertical'''
        self.rutaImagen = rutaImagen
        self.pantalla=pantalla
        self.x = x
        self.y = y
        self.escalaX=escalaX
        self.escalaY=escalaY
    
    def setEscala(self, escalaX:int, escalaY:int):
        '''Permite cambiar la escala final en que se graficará el sprite. 
        Recibe como parámetros: el valor horizontal y el valor vertical de la escala'''
        self.escalaX=escalaX
        self.escalaY=escalaY

    def setXY(self, x:int, y:int):
        '''Permite cambiar la posición final donde se graficará el sprite. 
        Recibe como parámetros: la coordenada X y la coordenada Y'''
        self.x = x
        self.y = y   
    
    def dibujarSprite(self, row:int, column:int):
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
    
    def posInicial(self):
        '''Dibuja el sprite mirando hacia el frente'''
        fila = 0
        columna = 0
        self.dibujarSprite(fila, columna)        
    
    def girarDerecha(self):
        '''Dibuja el sprite girado hacia la derecha'''
        fila = 1
        columna = 1
        self.dibujarSprite(fila, columna)  
        
    def girarIzquierda(self):
        '''Dibuja el sprite girado hacia la izquierda'''
        fila = 1
        columna = 3
        self.dibujarSprite(fila, columna)  

# Clase para la entrada de texto
class CajaTexto:
    def __init__(self, x, y, w, h, pantalla, texto=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color("orange")
        self.color_active = pygame.Color("black")
        self.color = self.color_inactive
        self.texto = texto
        self.font = pygame.font.Font(None, 48)
        self.active = False
        self.pantalla=pantalla

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
                if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    if len(self.texto)<=10:
                        self.texto+= event.unicode

    def actualizar(self):
        # Crear la superficie de texto y actualizar el rectángulo de la entrada de texto
        self.textoRenderizado = self.font.render(self.texto, True, self.color)

    def dibujar(self):
        # Dibujar la entrada de texto en la superficie dada con su respectivo rectangulo
        pygame.draw.rect(self.pantalla, (20, 20, 20), self.rect, 4)
        self.pantalla.blit(
                        self.textoRenderizado, (self.rect.x+(self.rect.width - self.textoRenderizado.get_width())/2, 
                        self.rect.y+(self.rect.height-self.textoRenderizado.get_height())/2)
                        )


class Boton(pygame.rect.Rect):
    def __init__(self, x:int, y:int, width:int, height:int, mensaje:str, pantalla:pygame.surface.Surface, 
                tamanioLetra:int=80, fuente:str=None, colorActivo:tuple=(255, 195, 0), colorPasivo:tuple=(218, 247, 166)):
        self.x = x
        self.y = y
        self.xInicial = x
        self.yInicial = y
        self.width = width
        self.height = height
        self.mensaje = mensaje
        self.pantalla=pantalla
        self.tamanioLetra = tamanioLetra
        self.fuente=fuente
        self.colorActivo = colorActivo
        self.colorPasivo = colorPasivo
        self.negro = (0, 0, 0)

    def desplazar(self, movX, movY):
        self.x=self.xInicial+movX
        self.y=self.yInicial+movY

    def volverPosInicial(self):
        self.x=self.xInicial
        self.y=self.yInicial

    def mostrarBoton(self):
        # Define el estilo de la fuente
        if self.fuente==None:
            textoBoton = pygame.font.Font(self.fuente, self.tamanioLetra).render(self.mensaje, True, self.negro)
        else:
            textoBoton = pygame.font.SysFont(self.fuente, self.tamanioLetra).render(self.mensaje, True, self.negro)

        # Detecta si el mouse esta posado sobre el botón
        if self.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.pantalla, self.colorPasivo, (self.x, self.y, self.w, self.h), 0, 20)
        else:
            pygame.draw.rect(self.pantalla, self.colorActivo, (self.x, self.y, self.w, self.h), 0, 20)
        self.pantalla.blit(textoBoton, ((self.x+(self.width-textoBoton.get_width())/2),(self.y+(self.height-textoBoton.get_height())/2)))