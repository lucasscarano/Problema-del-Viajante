import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

corridas = 300
tam_poblacion = 50
cant_ciudades = 24
chances_crossover = 0.90
chances_mutacion = 0.90
mvp = [0] * cant_ciudades
array_poblacion = [0] * tam_poblacion
nombres_ciudades = [0] * cant_ciudades
array_fitness = [0] * tam_poblacion
porc_elitismo = 0.1
tam_elitismo = int(tam_poblacion * porc_elitismo)
tam_elitismo = tam_elitismo if tam_elitismo % 2 == 0 else tam_elitismo + 1

# Se guarda el Excel de las distancias en un DataFrame de Pandas
df_ciudades_distancias = pd.read_excel('TablaCiudades.xlsx')

# Extrae la cabecera de la tabla con los nombres de las ciudades en una lista
nombres_ciudades = list(df_ciudades_distancias)

# Extrae solo las distancias entre las ciudades en un arreglo Numpy 2D
distancias = df_ciudades_distancias.tail(cant_ciudades).to_numpy()

# Se guardan las coordenadas de cada ciudad en el mapa en una lista 2D
df_tabla_coordenadas = pd.read_excel('TablaCoordenadas.xlsx', header=None)
lista_coordenadas = df_tabla_coordenadas.values.tolist()


def poblacion_inicial():
    for i in range(tam_poblacion):
        cromosoma = random.sample(range(cant_ciudades), cant_ciudades)
        array_poblacion[i] = cromosoma


def ruleta():
    nueva_poblacion = [0] * tam_poblacion
    for j in range(tam_poblacion):
        suma = 0
        cont_stop = random.random()
        for i in range(tam_poblacion):
            suma += array_fitness[i]
            if suma >= cont_stop:
                indice_stop = i
                break
        nueva_poblacion[j] = array_poblacion[indice_stop]
    return nueva_poblacion


def ciclico(padre1, padre2):
    hijo = [None] * cant_ciudades
    j = random.randint(0, cant_ciudades - 1)
    hijo[j] = padre1[j]
    flag = True
    while flag:
        aux_j = padre2[j]
        j = padre1.index(aux_j)
        if hijo[j] is None:
            hijo[j] = padre1[j]
        else:
            flag = False
            for j in range(cant_ciudades):
                if hijo[j] is None:
                    hijo[j] = padre2[j]
    return hijo


def crossover(cros_corridas):
    for i in range(0, cros_corridas, 2):
        cros = random.random()
        if cros < chances_crossover:
            padre1 = array_poblacion[i]
            padre2 = array_poblacion[i + 1]
            array_poblacion[i] = ciclico(padre1, padre2)
            array_poblacion[i + 1] = ciclico(padre2, padre1)


def calcula_distancia_recorrido(cromosoma):  # Devuelve el fitness de un solo cromosoma
    dist_recorrido = 0
    for i in range(cant_ciudades - 1):
        dist_recorrido += distancias[cromosoma[i], cromosoma[i + 1]]

    # Suma tambien la distancia de la ultima ciudad hasta la ciudad de partida
    dist_recorrido += distancias[cromosoma[cant_ciudades - 1], cromosoma[0]]
    return dist_recorrido


def calcula_fitness_poblacion():
    array_distancias = [0] * tam_poblacion
    for i in range(tam_poblacion):
        array_distancias[i] = calcula_distancia_recorrido(array_poblacion[i])
    distancia_total = np.sum(array_distancias)
    for i in range(tam_poblacion):
        array_fitness[i] = distancia_total - array_distancias[i]
    sumatoria_complementos = np.sum(array_fitness)
    for i in range(tam_poblacion):
        array_fitness[i] = (array_fitness[i] / sumatoria_complementos)


# Devuelve los mejores cromosomas (la cantidad igual al 10% del tam_poblacion)
def elite(cont):
    global array_poblacion
    indices_elitismo = np.argsort(array_fitness)[::-1][:tam_elitismo]
    # Devuelve los indices de los mejores cromosomas, considerando el fitness, de mayor a menor
    for i in range(0, tam_elitismo):
        array_poblacion[indices_elitismo[i]], array_poblacion[cont] = array_poblacion[cont], array_poblacion[indices_elitismo[i]]
        cont += 1


def mutacion(muta_corridas):
    for i in range(muta_corridas):
        muta = random.random()
        if muta < chances_mutacion:
            pos1 = random.randint(0, cant_ciudades - 1)
            pos2 = random.randint(0, cant_ciudades - 1)
            while pos2 == pos1:
                pos2 = random.randint(0, cant_ciudades - 1)
            array_poblacion[i][pos1], array_poblacion[i][pos2] = array_poblacion[i][pos2], array_poblacion[i][pos1]


def asigna_mvp():
    global mvp
    for i in range(tam_poblacion):
        if calcula_distancia_recorrido(mvp) > calcula_distancia_recorrido(array_poblacion[i]):
            mvp = array_poblacion[i]


# Main
#resp = input('Quiere hacer elitismo (s/n): ')
resp = 'n'
poblacion_inicial()
calcula_fitness_poblacion()
mvp = array_poblacion[0]
for cor in range(corridas):
    array_poblacion = ruleta()
    calcula_fitness_poblacion()
    if resp == 's' or resp == 'S':
        n = tam_poblacion - tam_elitismo
        elite(n)
    else:
        n = tam_poblacion
    crossover(n)
    mutacion(n)
    asigna_mvp()

coordenadas_mvp = [0] * cant_ciudades
distancia_mvp = calcula_distancia_recorrido(mvp)
recorrido_viajante = [0] * cant_ciudades
for k in range(cant_ciudades):
    recorrido_viajante[k] = nombres_ciudades[mvp[k]]

print(distancia_mvp)
print(recorrido_viajante)
print(mvp)

for ciudades in range(cant_ciudades):
    coordenadas = [0] * 2
    coordenadas[0] = lista_coordenadas[mvp[ciudades]][0]
    coordenadas[1] = lista_coordenadas[mvp[ciudades]][1]
    coordenadas_mvp[ciudades] = coordenadas

coordenadas_mvp.append(coordenadas_mvp[0])  # Agrega el primer punto al final para cerrar la ruta
xs, ys = zip(*coordenadas_mvp)  # Crea una lista de los valores mapa,y
mapa = "mapa_arg.png"
img = mpimg.imread(mapa)
imgplot = plt.imshow(img)
imgplot.axes.get_xaxis().set_visible(False)
plt.axis('off')
plt.plot(xs, ys, color="black")
plt.suptitle("Gráfica del mejor recorrido")
distancia = calcula_distancia_recorrido(mvp)
plt.title("se recorrieron " + str(distancia) + " kilometros", fontsize=10)
plt.show()
