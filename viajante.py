import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

corridas = 500
tam_poblacion = 50
cant_ciudades = 24
chances_crossover = 0.75
chances_mutacion = 0.05
nombres_ciudades = [0] * cant_ciudades
array_fitness = [0] * tam_poblacion
array_poblacion = [0] * tam_poblacion
aux_poblacion = [0] * tam_poblacion
porc_elitismo = 0.1
tam_elitismo = int(tam_poblacion * porc_elitismo)
tam_elitismo = tam_elitismo if tam_elitismo % 2 == 0 else tam_elitismo + 1

df_tabla_coordenadas = pd.read_excel('TablaCoordenadas.xlsx',header=None)
coordenadas1 = df_tabla_coordenadas.to_numpy()

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


def ruleta():
    base = 0
    cant_casilleros = 0

    for i in range(0, tam_poblacion):
        casilleros = round(array_fitness[i] * 1000)
        cant_casilleros = cant_casilleros + casilleros
    roulette = [0] * cant_casilleros

    for i in range(0, tam_poblacion):
        casilleros = round(array_fitness[i] * 1000)

        for j in range(base, base + casilleros):
            roulette[j] = i
        base = base + casilleros

    nueva_poblacion = [0] * tam_poblacion
    for i in range(0, tam_poblacion):
        bolilla = random.randint(0, cant_casilleros - 1)
        nueva_poblacion[i] = array_poblacion[roulette[bolilla]]

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
    cros_corridas = len(aux_poblacion)
    for i in range(0, cros_corridas, 2):
        cros = random.random()
        if cros < chances_crossover:
            padre1 = aux_poblacion[i]
            padre2 = aux_poblacion[i + 1]
            aux_poblacion[i] = ciclico(padre1, padre2)
            aux_poblacion[i + 1] = ciclico(padre2, padre1)


def calcula_distancia_recorrido(cromosoma):  # Devuelve el fitness de un solo cromosoma
    dist_recorrido = 0
    for i in range(0, cant_ciudades - 1):
        dist_recorrido += distancias[cromosoma[i], cromosoma[i + 1]]

    # Suma tambien la distancia de la ultima ciudad hasta la ciudad de partida
    dist_recorrido += distancias[cromosoma[cant_ciudades - 1], cromosoma[0]]

    return dist_recorrido


def calcula_fitness_poblacion():
    array_distancias = [0] * tam_poblacion
    for i in range(0, tam_poblacion):
        array_distancias[i] = calcula_distancia_recorrido(array_poblacion[i])
    distancia_total= np.sum(array_distancias)
    for i in range(0, tam_poblacion):
        array_fitness[i] = distancia_total - array_distancias[i]
    sumatoria_complementos = np.sum(array_fitness)
    for i in range(0, tam_poblacion):
        array_fitness[i] = (array_fitness[i] / sumatoria_complementos)


#Devuelve los mejores cromosomas (la cantidad igual al 10% del tam_poblacion)
def elite():
    global aux_poblacion
    array_elitismo = [0] * tam_elitismo
    indices_elitismo = np.argsort(array_fitness)[::-1][:tam_elitismo]
    #Devuelve los indices de los mejores cromosomas, considerando el fitness, de mayor a menor
    for i in range(0, tam_elitismo):
        array_elitismo[i] = array_poblacion[indices_elitismo[i]]

    aux_poblacion = np.delete(array_poblacion, indices_elitismo, 0).tolist()
    return array_elitismo

def mutacion():
    muta_corridas = len(array_poblacion)
    for i in range(0, muta_corridas):
        muta = random.random()
        if muta < chances_mutacion:
            pos1 = random.randint(0,cant_ciudades-1)
            pos2 = random.randint(0,cant_ciudades-1)
            while pos2 == pos1:
                pos2 = random.randint(0,cant_ciudades-1)
            cromosoma = array_poblacion[i]
            array_poblacion[pos1], array_poblacion[pos2] = array_poblacion[pos2], array_poblacion[pos1]


#main
resp = input('Quiere hacer elitismo (s/n): ')
if resp == 's' or resp == 'S':
    array_elite = elite()

poblacion_inicial()
for i in range(0, corridas):
    calcula_fitness_poblacion()
    array_poblacion = ruleta()
    aux_poblacion = array_poblacion
    crossover()
    mutacion()
    #Ingresa los cromosomas elitistas a la poblacion resultante del crossover
    if resp == 'S' or resp == 's':
        for l in range(0, len(array_elite)):
            aux_poblacion.append(array_elite[l])
        array_poblacion = aux_poblacion






coord = [0]*24
indice_mvp = np.argmax(array_fitness)
skere = array_poblacion[indice_mvp]
for i in range(0, 24):
    coordenadas = [0]*2
    coordenadas[0] = coordenadas1[skere[i]][0]
    coordenadas[1] = coordenadas1[skere[i]][1]
    coord[i] = coordenadas


coord.append(coord[0]) #repeat the first point to create a 'closed loop'
xs, ys = zip(*coord) #create lists of x and y values
x = "C:/Users/malga/OneDrive/Documentos/GitHub/Problema-del-Viajante/z1.png"
img = mpimg.imread(x)
imgplot = plt.imshow(img)
imgplot.axes.get_xaxis().set_visible(False)
plt.axis('off')
plt.plot(xs,ys, color="black")
plt.suptitle("Gráfica de el mejor recorrido")
distancia = calcula_distancia_recorrido(skere)
plt.title("se recorrieron "+ str(distancia)+" kilometros", fontsize=10)
plt.show()
