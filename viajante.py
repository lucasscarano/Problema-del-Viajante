import random
import pandas as pd

tam_poblacion = 50
cant_provincias = 23
chances_crossover = 0.75
array_poblacion = [0] * tam_poblacion
nombre_capitales = [0] * cant_provincias
array_fitness = [0] * tam_poblacion

distancias = pd.read_excel('TablaCapitales.xlsx')
distancias = distancias.to_numpy()

for k in range(0, cant_provincias):
    nombre_capitales[k] = distancias[k][0]

distancias = pd.read_excel('TablaCapitales.xlsx', index_col=0)
distancias = distancias.to_numpy()


def poblacion_inicial():
    for i in range(0, tam_poblacion):
        cromosoma = random.sample(range(cant_provincias), cant_provincias)
        array_poblacion[i] = cromosoma


def ciclico(padre1, padre2):
    hijo = [None] * cant_provincias
    j = 0
    hijo[j] = padre1[j]
    flag = True
    while flag:
        aux_j = padre2[j]
        j = padre1.index(aux_j)
        if hijo[j] is None:
            hijo[j] = padre1[j]
        else:
            flag = False
    for j in range(1, cant_provincias):
        if hijo[j] is None:
            hijo[j] = padre2[j]

    return hijo


def crossover():
    for i in range(0, tam_poblacion, 2):
        cros = random.random()
        if cros < chances_crossover:
            padre1 = array_poblacion[i]
            padre2 = array_poblacion[i + 1]
            array_poblacion[i] = ciclico(padre1, padre2)
            array_poblacion[i + 1] = ciclico(padre2, padre1)


def fitness(cromosoma):  # Devuelve el fitness de un solo cromosoma (La distancia total del recorrido en km)
    acum_fitness = 0
    for i in range(0, cant_provincias-1):
        acum_fitness += distancias[cromosoma[i], cromosoma[i + 1]]

    # Suma tambien la distancia de la ultima ciudad hasta la ciudad de partida
    acum_fitness += distancias[cromosoma[cant_provincias - 1], cromosoma[0]]

    return acum_fitness


poblacion_inicial()
crossover()
