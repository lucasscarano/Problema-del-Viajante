import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

cant_ciudades = 24

df_ciudades_distancias = pd.read_excel('TablaCiudades.xlsx')
nombres_ciudades = list(df_ciudades_distancias)
distancias = df_ciudades_distancias.tail(cant_ciudades).to_numpy()
ciudades_posibles = list(range(cant_ciudades))

df_tabla_coordenadas = pd.read_excel('TablaCoordenadas.xlsx', header=None)
coordenadas1 = df_tabla_coordenadas.to_numpy()


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
    mejor_recorrido[0] = int(input("Ingrese la ciudad desde la que quiere empezar: "))

    for i in range(1, 24):
        aux = mejor_recorrido[i-1]
        mejor_recorrido.append(calc_ciudad_mas_cercana(aux))


def valida_repeticion(ciudad):
    flag = False
    if ciudad in mejor_recorrido:
        flag = True
    return flag


def calc_ciudad_mas_cercana(ciudad):
    distancias_ciudad = distancias[ciudad]
    cont = 1
    flag = True
    distancia_minima = np.argsort(distancias_ciudad)
    while flag:
        ciudad_mas_cercana = distancia_minima[cont]
        valida = valida_repeticion(ciudad_mas_cercana)
        if valida:
            cont += 1
        else:
            flag = False
    return ciudad_mas_cercana


def mostrar_mapa():
    coord = [0] * 24
    skere = mejor_recorrido
    for i in range(0, 24):
        coordenadas = [0] * 2
        coordenadas[0] = coordenadas1[skere[i]][0]
        coordenadas[1] = coordenadas1[skere[i]][1]
        coord[i] = coordenadas

    coord.append(coord[0])  # repeat the first point to create a 'closed loop'
    xs, ys = zip(*coord)  # create lists of x and y values
    x = "mapa_arg.png"
    img = mpimg.imread(x)
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    plt.axis('off')
    plt.plot(xs, ys, color="black")
    plt.suptitle("Gráfica del mejor recorrido partiendo de " + nombres_ciudades[mejor_recorrido[0]])
    distancia = calcula_distancia_recorrido(skere)
    plt.title("Se recorrieron " + str(distancia) + " kilómetros", fontsize=10)
    plt.show()


mejor_recorrido = [0]
menu()
print(mejor_recorrido)
mostrar_mapa()
