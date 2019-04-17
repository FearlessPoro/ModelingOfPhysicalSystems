import matplotlib.pyplot as plt

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
c = []
Cd = D * dt / dx ** 2
Ca = U * dt / dx

river_lenght = int(length / dx)


def f(x):
    if x < 2:
        return 0
    if x == river_lenght - 1:
        return c[x - 1]
    return c[x] +\
           (Cd * (1 - Ca) - (Ca / 6) * (pow(Ca, 2) - 3 * Ca + 2)) * c[x + 1] - \
           (Cd * (2 - 3 * Ca) - (Ca / 2) * (pow(Ca, 2) - 2 * Ca - 1)) * c[x] + \
           (Cd * (1 - 3 * Ca) - (Ca / 2) * (pow(Ca, 2) - Ca - 2)) * c[x - 1] + \
           (Cd * Ca + (Ca / 6) * (pow(Ca, 2) - 1)) * c[x - 2]


def initiate_river():
    global i
    for i in range(river_lenght):
        c.append(0)
    c[int(xi / dx)] = m / (width * depth * dx)


def plot(table, i):
    plt.plot(river_to_plot, table)
    plt.ylim(-0.01, 0.05)
    plt.xlabel("Rzeka [m]")
    plt.ylabel("Znacznik [kg/m3]")
    plt.title("Time = " + str(dt * i) + "s, m = " + str(sum_all())+ "kg")
    plt.show()
    plt.close()


def sum_all():
    sum = 0
    for i in c:
        sum += i
    return sum * width * depth


initiate_river()
river_to_plot = []
for i in range(river_lenght):
    river_to_plot.append(i * dx)
plot(c, 0)

for i in range(2000):
    c_new = []
    for j in range(river_lenght):
        c_new.append(f(j))
    if i % 10 == 0:
        plot(c_new, i)
    c = c_new

