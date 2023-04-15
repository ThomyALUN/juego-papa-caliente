from random import randint
import time 

class Queue:
    '''Cola implementada utilizando una lista nativa de Python'''
    def __init__(self):
        '''Construye una instancia de la clase Cola'''
        self._items = []
    def enqueue(self, item):
        '''Agrega un elemento recibido como pámetro al final de la Cola'''
        self._items.insert(0, item)
    def dequeue(self):
        '''Elimina un elemento al frente de la Cola y lo retorna'''
        return self._items.pop()
    def peek(self):
        '''Método propio: Retorna el elemento al frente de la Cola sin eliminarlo'''
        return self._items[-1]
    def size(self):
        '''Retorna la cantidad de elementos presentes en la Cola'''
        return len(self._items)
    def isEmpty(self):
        '''Retorna un booleano que indica si la Cola esta vacía o no'''
        return not bool(self._items)
    def search(self,item):
        '''Método propio: Determina si un elemento esta en la cola'''
        return item in self._items

class CtrldrPapaCaliente(Queue):
    '''Controlador del juego de la papa caliente'''
    def __init__(self, nombre:str):
        '''Construye el controlador del juego papa caliente'''
        super().__init__()
        self._inicio=False
        self.agregarPersonaje(nombre)
        self._nombreJugador=nombre

    def iniciarJuego(self):
        self._inicio=True

    def pausarJuego(self):
        self._inicio=False

    def moverPapa(self):
        if self._inicio and self.size()>1:
            self.enqueue(self.dequeue())

    def agregarPersonaje(self, nombre:str):
        '''Agrega un personaje(nombre) a la cola si no esta repetido'''
        if not self._inicio and not self.search(nombre):
            self.enqueue(nombre)

    def agregarListaPjs(self, listaNombres:list):
        '''Agrega una lista de personajes(nombres a la cola), 
        teniendo en cuenta que cada nombre no este repetido'''
        if not self._inicio:
            for nombre in listaNombres:
                self.agregarPersonaje(nombre)

    def jugarRonda(self):
        numJugadores=self.size()
        tiempoExtra=randint(numJugadores*2, numJugadores*3)
        print(tiempoExtra)
        tiempoActual=time.time()
        tiempoFinal=tiempoActual+tiempoExtra
        while time.time()<tiempoFinal:
            if self.peek()==self._nombreJugador:
                input(f"Turno de {self._nombreJugador}")
            else:
                time.sleep(0.7)
            self.moverPapa()
            self.mostrarJugadores()
        print("Sale: ",self.dequeue())

    def mostrarJugadores(self):
        print(f"La cola tiene los siguientes elementos {self._items}")
        print(f"La persona que tiene la papa caliente es: {self.peek()}")

if __name__=="__main__":
    controlador=CtrldrPapaCaliente("Thomas")
    controlador.agregarListaPjs(["Carlos","Yolanda","Thomas","Luke"])
    controlador.mostrarJugadores()

    controlador.iniciarJuego()
    controlador.moverPapa()
    controlador.mostrarJugadores()

    while controlador.size()>1:
        controlador.jugarRonda()
        controlador.mostrarJugadores()

