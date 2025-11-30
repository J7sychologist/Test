"""Блок импорта"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style


"""Блок задания начальных значений (можно менять)"""
axis = 2 # ось "оу"
N = 250 # количество итераций (не трогаем, пока не разберемся)
diss = 0.75 # коэффициент затухания после удара (0-1)
x_start = 0.7 # позиция корзины по X (от 0 до 1), относительная величина
y_start = 0.15 # позиция корзины по Y (от 0 до 1)


"""Блок функций"""
# Получение параметров от пользователя
def get_user_input():
    print("\nВы пытаетесь попасть мячом в корзину. С какой силой и под каким углом бросите мяч?")
    while True:
        try:
            v = float(input("\nНачальная скорость (1-15 м/с) = "))
            angle = float(input("Угол броска (0-90 градусов) = "))
            if 1 <= v <= 15 and 0 <= angle <= 90:
                return v, angle
            else:
                print("Скорость должна быть 1-15 м/с, угол 0-90 градусов")
        except ValueError:
            print("Пожалуйста, введите числа!")
        except KeyboardInterrupt:
            print("\nОтключаюсь...")
            exit()

# Константы, начальные значения, инициализация
def initialization():
    global R, angle, alpha
    global x, y, vx, vy, ax, ay

    g = 9.81  # ускорение свободного падения
    R = 0.1 # радиус мяча (не трогать)
    # Преобразование градусов в радианы (не трогать)
    alpha = angle
    angle = np.radians(angle) # угол полета
    # Начальные координаты (можно менять)
    x = R
    y = R
    # Начальная скорость
    vx = v * np.cos(angle)
    vy = v * np.sin(angle)
    # Ускорения (можно менять)
    ax = 0
    ay = -g

# Предрасчеты (не трогать)
def preprocessing():
    global wid, dwid
    global xlim, ylim   
    global cx, cy
    global dt, flag

    wid, dwid = 7, 2 # соотношение размеров холста
    dt = 7e-03  # величина шага по времени, с
    flag = False # попал или не попал
    # Размеры осей
    xlim = axis * dwid
    ylim = axis
    # Для корзины
    xdif = 0.06
    ydif = 0.1
    cx = [x_start * xlim, (x_start + 0.5 * xdif) * xlim, (x_start + 2 * xdif) * xlim, (x_start + 2.5 * xdif) * xlim]
    cy = [y_start * ylim, (y_start + ydif) * ylim, (y_start + 4 * ydif) * ylim]

# Отражение от границ (не трогать)
def reflection(coor, vel, lim):
    if (coor - R) <= 0:
        vel = -diss * vel
        coor += R - coor
    if (coor + R) >= lim and coor < lim:
        vel = - diss * vel
        coor += lim - (coor + R)
    if coor >= lim:
        vel = -diss * vel
        coor += lim - coor
    return coor, vel

# Отражение от стенок корзины (не трогать)
def reflect():
    global x, vx, y, vy

    if (x + R) >= cx[0] and (x + R) < cx[0] * 1.1 and (y + R) > cy[0] * 1.1 and (y - R) < cy[2] * 0.9 :
        vx = -diss * vx
        x += cx[0] - (x + R)
    if (x - R) <= cx[1] and (x - R) > cx[1] * 0.9 and (y + R) > cy[1] * 1.1 and (y - R) < cy[2] * 0.9 :
        vx = -diss * vx
        x += cx[1] - (x - R)        
    if (x + R) >= cx[2] and (x + R) < cx[2] * 1.02 and (y + R) > cy[1] * 1.1 and (y - R) < cy[2] * 0.9:
        vx = -diss * vx
        x += cx[2] - (x + R)
    if (x - R) <= cx[3] and (x - R) > cx[3] * 0.98 and (y + R) > cy[0] * 1.1 and (y - R) < cy[2] * 0.9:
        vx = -diss * vx
        x += cx[3] - (x - R)

    if (x + R) > (cx[0] * 1.01) and (x - R) < (cx[1] * 0.99) and (y - R) <= (cy[2]) and (y - R) > (cy[2] * 0.9):
        vy = -diss * vy
        y += cy[2] - (y - R)
    if (x + R) > cx[2] * 1.01 and (x - R) < cx[3] * 0.99 and (y - R) <= cy[2] and (y - R) > cy[2] * 0.9:
        vy = -diss * vy
        y += cy[2] - (y - R)
    if (x + R) > cx[1] * 1.01 and (x - R) < cx[2] * 0.99 and (y - R) <= cy[1] and (y - R) > cy[1] * 0.9:
        vy = -diss * vy
        y += cy[1] - (y - R)
    if (x + R) > cx[0] * 1.01 and (x - R) < cx[3] * 0.99 and (y + R) >= cy[0] and (y + R) < cy[0] * 1.1:
        vy = -diss * vy
        y += cy[0] - (y + R)

# Отрисовка корзины (не трогать)
def garbage():
    axs.plot([cx[0], cx[0]], [cy[0], cy[2]], color="white")
    axs.plot([cx[0], cx[1]], [cy[2], cy[2]], color="white")
    axs.plot([cx[1], cx[1]], [cy[2], cy[1]], color="white")
    axs.plot([cx[1], cx[2]], [cy[1], cy[1]], color="white")
    axs.plot([cx[2], cx[2]], [cy[1], cy[2]], color="white")
    axs.plot([cx[2], cx[3]], [cy[2], cy[2]], color="white")
    axs.plot([cx[3], cx[3]], [cy[2], cy[0]], color="white")
    axs.plot([cx[3], cx[0]], [cy[0], cy[0]], color="white")

# Функция, рассчитывающая изменение скорости и координаты мяча (не трогать)
def position():
    global vx, x, vy, y
    vx += dt * ax
    x += dt * vx
    vy += dt * ay
    y += dt * vy
    x, vx = reflection(x, vx, xlim)
    y, vy = reflection(y, vy, ylim)
    reflect()
    return x, y

# Выстрел и анимация полета (не трогать)
def shot():
    global flag

    x, y = position()
    new_circle = plt.Circle((x, y), R, color="blue")
    axs.clear()
    if x >= cx[1] and x <= cx[2] and y >= cy[1] and y < cy[2]:
        flag = True
        axs.set_title(f"Гооооооол!, v={v}, angle={alpha}", color='green', fontsize=16)
    elif i == N - 1 and not flag:
        axs.set_title(f"Мимо! 😞, v={v}, angle={alpha}", color='red', fontsize=16)
    else:
        axs.set_title(f"Мяч летит..., v={v}, angle={alpha}", color='yellow', fontsize=14)
    axs.set_ylim(0, axis)
    axs.set_xlim(0, dwid * axis)
    axs.add_artist(new_circle)
    garbage()
    plt.pause(1e-2)


"""Основная часть программы"""
def main():
    global axs, i
    global v, angle

    v, angle = get_user_input()
    initialization()
    preprocessing()
    plt.style.use('dark_background')
    fig, axs = plt.subplots(figsize=(wid * dwid, wid))
    for i in range(N):
        shot()
    plt.show()

# Точка входа в программу
if __name__ == "__main__":
    try:
        while(True):
            main()
            if not flag:
                print("\nПопробуйте еще раз!")
    except KeyboardInterrupt:
        print("\nОтключаюсь...")
        exit()