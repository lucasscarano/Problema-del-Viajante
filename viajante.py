import random
import pandas as pd
import numpy as np

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


def rank():
    aux_fitness_indices = np.argsort(array_fitness)[::-1]
    aux_poblacion = [0] * tam_poblacion
    total_fitness = int((tam_poblacion * (tam_poblacion + 1)) / 2)
    for i in range(0, tam_poblacion):
        aux_poblacion[i] = array_poblacion[aux_fitness_indices[i]]
    valor_ruleta = [0] * total_fitness
    cont = 0
    for i in range(0, tam_poblacion):
        for j in range(0, i+1):
            valor_ruleta[cont] = i
            cont += 1
    nueva_poblacion = [0] * tam_poblacion
    for i in range(0, tam_poblacion):
        nueva_poblacion[i] = aux_poblacion[valor_ruleta[random.randint(0, total_fitness-1)]]
    print()
    return nueva_poblacion


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


def calcula_distancia_recorrido(cromosoma):  # Devuelve el fitness de un solo cromosoma
    acum_fitness = 0
    for i in range(0, cant_ciudades - 1):
        acum_fitness += distancias[cromosoma[i], cromosoma[i + 1]]

    # Suma tambien la distancia de la ultima ciudad hasta la ciudad de partida
    acum_fitness += distancias[cromosoma[cant_ciudades - 1], cromosoma[0]]

    return acum_fitness


def calcula_fitness_poblacion():
    for i in range(0, tam_poblacion):
        array_fitness[i] = calcula_distancia_recorrido(array_poblacion[i])


poblacion_inicial()
crossover()
calcula_fitness_poblacion()
array_poblacion = rank()
