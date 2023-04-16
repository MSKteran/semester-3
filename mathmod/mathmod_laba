import math
import matplotlib.pyplot as plt
import numpy as np


# Определяем функцию f(x, y) для метода Рунге-Кутта
def f(sumval1, sumval2):
	return (x[i] + sumval1) * math.exp(-((x[i] + sumval1) ** 2)) - 2 * (x[i] + sumval1) * (y2[i] + sumval2)


# Создаем список значений от 0 до 1 с шагом h
h = 0.005
split_num = int(1 / h) + 1
x = np.linspace(0, 1, split_num)

# Создаем списки значений для метода Эйлера, Рунге-кутта и аналитического
# Указываем их изначальные состояния
y1 = np.zeros(len(x))
y1[0] = 1

y2 = np.zeros(len(x))
y2[0] = 1

y3 = np.zeros(len(x))
y3[0] = 1

# Заполнение списков значениями
for i in range(len(x) - 1):
	# Метод Эйлера
	y1[i + 1] = y1[i] + h * (x[i] * math.exp(-(x[i] ** 2)) - 2 * x[i] * y1[i])

	# Метод Рунге-Кутта 4 порядка
	k1 = h * f(0, 0)
	k2 = h * f(h / 2, k1 / 2)
	k3 = h * f(h / 2, k2 / 2)
	k4 = h * f(h, k3)
	y2[i + 1] = y2[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6

	# Аналитический метод
	y3[i + 1] = (x[i + 1] ** 2 + 2) / (2 * math.exp(x[i + 1] ** 2))

# Список всех y в виде: y1 y2 y3 с точностью до 4 цифр
print('{:<10} {:<10} {:<10} {:<10}'.format('x', 'Эйлер', 'Рунге-Кутт', 'Аналитика'))
for i in range(len(x)):
	x_i = "%.2f" % x[i]
	y_euler = "%.4f" % y1[i]
	y_rk = "%.4f" % y2[i]
	y_analytic = "%.4f" % y3[i]
	print('{:<10} {:<10} {:<10} {:<10}'.format(x_i, y_euler, y_rk, y_analytic))

print('\n', '\n')

# Вывод всех y(b) и каждой погрешности
print(f'''Аналитика:
y(b) = {"%.4f" % y3[-1]},

Эйлер:
y(b) = {"%.4f" % y1[-1]},
Погрешность Эйлера = {abs(float(y1[-1]) - float(y3[-1]))},

Рунге-Кутт:
y(b) = {"%.4f" % y2[-1]},
Погрешность Рунге-Кутта = {abs(float(y2[-1]) - float(y3[-1]))}.''')

# Построение графика
plt.plot(x, y1, label="Метод Эйлера", color='green')
plt.plot(x, y2, label="Метод Рунга-Кутта 4 порядка", linestyle='--', color='red')
plt.plot(x, y3, label="Аналитический метод", linestyle=':', color='black')
plt.legend()
plt.show()
