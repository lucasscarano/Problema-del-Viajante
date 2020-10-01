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
lista_coordenadas = df_tabla_coordenadas.values.tolist()


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
    recorrido_mvp[0] = int(input("Ingrese la ciudad desde la que quiere empezar: "))

    for i in range(1, 24):
        aux = recorrido_mvp[i - 1]
        recorrido_mvp.append(calc_ciudad_mas_cercana(aux))


def valida_repeticion(ciudad):
    flag = False
    if ciudad in recorrido_mvp:
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
    coordenadas_mvp = [0] * 24

    # Guarda las coordenadas del mejor recorrido en orden para mostrar en el mapa
    for i in range(0, cant_ciudades):
        coordenadas_mvp[i] = lista_coordenadas[recorrido_mvp[i]]

    coordenadas_mvp.append(coordenadas_mvp[0])  # Agrega el primer punto al final para cerrar la ruta
    xs, ys = zip(*coordenadas_mvp)  # Crea una lista de los valores mapa,y
    mapa = "mapa_arg.png"
    img = mpimg.imread(mapa)
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    plt.axis('off')
    plt.plot(xs, ys, color="black")
    plt.suptitle("Gráfica del mejor recorrido partiendo de " + nombres_ciudades[recorrido_mvp[0]])
    distancia = calcula_distancia_recorrido(recorrido_mvp)
    plt.title("Se recorrieron " + str(distancia) + " kilómetros", fontsize=10)
    plt.show()


recorrido_mvp = [0]
menu()
print(recorrido_mvp)
mostrar_mapa()
