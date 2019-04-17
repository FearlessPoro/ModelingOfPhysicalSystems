import matplotlib.pyplot as plt
import sage
from scipy.optimize import fsolve

S_default = 1366 # 70% tej wart 130%
A = 0.3
E = 0.9 # dla modelu nieuproszczonego mozna porównać z modelem uproszczonym 1
boltzman = 5.67e-8  # stala Stafana Boltzmana
a_s = 0.19
t_a = 0.53
a_a = 0.30
t_a_ = 0.06
a_a_ = 0.31
c = 2.7
T = 0
S = 0

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def calculate_temperature(sun_radiation):
    sun_constant = S_default * (sun_radiation / 100)
    return pow((sun_constant / (4 * boltzman * E)) * (1 - A), 1 / 4)

# procenty = []
# temperatury = []
# for i in reversed(range(70, 131)):
#     procenty.append(i)
#     temperatury.append(kelvin_to_celsius(calculate_temperature(i)))
#
# plt.plot(procenty, temperatury)
# plt.ylabel('średnia temperatura powierzchni[°C]')
# plt.xlabel('Stała słoneczna [% wartości domyślnej]')
# plt.title('Wpływ stałej słonecznej na średnią temperaturę planety')
# plt.savefig("normal.png")
# plt.show()

print(T)


def solve_equation(percent):
    S = S_default * percent/100

    def f(variables):
        (T_s, T_a) = variables

        first_eq = ((-t_a) * (1.0 - a_s) * S / 4.0) + (c * (T_s - T_a)) + (boltzman * pow(T_s, 4) * (1.0 - a_a_)) -\
                   (boltzman * pow(T_a, 4))
        second_eq = -((1.0 - a_a - t_a + (a_s * t_a)) * S / 4.0) - (c * (T_s - T_a)) - (boltzman * pow(T_s, 4) * (1.0 - t_a_ - a_a_)) + (2.0 * boltzman * pow(T_a, 4))
        return first_eq, second_eq

    return fsolve(f, (273, 273))


procenty = []
t_atm = []
t_pow  = []
for i in reversed(range(80, 121)):
    procenty.append(i)
    (a, s) = solve_equation(i)
    t_atm.append(kelvin_to_celsius(a))
    t_pow.append(kelvin_to_celsius(s))
    if kelvin_to_celsius(a) <= 0.5:
        a_s = 0.65
plt.close()
plt.plot(procenty, t_atm, label='Temperatura atmosfery')
plt.plot(procenty, t_pow, label='Temperatura powierzchni')
plt.ylabel('średnia temperatura powierzchni[°C]')
plt.xlabel('Stała słoneczna [% wartości domyślnej]')
plt.title('Wpływ stałej słonecznej na średnią temperaturę planety')
plt.legend()
plt.savefig("drugie_albedo.png")
plt.show()
#print('T_s (powierzchni): {}[st. C], T_a (atmosfery): {}[st. C]'.format(kelvin_to_celsius(T_s), kelvin_to_celsius(T_a)))

#TODO jesli temperatura ponizej 0.5 stopnia to albedo zmienia sie z 0.19 do 0.65
# bez punktu 7