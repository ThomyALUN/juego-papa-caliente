import random
def listaAleatoria(cantidadP):
    """
    Crea una lista de nombres aleatorios sin repetición.

    Parámetros:
    cantidadP (int): la cantidad de personas que van a jugar.

    Retorna:
    Una lista con `cantidadP` de nombres aleatorios seleccionados al azar de la lista `nombres`.
    """
    nombres = ["Thomas", "María", "Alejandra", "Ana", "Jeronimo", "Juan", "Brahian", "Pedro", 
               "Gabriela", "Camilo", "Sofia", "Andres", "Valery", "Pepe", "Juanita", "Luis",
               "Clara", "Adrian", "Veronica", "Santiago", "Valentina", "Miguel", "Manuela",
               "Manuel", "Gina", "Stiven", "Dana", "Sara", "Jessica", "Jhon", "Esteban", "David"]
    lista=[]
    i=cantidadP
    while i != 0:
        aleatorio = random.choice(nombres)
        if aleatorio not in lista: 
            lista.append(aleatorio)
            i-=1
    return lista

cantidadP = int(input("Ingrese la cantidad de personas jugarán: "))

print("Las personas son: ", listaAleatoria(cantidadP)) 
