from pygame import *
import sys

def pintar_boton(screen, boton, mensaje):
    """
    Esta funcion sirve para pintar los botones de la dificultad.
    Tiene como parametros:
    La pantalla, el boton y el mensaje que tendrá en el botón
    
    No retorna nada, ya que solo pintará el boton
    """
    if boton.collidepoint(mouse.get_pos()): #Detecta el movimiento del mouse para cambiar de color cada vez que pase por encima del boton
        draw.rect(screen, (237,128,19), boton, 0)
    else:
        draw.rect(screen, (70,189,34), boton, 0)
    myFont = font.SysFont("Calibri",30) 
    texto= myFont.render(mensaje, True, (225,225,225))
    screen.blit(texto, (boton.x+(boton.width-texto.get_width())//2,
                        boton.y+(boton.height-texto.get_height())//2)) #Colocando el texto en el centro del boton

def clic_boton():
    global clic
    """Esta funcion detecta en que boton se le da click
    Y lo almacena en una variable para que despues ese valor seq utilizado"""
    if facil.collidepoint(mouse.get_pos()):
        clic = True
    if estandar.collidepoint(mouse.get_pos()):
        clic = True
    if dificil.collidepoint(mouse.get_pos()):
        clic = True
    return clic

init()
screen = display.set_mode((800,600))

#Se crean los botones
facil = Rect(300,100,150,50)
estandar = Rect(300,200,150,50)
dificil = Rect(300,300,150,50)

while True: 
    screen.fill((225,225,225))
    for e in event.get():
        if e.type == QUIT: sys.exit()
        #Detectar clic del mouse y almacenarlo en una variable con valor True
        if e.type == MOUSEBUTTONDOWN and e.button==1:
            clic_boton()

    pintar_boton(screen, facil, "FACIL")
    pintar_boton(screen, estandar, "ESTANDAR")
    pintar_boton(screen, dificil, "DIFICIL")

    display.flip()


