import math
import csv
import scipy.integrate
import matplotlib.pyplot as plt
import numpy as np

tt = 10
lambd = math.log(2)/148
Pe = 10

#Wyznaczanie wartosci funkcji przejscia w modelu eksponencjalnym
def g_2(t, tt):
    return math.pow(tt, -1) * math.exp(-t / tt)

#wyznaczanie wartosci calki w modelu eksponencjalnym
def C(t, tt):
    Y = np.zeros(t)
    for i in range(0, t):
        Y[i] = input_data[i] * g_2(t - i, tt) * math.exp(-lambd * (t - i))
    return scipy.integrate.trapz(Y, dx=1.0)

#wyznaczanie wartosci funkcji przejscia w modelu dyspersyjnym
def g_3(t, tt, Pe):
    return pow(4 * math.pi * Pe * t / tt, -1 / 2) * 1 / t * (math.exp(-1 * (pow(1 - t/tt, 2)/(4 * Pe * t/tt))))

#wyznaczanie wartosci calki w modelu dyspersyjnym
def C_3(t, tt, Pe):
    Y = np.zeros(t)
    for i in range(0, t):
        Y[i] = input_data[i] * g_3(t - i, tt, Pe) * math.exp(-lambd * (t - i))
    return scipy.integrate.trapz(Y, dx=1.0)

#metoda wczytujaca dane z plikow, przerobionych recznie na pliki csv
def load_data(model_csv, input_csv):
    with open(model_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar="|")
        for row in reader:
            month, value = row
            model_data.append(float(value))
            months.append(int(month))

    with open(input_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar="|")
        for row in reader:
            month, value = row
            input_data.append(float(value))


#metoda wypisujaca wykres
def plot(table, tt, Pe):
    plt.plot(months[162:], table[162:], "-", label="wynik")
    plt.plot(months, model_data, ".", label="dane modelowe")
    plt.plot(months[tt:162], table[tt:162], "--", label="przewidywanie")
    plt.plot(months[:tt], table[:tt], "--", label="niewystarczajaca ilosc danych")
    plt.xlabel("Czas (miesiace)")
    plt.ylabel("Ilosc trytu w rzece")
    plt.title("tt= " + str(tt) + "Pe = " + str(Pe))
    plt.legend(loc='upper right')
    plt.savefig("tocmp_prediciton_tt= " + str(tt) + "Pe = " + str(Pe) + ".png")
    plt.show()
    plt.close()

#inicjowanie uzywanych zmiennych
model_data = []
input_data = []
months = []
best_Pe = -1
best_tt = -1
differences_min = 999999999999
load_data("dunaj.csv", "opady.csv")

#metoda wyznaczajaca wartosc calki splotu dla zadanych parametrow tt i Pe dla metody dyspersyjnej
def try_parameters_3(tt, Pe):
    global i
    output_data = []
    for i in range(tt):
        output_data.append(0)
    for i in range(tt, len(model_data)):
        output_data.append(C_3(i, tt, Pe))
    return output_data


#metoda wyznaczajaca wartosc calki splotu dla zadanych parametrow tt i Pe dla metody dyspersyjnej
def try_parameters_2(tt):
    global i
    output_data = []
    for i in range(tt):
        output_data.append(0)
    for i in range(tt, len(model_data)):
        output_data.append(C(i, tt))
    return output_data

#podwojna petla iterujaca po wartosciach Pe i tt w celu wyznacznia opty
for i in range(1, 130):
    Pe = i/10
    for j in range(1, 130):
        tt = j
        output_data = try_parameters_3(tt, Pe)
        differences = 0
        #wyznaczanie bledu sredniokwadratowego w celu znalezienia najdokladniejszej metody
        for k in range(162, len(output_data)):
            differences += (output_data[k] - model_data[k])**2
        if differences_min > differences:
            differences_min = differences
            best_tt = tt
            best_Pe = Pe
        print("tt = " + str(tt) + "Pe = " + str(Pe) + "difference sum: " + str(differences))

#wypisywanie wykresu najblizszego danym modelowym
output_data = try_parameters_3(best_tt, best_Pe)
plot(output_data, best_tt, best_Pe)


