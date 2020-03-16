import random
import math
import numpy


def dispersion(array_y, array_y_average):
    array_dispersion = []

    for j in range(N):
        array_dispersion.append(0)
        for g in range(m):
            array_dispersion[j] += (array_y[j][g] - array_y_average[j])**2
        array_dispersion[j] /= m
    return array_dispersion


def cohren(y_array, y_average_array):
    dispersion_array = dispersion(y_array, y_average_array)
    max_dispersion = max(dispersion_array)
    Gp = max_dispersion/sum(dispersion_array)
    return Gp < Gt[m-1]


def student(y_array, y_average_array):
    general_dispersion = sum(dispersion(y_array, y_average_array)) / N
    statistic_dispersion = math.sqrt(general_dispersion / (N*m))
    beta = []
    for i in range(N):
        b = 0
        for j in range(3):
            b += y_average_array[i] * xn[i][j]
        beta.append(b / N)
    ts = [abs(beta[i]) / statistic_dispersion for i in range(N)]
    f3 = (m-1)*N
    return ts[0] > tt[f3], ts[1] > tt[f3], ts[2] > tt[f3], ts[3] > tt[f3]


def coef(x_array, y_average_array):
    mx1 = sum([x_array[i][0] for i in range(N)]) / N
    mx2 = sum([x_array[i][1] for i in range(N)]) / N
    mx3 = sum([x_array[i][2] for i in range(N)]) / N
    my = sum(y_average_array) / N
    a11 = sum([x_array[i][0]**2 for i in range(N)]) / N
    a22 = sum([x_array[i][1]**2 for i in range(N)]) / N
    a33 = sum([x_array[i][2]**2 for i in range(N)]) / N
    a12 = sum([x_array[i][0]*x_array[i][1] for i in range(N)]) / N
    a13 = sum([x_array[i][0]*x_array[i][2] for i in range(N)]) / N
    a23 = sum([x_array[i][1]*x_array[i][2] for i in range(N)]) / N
    a1 = sum([x_array[i][0]*y_average_array[i] for i in range(N)]) / N
    a2 = sum([x_array[i][1]*y_average_array[i] for i in range(N)]) / N
    a3 = sum([x_array[i][2]*y_average_array[i] for i in range(N)]) / N
    a = numpy.array([[1, mx1, mx2, mx3], [mx1, a11, a12, a13], [mx2, a12, a22, a23], [mx3, a13, a23, a33]])
    c = numpy.array([[my], [a1], [a2], [a3]])
    b = numpy.linalg.solve(a, c)
    return b


def fisher(y_average_array, y0_array, y_array):
    dispersion_adequacy = 0
    for i in range(N):
        dispersion_adequacy += (y0_array[i] - y_average_array[i]) ** 2
    dispersion_adequacy = dispersion_adequacy * m / (4 - d)
    dispersion_reproducibility = sum(dispersion(y_array, y_average_array)) / N
    Fp = dispersion_adequacy / dispersion_reproducibility
    f3 = (m-1)*N
    f4 = N - d
    return Fp < Ft[f4][f3]


x1_min = -30
x1_max = 20
x2_min = -30
x2_max = 45
x3_min = -30
x3_max = -15
y_min = 170
y_max = 217

xn = [
    [-1, -1, -1],
    [-1, +1, +1],
    [+1, -1, +1],
    [+1, +1, -1]
]
x = [
    [-30, -30, -30],
    [-30, 45, -15],
    [20, -30, -15],
    [20, 45, -30]
]

m = 3
N = 4
y = [[random.randint(y_min, y_max) for _ in range(m)] for _ in range(N)]
y_average = [sum(y[i])/m for i in range(N)]
condition_cohren = False
Gt = {1: 0.9065, 2: 0.7679, 3: 0.6841, 4: 0.6287, 5: 0.5892, 6: 0.5598, 7: 0.5365, 8: 0.5175, 9: 0.5017, 10: 0.4884}
tt = {4: 2.776, 8: 2.306, 12: 2.179, 16: 2.120, 20: 2.086, 24: 2.064, 28: 2.048}
Ft = {1: {4: 7.7, 8: 5.3, 12: 4.8, 16: 4.5, 20: 4.4, 24: 4.3, 28: 4.2},
      2: {4: 6.9, 8: 4.5, 12: 3.9, 16: 3.6, 20: 3.5, 24: 3.4, 28: 3.3},
      3: {4: 6.6, 8: 4.1, 12: 3.5, 16: 3.2, 20: 3.1, 24: 3.0, 28: 3.0},
      4: {4: 6.4, 8: 3.8, 12: 3.3, 16: 3.0, 20: 2.9, 24: 2.8, 28: 2.7},
      5: {4: 6.3, 8: 3.7, 12: 3.1, 16: 2.9, 20: 2.7, 24: 2.6, 28: 2.6},
      6: {4: 6.2, 8: 3.6, 12: 3.0, 16: 2.7, 20: 2.6, 24: 2.5, 28: 2.4}}


while not condition_cohren:
    condition_cohren = cohren(y, y_average)
    if not condition_cohren:
        m += 1
        for i in range(N):
            y[i].append(random.randint(y_min, y_max))
condition_student = student(y, y_average)
d = sum(condition_student)
b = [coef(x, y_average)[i][0]*condition_student[i] for i in range(N)]
yo = []
for i in range(4):
    yo.append(b[0] + b[1] * x[i][0] + b[2] * x[i][1] + b[3] * x[i][2])
if d != N:
    condition_fisher = fisher(y_average, yo, y)
else:
    condition_fisher = True

print('x1 min:', x1_min, '  x1 max:', x1_max)
print('x2 min:', x2_min, '  x2 max:', x2_max)
print('x3 min:', x3_min, '  x3 max:', x3_max)
print('y min:', y_min, ' y max:', y_max)
print()
print(f'Отримане рівняння регресії при m={m}:')
print(f'y = {b[0]:.2f} + {b[1]:.2f} x1 + {b[2]:.2f} x2 + {b[3]:.2f} x3')
print('Перевірка:')
for i in range(N):
    print(f'Yc{i+1:.2f}={y_average[i]:.2f}')
    print(f'Y{i+1:.2f}={y_average[i]:.2f}')
print(f'Кількість значущих коефіцієнтів:{d}')
if condition_fisher:
    print('Отримана математична модель адекватна експериментальним даним')
else:
    print('Рівняння регресії неадекватно оригіналу')




