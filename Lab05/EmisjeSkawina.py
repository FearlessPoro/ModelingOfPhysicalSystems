import math

h = 120  # [m]
emisje_rok = 150000  # [kg]
E = emisje_rok / (365 * 24 * 60 * 60)
T = 130 + 273.16
T0 = 10 + 273.16
d = 14  # m
v = 38  # m/s
x = 13000  # m

m = [0.080, 0.143, 0.196, 0.270, 0.363, 0.440]
a = [0.888, 0.865, 0.845, 0.818, 0.784, 0.756]
b = [1.284, 1.108, 0.978, 0.822, 0.660, 0.551]
g = [1.692, 1.781, 1.864, 1.995, 2.188, 2.372]
C1 = [0.213, 0.218, 0.224, 0.234, 0.251, 0.271]
Q = (math.pi * d * d) / 4 * (273.16 / T) * 1.3 * v * (T - T0)
z0 = 2.0
# predkosc wiatru
ua = [3, 5, 8, 11, 5, 4]
for i in range(6):
    u = ua[i] * pow(h / 14, m[i])  # predkosc wiatru u wylotu komina

    if v <= 0.5 * u:
        d_h = 0
    elif v >= u:
        d_h = (1.5 * v * d + 0.00974 * Q) / u
    else:
        d_h = ((1.5 * v * d + 0.00974 * Q) / u) * ((v - 0.5 * u) / (0.5 * u))

    H = h + d_h

    A = 0.088 * (6 * (pow(m[i], - 0.3)) + 1 - math.log(H / z0))
    B = 0.38 * pow(m[i], 1.3) * (8.7 - math.log(H / z0))

    ro_y = A * (pow(x, a[i]))  # wspol. poziomej dyfuzji atm
    ro_z = B * (pow(x, b[i]))  # wspol. pionowej dyfuzji atm

    S(i) = E / (2 * math.pi * u * ro_y * ro_z) * math.exp(1) ^ (-(H ^ 2) / (2 * (ro_y) ^ 2)) * 1000

# predkosc wiatru z komina
v = 1

figure(1)
plot(S, '*')
ylabel("Stezenie [g/m3]")
xlabel("Stan atmosfery")

i = 1
for ua2=[1:0.1: 11]
u = ua2 * ((h / 14) ^ m(4))
if v <= 0.5 * u
    d_h = 0
elseif
v >= u
d_h = (1.5 * v * d + 0.00974 * Q) / u
else
d_h = ((1.5 * v * d + 0.00974 * Q) / u) * ((v - 0.5 * u) / (0.5 * u));
end

H = h + d_h;

A = 0.088 * (6 * (m(4) ^ (-0.3)) + 1 - log(H / z0));
B = 0.38 * (m(4) ^ (1.3)) * (8.7 - log(H / z0));

ro_y = A * (x ^ a(4));
ro_z = B * (x ^ b(4));

S2(i) = E / (2 * pi * u * ro_y * ro_z) * exp(1) ^ (-(H ^ 2) / (2 * (ro_y) ^ 2)) * 1000;
i = i + 1;
end
ua2 = [1:0.1: 11];
figure(2);
plot(ua2, S2);
ylabel("Stezenie [g/m3]");
xlabel("Wiatr [m/s]");

% zaleznosc
od
odleglosci
dla
wiatru
odpowiedniego
dla
atm
k
i
stanu
atm
k
for k=[1:6]
i = 1;
for x=[0:10: 15090]
u = ua(k) * ((h / 14) ^ m(k));
if v <= 0.5 * u
    d_h = 0;
elseif
v >= u
d_h = (1.5 * v * d + 0.00974 * Q) / u;
else
d_h = ((1.5 * v * d + 0.00974 * Q) / u) * ((v - 0.5 * u) / (0.5 * u));
end

H = h + d_h;

A = 0.088 * (6 * (m(k) ^ (-0.3)) + 1 - log(H / z0));
B = 0.38 * (m(k) ^ (1.3)) * (8.7 - log(H / z0));

ro_y = A * (x ^ a(k));
ro_z = B * (x ^ b(k));

S3(k, i) = E / (2 * pi * u * ro_y * ro_z) * exp(1) ^ (-(H ^ 2) / (2 * (ro_y) ^ 2)) * 1000;
i = i + 1;
end
end
odl = [0:10: 15090];
figure(3);
% plot(odl, S3(k,:));
hold
on;
for k=[1:6]
plot(odl, S3(k,:));
end
hold
off;
ylabel("Stezenie [g/m3]");
xlabel("Odleglosc [m]");
legend('Stan 1', 'Stan 2', 'Stan 3', 'Stan 4', 'Stan 5', 'Stan 6');

% maksymalne
stê¿enie
for k=[1:6]
u = ua(k) * ((h / 14) ^ m(k));
if v <= 0.5 * u
    d_h = 0;
elseif
v >= u
d_h = (1.5 * v * d + 0.00974 * Q) / u;
else
d_h = ((1.5 * v * d + 0.00974 * Q) / u) * ((v - 0.5 * u) / (0.5 * u));
end

H = h + d_h;
A = 0.088 * (6 * (m(k) ^ (-0.3)) + 1 - log(H / z0));
B = 0.38 * (m(k) ^ (1.3)) * (8.7 - log(H / z0));

Smax(k) = C1(k) * E / (2 * u * A * B) * (B / H) ^ g(k) * 1000;
end
figure(4);
plot(Smax, '*');
ylabel("Stezenie maksmalne [g/m3]");
xlabel("Stan atmosfery");
