import random
import pandas as pd

tam_poblacion = 50
cant_ciudades = 24
chances_crossover = 0.75
array_poblacion = [0] * tam_poblacion
nombres_ciudades = [0] * cant_ciudades
array_fitness = [0] * tam_poblacion

# Se guarda el Excel en un DataFrame de Pandas
df_ciudades_distancias = pd.read_excel('TablaCiudades.xlsx')

# Extrae la cabecera de la tabla con los nombres de las ciudades en una lista
nombres_ciudades = list(df_ciudades_distancias)

# Extrae solo las distancias entre las ciudades en un arreglo Numpy 2D
distancias = df_ciudades_distancias.tail(cant_ciudades).to_numpy()


def poblacion_inicial():
    for i in range(0, tam_poblacion):
        cromosoma = random.sample(range(cant_ciudades), cant_ciudades)
        array_poblacion[i] = cromosoma


def ciclico(padre1, padre2):
    hijo = [None] * cant_ciudades
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
    for j in range(1, cant_ciudades):
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
    for i in range(0, cant_ciudades-1):
        acum_fitness += distancias[cromosoma[i], cromosoma[i + 1]]

    # Suma tambien la distancia de la ultima ciudad hasta la ciudad de partida
    acum_fitness += distancias[cromosoma[cant_ciudades - 1], cromosoma[0]]

    return acum_fitness


poblacion_inicial()
crossover()
