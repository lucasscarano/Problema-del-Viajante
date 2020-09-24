import pandas as pd
import numpy as np

cant_ciudades = 24
nombres_ciudades = [0] * cant_ciudades

df_ciudades_distancias = pd.read_excel('TablaCiudades.xlsx')
nombres_ciudades = list(df_ciudades_distancias)
distancias = df_ciudades_distancias.tail(cant_ciudades).to_numpy()
ciudades_posibles = list(range(cant_ciudades))


def calcula_distancia_recorrido(cromosoma):  # Devuelve el fitness de un solo cromosoma
    dist_recorrido = 0
    for i in range(cant_ciudades - 1):
        dist_recorrido += distancias[cromosoma[i], cromosoma[i + 1]]

    # Suma tambien la distancia de la ultima ciudad hasta la ciudad de partida
    dist_recorrido += distancias[cromosoma[cant_ciudades - 1], cromosoma[0]]
    return dist_recorrido


def menu():
    for i in range(cant_ciudades):
        print(i, '. ', nombres_ciudades[i])
    ciudad_cercana = int(input("Ingrese la ciudad desde la que quiere empezar: "))

    # while ciudades_posibles is not None:
    ciudad_cercana = calc_ciudad_cercana(ciudad_cercana)
    print(ciudad_cercana)


def calc_ciudad_cercana(ciudad):
    global ciudades_posibles
    distancias_ciudad = distancias[ciudad]
    dist_sin_cero = distancias_ciudad[distancias_ciudad != 0]
    distancia_minima = np.argsort(distancias_ciudad)
    ciudad_cercana = distancia_minima[1]
    # ciudades_posibles = np.delete(ciudades_posibles, ciudad, 0)
    return ciudad_cercana


menu()
