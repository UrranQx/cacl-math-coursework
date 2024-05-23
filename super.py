"""
lambda1 = y * 31.66675 * 10**(-5),
    где y - корень уравнения:
    2 * sqrt(x) = cos((PI*x)/2)
    x ~= 0.221050639495735

lambda2 = -z * 3.039830 * 10**(-5),
    где z - значение, минимизирующее f(z) на [-2, -1]
    f(z) =
= (e**z)*(2*z**2-4) + (2*z**2-1)**2 + e**(2*z) - 3*z**4


EFF = (E_в / E) * 100% =
64.77 / (T**4) * integrate from lambda1 to lambda 2:
    dx / ((x**5) * (e**(1.432/(T*x)) - 1)
Calculate EFF from T = 1000 K to 9000 K with step 1000 K

По полученным данным построить график светимости от
температуры, взяв достаточное количество точек.

Оценить погрешность результата и влияние на
точность погрешности в задании лямбда1 и лямбда2

"""
import matplotlib.pyplot as plt
import scipy.optimize as optimize
from scipy.integrate import quad
import numpy as np
from math import sqrt, cos, pi

accuracy = 1e-16


def fun_x(x):
    return 2 * sqrt(x[0]) - cos((pi * x[0]) / 2)


def fun_z(z):
    return (np.e ** z) * (2 * z ** 2 - 4) + (2 * z ** 2 - 1) ** 2 + np.e ** (2 * z) - 3 * z ** 4


def get_lambdas(accuracy, fun_x, fun_z):
    res_x = optimize.fsolve(fun_x, np.array([0]), xtol=accuracy)
    print(res_x)
    # [0.22105064]

    lower_bound = -2
    upper_bound = -1
    bounds = optimize.Bounds(lower_bound, upper_bound)
    res_z = optimize.minimize(fun_z,
                              np.array((lower_bound + upper_bound) / 2),
                              bounds=bounds,
                              method='TNC',
                              tol=accuracy).x
    print(res_z)
    # [-1.3159745]
    L_1 = res_x[0] * 31.66675 * 10 ** (-5)
    L_2 = -res_z[0] * 3.039830 * 10 ** (-5)
    print(f'lambda_1 = {L_1}\nlambda_2 = {L_2}')

    # lambda_1 = 6.999955338251561e-05
    # lambda_2 = 4.00033875088364e-05
    return sorted([L_1, L_2])


def integrand(x, T):
    return 1 / ((x ** 5) * (np.exp(1.432 / (T * x)) - 1))


def EFF(T, l_bound, u_bound):
    return (
            64.77 / (T ** 4) * quad(integrand, l_bound, u_bound, args=T, epsabs=accuracy)[0]
    )


def calculate_EFF(lambda_1, lambda_2, label='EFF'):
    ans = []
    T0 = 1000
    step = 1000
    for i in range(9):
        T = T0 + i * step
        t_res = EFF(T, lambda_1, lambda_2)
        ans.append(t_res)

    T_values = list(range(T0, T0 + step * len(ans), step))

    return ans, T_values


lambda_1, lambda_2 = get_lambdas(accuracy, fun_x, fun_z)
# Вычислим EFF с исходными значениями lambda
original_EFF, T_values = calculate_EFF(lambda_1, lambda_2)

# Создадим некоторое отклонение от исходных значений lambda
delta = 1e-6
accuracy = 1e-16  # А также изменим немного точность, при которых были вычислены х и z: default - 1e-16

new_lambdas = get_lambdas(accuracy, fun_x, fun_z)
lambda_1_new = new_lambdas[0] + lambda_1 * 0.01  # delta * np.random.uniform(-1, 1)
lambda_2_new = new_lambdas[1] + lambda_2 * 0.01  # delta * np.random.uniform(-1, 1)

print(f"Original lambda_1: {lambda_1}, Original lambda_2: {lambda_2}")
print(f"New lambda_1: {lambda_1_new}, New lambda_2: {lambda_2_new}")
print(f"Difference in lambda_1: {np.abs(lambda_1 - lambda_1_new)}")
print(f"Difference in lambda_2: {np.abs(lambda_2 - lambda_2_new)}")
# Calculate EFF with new lambda values
new_EFF, T_values2 = calculate_EFF(lambda_1_new, lambda_2_new, label='New EFF')

plt.figure(figsize=(10, 6))
plt.plot(T_values, original_EFF, marker='o')
plt.title('EFF and new EFF vs T')
plt.xlabel('Temperature (T)')
plt.ylabel('EFF')
plt.plot(T_values2, new_EFF, marker='o', color='green')
plt.legend(['Original EFF', 'New EFF'])
plt.grid(True)
plt.show()

# Calculate the difference between the original and new EFF values
diff_EFF = np.abs(np.array(original_EFF) - np.array(new_EFF))
div_diff_EFF = np.abs((np.array(original_EFF) - np.array(new_EFF)) / np.array(original_EFF)) * 100

print(f"Original EFF: {original_EFF}")
print(f"New EFF: {new_EFF}")
print(f"Difference in EFF: {diff_EFF}")
print(f"div_diff_EFF: {div_diff_EFF}")

plt.figure(figsize=(10, 6))
plt.plot(T_values, diff_EFF, marker='o', color='red')
plt.title('Difference in EFF vs T')
plt.xlabel('Temperature (T)')
plt.ylabel('Difference in EFF')
plt.grid(True)

plt.show()
