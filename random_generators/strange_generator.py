import sympy as sp
import numpy as np
from .random_generator import RandomGenerator
from .uniform_generator import UniformRandomGenerator

# class TwoLinesRandomGenerator(RandomGenerator):
#     def __init__(self, k_val, phi_val):
#         # Объявляем символьные переменные
#         x, k, phi = sp.symbols(r'x k \phi')
#         # Вычисляем c
#         c = sp.sqrt(2/(k*(1+k**2)))
#         # Создаем генератор равномерного распределения
#         self.uniform = UniformRandomGenerator()
#         # Вычисляем значение c
#         c_val = c.subs(k, k_val)
        
#         # Правильно интегрируем и упрощаем функции распределения
#         self.distribution_function_1 = sp.integrate(c - 1/k*(x - phi), (x, phi, x)).simplify()
#         # Важно: добавляем значение F1 в начальной точке второго интервала для обеспечения непрерывности функции распределения
#         self.distribution_function_2 = sp.integrate(-c + 1/k*(x - phi), (x, k*c + phi, x)).simplify() + self.distribution_function_1.subs(x, k*c + phi)

#         # Подставляем значения k и phi
#         self.distribution_function_1 = self.distribution_function_1.subs({k: k_val, phi: phi_val})
#         self.distribution_function_2 = self.distribution_function_2.subs({k: k_val, phi: phi_val})

#         # Объявляем символьную переменную y
#         y = sp.symbols('y')
#         # Решаем уравнения для обратных функций и берем первое решение (должно быть только одно)
#         self.inverse_function_1 = sp.solve(self.distribution_function_1 - y, x)[0]
#         self.vectorized_function_1 = sp.lambdify(y, self.inverse_function_1, 'numpy')

#         self.inverse_function_2 = sp.solve(self.distribution_function_2 - y, x)[0]
#         self.vectorized_function_2 = sp.lambdify(y, self.inverse_function_2, 'numpy')

#         # Вычисляем интервалы напрямую, используя функции распределения
#         self.interval_1 = (0, self.distribution_function_1.subs(x, k_val*c_val + phi_val).evalf())
#         self.interval_2 = (self.interval_1[1], self.distribution_function_2.subs(x, phi_val + k_val*c_val*(1+k_val)).evalf())


#     def getNext(self, N):
#         # Генерируем равномерно распределенные числа
#         y = self.uniform.getNext(N)
        
#         # Используем булеву индексацию для эффективности:
#         random_values_1 = self.vectorized_function_1(y[np.logical_and(y >= self.interval_1[0], y <= self.interval_1[1])])
#         random_values_2 = self.vectorized_function_2(y[np.logical_and(y > self.interval_1[1], y <= self.interval_2[1])])

#         # Объединяем результаты
#         return np.concatenate([random_values_1, random_values_2])


# # Функция find_extrema_on_interval больше не нужна, так как интервалы вычисляются напрямую.

class TwoLinesRandomGenerator(RandomGenerator):
    def __init__(self, k_val, phi_val):
        self.k = k_val
        self.phi = phi_val
        self.c = np.sqrt(2/(self.k*(self.k**2+1)))
        self.uniform = UniformRandomGenerator()

    def densityFunction(self, x):
        if self.phi <= x and x < self.k * self.c + self.phi:
            return self.c - 1/self.k*(x-self.phi)
        if self.k * self.c + self.phi <= x and x < self.k * self.c * (1+self.k) + self.phi:
            return -self.c + 1/self.k*(x-self.phi)
        
    def calculateDensityFunctionForManyValues(self, numbers):
        return np.array([self.densityFunction(n) for n in numbers])

    def randomNeiman(self, N, a, b, M):
        random_values = []
        while N > 0:
            m = self.uniform.getNextAB(N, 0, M)
            r = self.uniform.getNextAB(N, a, b)
            fr = self.calculateDensityFunctionForManyValues(r)
            mask = fr >= m
            random_values.extend(r[mask])
            N -= sum(mask)
        return random_values

    def getNext(self, N):
        return self.randomNeiman(N,  self.phi, self.k * self.c * (1+self.k) + self.phi, self.k*self.c)


# Функция find_extrema_on_interval больше не нужна, так как интервалы вычисляются напрямую.