import numpy as np
import math
import matplotlib.pyplot as plt


l = 100
dx = 1
T = 100
dt = 1
size = int(l / dx)
time = int(T / dt)

g = 6.67e-6 #stala grawitacji
h0 = 0.0e+00
Q0 = 0
hmax = 5.0e+00
A = 3 # stala szerokosc rzeki
dh = 0
S = dh / l
R = A / l
fdw = 5 # wspolczynnik weissbaha proponowane 10 ale moze byc dziwnie

to_plot_x = np.array(list(range(size)))
to_plot_t = np.array(list(range(time)))
slice_in_time = np.zeros(size)
h = np.zeros((time, size))
Q = np.zeros((time, size))
const = (fdw * l) / (8 * pow(A, 2) * hmax)


for i in range(int(size/2)):
    h[0][i] = hmax
for i in range(int(size/2), size):
    h[0][i] = h0


def calculate_h(t, x):
    return ((-1 / A) * ((Q[t][x + 1] - Q[t][x]) / dx)) * dt + h[t][x]


def calculate_Q(t, x):
    ret = (-1 * ((pow(Q[t][x+1], 2) - pow(Q[t][x-1], 2)) / A) / (2*dx) - const * Q[t][x] * math.fabs(Q[t][x]) - g * A * ((h[t+1][x+1] - h[t+1][x]) / dx - S)) * dt + Q[t][x]
    # if ret < -10:
    #     print("t: ", t , "x: ", x)
    return ret


def plot_h_at_time(t):
    #plt.ylim(0, 5)
    plt.plot(to_plot_x, h[t], "-")
    plt.xlabel("Rzeka [m]")
    plt.ylabel("Wysokosc wody [m]")
    plt.title("wysokosc rzeki w momencie " + str(t) + "s")
    #plt.legend(loc='upper right')
    #plt.savefig("tocmp_prediciton_tt= " + str(tt) + "Pe = " + str(Pe) + ".png")
    plt.show()
    plt.close()


def plot_h_at_x(x):
    plotter = np.zeros(time)
    for t in range(time):
        plotter[t] = h[t][x]
    #plt.ylim(0, 5)
    plt.plot(to_plot_t, plotter, "-")
    plt.xlabel("Czas [s]")
    plt.ylabel("Wysokosc wody [m]")
    plt.title("wysokosc rzeki w punkcie " + str(x) + "m")
    #plt.legend(loc='upper right')
    #plt.savefig("tocmp_prediciton_tt= " + str(tt) + "Pe = " + str(Pe) + ".png")
    plt.show()
    plt.close()


for t in range(time -1):
    h[t+1][0] = hmax # lewostronne h
    for x in range(1, size-1):
        h[t+1][x] = calculate_h(t, x)
    h[t+1][size - 1] = h0 # prawostronny warunek
    Q[t+1][0] = Q0 #lewostronny warunek
    for x in range(1, size - 1):
        Q[t+1][x] = calculate_Q(t, x)

#plot_h_at_time(1)
#plot_h_at_time(10)
plot_h_at_time(20)
#plot_h_at_x(50)

#plot_h_at_x(50)