import pygame
import sys

def pintar_boton(screen, boton, mensaje):
    """
    Esta funcion sirve para pintar los botones de la dificultad.
    Tiene como parametros:
    La pantalla, el boton y el mensaje que tendrá en el botón
    
    No retorna nada, ya que solo pintará el boton
    """
    if boton.collidepoint(pygame.mouse.get_pos()): #Detecta el movimiento del mouse para cambiar de color cada vez que pase por encima del boton
        pygame.draw.rect(screen, (237,128,19), boton, 0)
    else:
        pygame.draw.rect(screen, (70,189,34), boton, 0)
    myFont = pygame.font.SysFont("Calibri",30) 
    texto= myFont.render(mensaje, True, (225,225,225))
    screen.blit(texto, (boton.x+(boton.width-texto.get_width())//2,
                        boton.y+(boton.height-texto.get_height())//2)) #Colocando el texto en el centro del boton

def clic_boton():
    global clic
    """Esta funcion detecta en que boton se le da click
    Y lo almacena en una variable para que despues ese valor seq utilizado"""
    if facil.collidepoint(pygame.mouse.get_pos()):
        clic = 1
    if estandar.collidepoint(pygame.mouse.get_pos()):
        clic = 2
    if dificil.collidepoint(pygame.mouse.get_pos()):
        clic = 3
    return clic

pygame.init()
screen = pygame.display.set_mode((800,600))

#Se crean los botones
facil = pygame.Rect(300,100,150,50)
estandar = pygame.Rect(300,200,150,50)
dificil = pygame.Rect(300,300,150,50)

while True: 
    screen.fill((225,225,225))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        #Detectar clic del pygame.mouse y almacenarlo en una variable con valor True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            print(clic_boton())

    pintar_boton(screen, facil, "FACIL")
    pintar_boton(screen, estandar, "ESTANDAR")
    pintar_boton(screen, dificil, "DIFICIL")

    pygame.display.flip()


