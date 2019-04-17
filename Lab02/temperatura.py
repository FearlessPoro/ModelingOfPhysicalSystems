import time

import matplotlib.pyplot as plt
import numpy as np

# temp
from matplotlib import animation

Th = 100
T0 = 0
Tp = 20
# dimensions
h = 0.5
A = 20 + 2 * h
B = 10
C = 5
D = 3

siatka = 0.5

size = int(np.floor(A / siatka))

K_cu = 237
cw_cu = 900
ro_cu = 2700
P = 100
Cw = cw_cu
ro = ro_cu
V = 115E-6

dt = 60
const = (dt * K_cu) / (cw_cu * ro_cu)

# liczba liczb po przecinku w porownaniu
epsilon = 20

difference = np.empty((size, size))
difference.fill(1)


def set_resolution(siatka):
    A = 20 / siatka
    B = 10 / siatka
    C = 5 / siatka
    D = 3 / siatka


def plansza_kwadrat():
    size = recalculate(A)
    array = np.empty((size, size))
    array.fill(Tp)
    array = edge_case(array)
    for t in range(0, 500):
        array = przyjemne_rownanie(array)
    plot(array)
    # trace = go.Heatmap(z=array.tolist())
    # data = [trace]
    # py.plot(data, filename='heatmap-start')


def edge_case(array):
    array = static_hot(array)
    for i in range(0, size):
        for j in range(0, size):
            if not is_T_edge(i, j):
                array[i][j] = 0
    return array


def dynamic_hot(input):
   #funkcja sluzaca podgrzewaniu wybranych elementow blaszki grzalka o mocy P
    array = input.copy()
    if dt > 10:
        time = 10
    else:
        time = dt
    for i in range(calculate_index(8), calculate_index(11)):
        for j in range(calculate_index(2), calculate_index(5)):
            array[i][j] = array[i][j] + (P * time)/(Cw * (h/100) * ro * (D/100)**2)
    return array

def static_hot(array):
    for i in range(calculate_index(8), calculate_index(11)):
        for j in range(calculate_index(2), calculate_index(5)):
            array[i][j] = Th
    return array


def calculate_index(x):
    return recalculate(x) + 1


def przyjemne_rownanie(input):
    output = np.empty((size, size))
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            output[i][j] = input[i][j] + (const / siatka ** 2) * (input[i + 1][j] - 2 * input[i][j] + input[i - 1][j]) + \
                           (const / siatka ** 2) * (input[i][j + 1] - 2 * input[i][j] + input[i][j - 1])
    output = edge_case(output)
    difference.fill(0)
    for i in range(2, size - 2):
        for j in range(2, size - 2):
            difference[i][j] = input[i][j] - output[i][j]
    return output


def calculate_next_step_with_isolation(input):
    #utworz kopie danych wejsciowych
    output = input.copy()
    #wyznaczanie warunkow von Neumana
    output = calculate_edges(output)
    #wyznaczanie temperatury w kolejnym krokau czasowym
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if is_T_edge(i, j):
                output[i][j] = input[i][j] + (const / siatka ** 2) * (
                            input[i + 1][j] - 2 * input[i][j] + input[i - 1][j]) + \
                               (const / siatka ** 2) * (input[i][j + 1] - 2 * input[i][j] + input[i][j - 1])
    return output


def plot(output):
    plt.close()
    plt.imshow(output, cmap='hot', interpolation='nearest')
    heatmap = plt.pcolor(output)
    plt.colorbar(heatmap)
    plt.show()


def plansza_T():
    size = recalculate(A)
    array = np.empty((size, size))
    array.fill(Tp)
    array = static_hot(array)
    for i in range(0, size):
        for j in range(0, size):
            if not is_T_edge(i, j):
                array[i][j] = 0
    rounded = np.around(difference, epsilon)
    licznik = 0
    while True:
        rounded = np.around(difference)
        array = przyjemne_rownanie(array)
        licznik += 1
        if licznik % 100 == 0:
            plot(array)
    plot(array)


def plot_case_2():
    #inicjacja danych w tablicy dwuwymiarowej
    #metoda recalculate wyznacza rozmiar tabelii biorac pod uwage wielkosc siatki i zadane A
    size = recalculate(A)
    data = np.empty((size, size))
    data.fill(Tp)
    for i in range(0, size):
        for j in range(0, size):
            if not is_extended_T_edge(i, j):
                data[i][j] = 0
    #wyznaczanie czasu trwania algorytmu
    start = time.time()
    #deklaracja zmiennej ktora bedzie uzywana jako wyznacznik ktora chwila czasowa jest obecnie
    counter = 0
    #wyznacz przewidywana koncowa temperature ze wzoru
    DeltaT = 20 + P * 10 / (Cw * ro * V)
    print("tempend= " + str(DeltaT))
    #narysuj poczatkowy moment wykresu
    plot_and_save(data, counter="start", max=20, min=0)
    #petla ktora sluzy wyznaczeniu wartosci koncowych
    while counter < 2000000:
        #znajdz maksymalna i minimalna temperature
        max, min = find_edge_temp(data)
        #w celu wyznaczenia skali wykresu musimy obsluzyc przypadek rownych wartosci
        if np.abs(max - min) < 0.01:
            max = min + 1
        #podgrzewanie w poczatkowych 10 sekundach
        if counter < 10:
            data = dynamic_hot(data)
            max, min = find_edge_temp(data)
            plot_and_save(data, counter, max, min)
        # wykonaj jedna iteracje algorytmu
        data = calculate_next_step_with_isolation(data)
        #powieksz licznik o jeden krok czasowy
        counter += dt
        #zapisywanie wykresu do pliku w wybranych chwilach czasowych: im dalej w czasie tym rzadziej
        if counter < 300 * dt:
            if counter % 10 * dt == 0:
                plot_and_save(data, counter, max, min)
        elif counter < 3000 * dt:
            if counter % 100 * dt == 0:
                plot_and_save(data, counter, max, min)
        else:
            if counter % 1000 * dt == 0:
                plot_and_save(data, counter, max, min)
    #wyliczanie ile czasu uplynelo
    end = time.time()
    print("Time elapsed: " + str(end - start))


#metoda zapisujaca wykresy do pliku
def plot_and_save(array, counter, max, min):
    plt.close()
    fig = plt.figure()
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    heatmap = plt.pcolor(array, cmap=plt.cm.seismic, vmin=min, vmax=max)
    if counter != "start":
        counter = "T = " + str(counter)
    fig.suptitle(
        counter + "s, Tmax = " + str(np.round(max, 3)) + "°C, Tmin = " + str(np.round(min, 3)) + "°C, ",
        fontsize=16)
    fig.colorbar(heatmap)
    name = "C:\studies\MPF\Lab02\pics\heatmap-" + counter + ".png"
    fig.savefig(name)


def find_edge_temp(array):
    #znajdz temperature maksymalna i minimalna, pomijajac obszary poza plytka
    Tmax = -10
    Tmin = 100
    for i in range(0, size):
        for j in range(0, size):
            if is_extended_T_edge(i, j):
                if array[i][j] > Tmax:
                    Tmax = array[i][j]
                if array[i][j] < Tmin:
                    Tmin = array[i][j]
    return Tmax, Tmin


def is_edge(i, j):
    if i == 0 or j == 0 or i == size - 1 or j == size - 1:
        return False
    return True


def is_T_edge(i, j):
    if not is_edge(i, j):
        return False
    if i < calculate_index(C) or i >= calculate_index(A - C - 1):
        if j >= calculate_index(D):
            return False
    return True


def is_extended_T_edge(i, j):
    if i < 10 or i > 31:
        if j > 7:
            return False
    return True


def calculate_edges(data):
    #utworz kopie danych a nastepnie wyznacz temperature brzegow zgodnie z warunkami von Neumana
    array = data.copy()
    for i in range(0, size):
        array[i][0] = data[i][1]
    for i in range(7, 32):
        array[i][size - 1] = data[i][size - 2]
    for i in range(0, 11):
        array[i][7] = data[i][6]
        array[i+31][7] = data[i+31][6]
    for j in range(0, 7):
        array[0][j] = data[1][j]
        array[size - 1][j] = data[size - 2][j]
    for j in range(7, size):
        array[10][j] = data[11][j]
        array[31][j] = data[30][j]
    return array


def recalculate(A):
    return int(np.floor(A / siatka))


plot_case_2()
