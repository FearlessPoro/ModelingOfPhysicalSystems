import matplotlib.pyplot as plt
import numpy as np

#Ustawianie parametrow poczatkowych
length = 100
width = 5
depth = 1
U = 0.1
D = 0.01
xi = 10
xe = 90
m = 1
dx = 1
dt = 1

#Wyznaczanie wartosci Cd i Ca
Cd = D * dt / dx ** 2
Ca = U * dt / dx

#wyznaczanie ilosci odcinkow, na ile podzielona jest rzeka
river_length = int(length / dx)
size = river_length

#inicjacja macierzy AA, BB oraz wektora c
AA = np.zeros((size, size))
BB = np.zeros((size, size))
c = np.zeros(size)
#"wrzucanie" wskaznika
c[int(xi / dx)] = m / (width * depth * dx)

#Wyznaczanie wartosci macierzy AA oraz BB
for i in range(size):
    AA[i, i] = 1 + Cd
    BB[i, i] = 1 - Cd
    if i + 1 < size:
        AA[i + 1, i] = - Cd / 2 - Ca / 4
        BB[i + 1, i] = Cd / 2 + Ca / 4
        AA[i, i + 1] = - Cd / 2 + Ca / 4
        BB[i, i + 1] = Cd / 2 - Ca / 4

#Wyznaczenie macierzy AB, czyli AA_inv * BB
AA_inv = np.linalg.inv(AA)
AB = np.matmul(AA_inv, BB)

#warunki Dirichleta dla 2 metody
for i in range(size):
    AB[0, i] = 0
    AB[size -1, size - 2] = AB[size -2, i]

#wyznaczanie wartosci jednej komorki w rzece pierwsza metoda
def f(x):
    #lewy warunek dirichleta
    if x < 2:
        return 0
    #prawy warunek dirichleta
    if x == river_length - 1:
        return c[x - 1]
    #wyznaczanie wartosci w kolejnej iteracji dla komorki x
    return c[x] + \
           (Cd * (1 - Ca) - (Ca / 6) * (pow(Ca, 2) - 3 * Ca + 2)) * c[x + 1] - \
           (Cd * (2 - 3 * Ca) - (Ca / 2) * (pow(Ca, 2) - 2 * Ca - 1)) * c[x] + \
           (Cd * (1 - 3 * Ca) - (Ca / 2) * (pow(Ca, 2) - Ca - 2)) * c[x - 1] + \
           (Cd * Ca + (Ca / 6) * (pow(Ca, 2) - 1)) * c[x - 2]


#metoda do wypisywania wykresu
def plot(table, i, method):
    plt.plot(river_to_plot, table)
    plt.ylim(-0.01, 0.05)
    plt.xlabel("Rzeka [m]")
    plt.ylabel("Znacznik [kg/m3]")
    plt.title(method + " Time=" + str(dt * i) + " U=" + str(U) + " D=" + str(D) + " m = " + str(round(sum_all(), 5)) + "kg")
    plt.savefig(method +"/" + method + "_Time=" + str(dt * i) + "_U=" + str(U) + "_D=" + str(D) + ".png")
    plt.close()

#wyznaczanie calkowitej masy znacznika w rzece
def sum_all():
    sum = 0
    for i in c:
        sum += i
    return sum * width * depth

#inicjacja rzeki dla pierwszej metody
i = 0
river_to_plot = []
for i in range(river_length):
    river_to_plot.append(i * dx)
#wykres dla warunkow poczatkowych
plot(c, 0, "Explicite")

#Petla zatrzymujaca sie gdy w rzece zostaje mniej niz 0.01kg znacznika
while sum_all() > 0.01:
    c_new = []
    #wyznaczanie wartosci w kolejnej iteracji
    for j in range(river_length):
        c_new.append(f(j))
    #Wyrysowanie co 1/U sekund
    if i % (1/U) == 0:
        plot(c, i, "Explicite")
    c = c_new
    i+= 1


#wyznaczenie druga metoda rznanczkina w nastepnej iteracji
def f2():
    return np.matmul(AB, c)


#wyzerowanie c i i
i = 0
c = np.zeros(size)
#ponowne wrzucenie znacznika do rzeki
c[int(xi / dx)] = m / (width * depth * dx)
#petla jak wyzej
while sum_all() > 0.01:
    c_new = f2()
    #wypisywanie rzeki jak wyzej
    if i % (1/U) == 0:
        plot(c, i, "Implicite")
    c = c_new
    i += 1
