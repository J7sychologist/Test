# Описывает движение и взаимодействие молекул в потенциале Леннарда-Джонса

import matplotlib.pyplot as plt
from random import randint
from math import pi, sin, cos
import time

start_time = time.time()  # время начала выполнения

# Константы
k = 1.380649 * 10 ** (-23)  # постоянная Больцамана
Na = 6.02214 * 10**23  # число Авогадро
A = 1e-10  # Ангстрем
eV = 1.60218e-19  # электрон-вольт в Джоули

# Параметры Аргона
M = 39.948 * 10 ** (-3)  # молярная масса
t = 0  #  температура
r = 1.88 * A  # радиус атома
free = 3  # число степеней свободы
eps = 1.04e-2  # епсилон в Эв

D = eps * eV  # Максимальная энергия притяжения
R = 3.4 * A  # Расстояние нуля взаимодействия

dt = 5e-14  # шаг по времени
N_t = 5000  # количество шагов по времени
N_x = 15  # количество молекул по х
N_y = 15  # количество молекул по у

x_border = R * (N_x * 1.0 + 15)
y_border = R * (N_y * 1.0 + 15)
axs = [0, x_border, 0, y_border]  # оси

T = t + 273.15  # абсолютная температура
N = N_x * N_y  # количество молекул
m0 = M / Na  # масса одной молекулы
v_average = (free * k * T / m0) ** (1 / 2)  # средняя начальная скорость


# Отражение от стен
def reflect(s, v, border):
    if s[j] < 0:
        s[j] = -s[j]
        v[j] = -v[j]
    elif s[j] > border:
        s[j] = 2 * border - s[j]
        v[j] = -v[j]


# Случайная скорость
v_x = [0] * N
v_y = [0] * N
for i in range(N):
    alpha = randint(0, 360) * pi / 180
    v_x[i] = v_average * cos(alpha)
    v_y[i] = v_average * sin(alpha)
    v_x[i] *= 1 + randint(-100, 100) * 0.005
    v_y[i] *= 1 + randint(-100, 100) * 0.005

# Начальное распределение
x, y = [0] * N, [0] * N
n = -1
for n_x in range(N_x):
    for n_y in range(N_y):
        n += 1
        x[n] = R * (n_x * 1.5 + 3.5)
        y[n] = R * (n_y * 1.5 + 3.5)

# Создаем объект графики
fig, ax = plt.subplots(figsize=(8, 8))

# Подготовка предиктора
x_cor, y_cor = [0] * N, [0] * N
vx_cor, vy_cor = [0] * N, [0] * N

# Основной цикл
for i in range(N_t):
    for j in range(N):
        x_cor[j] = x[j] + dt * v_x[j]
        y_cor[j] = y[j] + dt * v_y[j]

    # Обнуление взаимодействий
    a_x, a_y = [0] * N, [0] * N

    for n in range(N):
        for m in range(N):
            if n != m:
                # Расстояние между двумя молекулами
                distance = (
                    (x_cor[n] - x_cor[m]) ** 2 + (y_cor[n] - y_cor[m]) ** 2
                ) ** (1 / 2)
                if distance <= 3 * R:
                    # Сила взаимодействия по потенциалу леннарда-джонса
                    f = 12 * D / R * (2 * (R / distance) ** 13 - (R / distance) ** 7)
                    a_x[n] += f * (x_cor[n] - x_cor[m]) / (m0 * distance)
                    a_y[n] += f * (y_cor[n] - y_cor[m]) / (m0 * distance)

    for j in range(N):
        vx_cor[j] = v_x[j] + dt * a_x[j]
        vy_cor[j] = v_y[j] + dt * a_y[j]

        v_x[j] = 0.5 * (v_x[j] + vx_cor[j])
        v_y[j] = 0.5 * (v_y[j] + vy_cor[j])

        x[j] += dt * v_x[j]
        y[j] += dt * v_y[j]

        reflect(x, v_x, x_border)
        reflect(y, v_y, y_border)

        ax.add_artist(plt.Circle((x[j], y[j]), r))

    ax.set_aspect("equal", adjustable="box")
    ax.axis(axs)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.pause(0.1)
    ax.clear()

# plt.show()

end_time = time.time()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения

print(f"Время выполнения программы: {execution_time} секунд")

