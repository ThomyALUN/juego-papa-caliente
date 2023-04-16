import random
def listaAleatoria(cantidadP):
    nombres = ["Thomas", "María", "Alejandra", "Ana", "Jeronimo", "Juan", "Brahian", "Pedro", "Gabriela", "Camilo", "Sofia", "Andres", "Valery"]
    lista=[]
    for i in range(cantidadP):
        aleatorio = random.choice(nombres)
        lista.append(aleatorio)
    return lista
cantidadP = int(input("Ingrese la cantidad de personas jugarán: "))
print("Las personas son: ", listaAleatoria(cantidadP))