import sympy as sp
import numpy as np
from .random_generator import RandomGenerator
from .uniform_generator import UniformRandomGenerator

class TwoLinesRandomGenerator(RandomGenerator):
    def __init__(self, k_val, phi_val):
        x, k, phi = sp.symbols(r'x k \phi')
        c = sp.sqrt(2/(k*(1+k**2)))
        self.uniform = UniformRandomGenerator()
        c_val = c.subs(k, k_val)
        subintegral_function_1 = c - 1/k*(x-phi)
        subintegral_function_2 = -c + 1/k*(x-phi)
        # self.distribution_function_1 = sp.integrate(subintegral_function_1, (x, phi, x))
        # self.distribution_function_2 = sp.integrate(subintegral_function_2, (x, phi + k*c, x))
        self.distribution_function_1 = k**3*c**4/(2*(k*c-x))
        self.distribution_function_2 = 1/2*k*c**2 + k**5*c**3/x
        self.distribution_function_1 = self.distribution_function_1.subs(k, k_val).subs(phi, phi_val)
        self.distribution_function_2 = self.distribution_function_2.subs(k, k_val).subs(phi, phi_val)

        y =  sp.symbols('y')
        self.inverse_function_1 = sp.solve(self.distribution_function_1 - y, x)
        self.vectorized_function_1 = sp.lambdify([y], self.inverse_function_1, 'numpy')
        self.inverse_function_2 = sp.solve(self.distribution_function_2 - y, x)
        self.vectorized_function_2 = sp.lambdify([y], self.inverse_function_2, 'numpy')

        # Получаем интервалы
        self.interval_1 = find_extrema_on_interval(self.distribution_function_1, x, (phi_val, k_val*c_val+phi_val))
        self.interval_1 = (self.interval_1['min'][1], self.interval_1['max'][1])
        self.interval_2 = find_extrema_on_interval(self.distribution_function_2, x, (k_val*c_val+phi_val, phi_val + k_val*c_val*(1+k_val)))
        self.interval_2 = (self.interval_2['min'][1], self.interval_2['max'][1])

        # Проверяем корректность интервалов
        if (self.interval_1[0] < self.interval_2[0] and self.interval_2[0] < self.interval_1[1]):
            raise ValueError("unexpected distribution function")
        if (self.interval_2[0] < self.interval_1[0] and self.interval_1[0] < self.interval_2[1]):
            raise ValueError("unexpected distribution function")
        
    def getNext(self, N):
        y = self.uniform.getNext(N)
        
        # Первый интервал
        first_interval = np.logical_and(y <= self.interval_1[1], y >= self.interval_1[0])
        random_values = y[first_interval]
        if random_values.shape[0] > 0:
            random_values = self.vectorized_function_1(random_values)

        # Второй интервал
        second_interval = np.logical_and(y <= self.interval_2[1], y >= self.interval_2[0])
        random_values_2 = y[second_interval]
        if random_values_2.shape[0] > 0:
            random_values_2 = self.vectorized_function_2(random_values_2)

        # Возвращаем результат
        if random_values_2 and random_values:
            return np.concatenate([random_values, random_values_2])
        
        if random_values_2:
            return random_values_2
        
        if random_values:
            return random_values
        raise Exception("Empty random")


def find_extrema_on_interval(f, var, interval):
    """
    Находит максимум и минимум функции f на заданном отрезке.

    :param f: Символьное выражение функции.
    :param var: Переменная функции.
    :param interval: Кортеж (a, b), определяющий отрезок [a, b].
    :return: Словарь с минимумом и максимумом на отрезке.
    """
    a, b = interval
    interval_set = sp.Interval(a, b)
    
    # Находим первую производную
    f_prime = sp.diff(f, var)
    
    # Находим критические точки на интервале, решая f'(x) = 0
    critical_points = sp.solve(f_prime, var)
    
    # Отбираем только те критические точки, которые лежат на интервале [a, b]
    critical_points = [p for p in critical_points if interval_set.contains(p)]
    
    # Составляем список точек для проверки (концы отрезка и критические точки)
    points_to_check = [a, b]
    points_to_check.extend(critical_points)
    
    # Вычисляем значения функции в каждой из этих точек
    values = []
    for point in points_to_check:
        value = f.subs(var, point)
        values.append((point, value))
    
    # Определяем максимум и минимум символически, если не удалось вычислить численно
    min_value = 0
    max_value = 1
    min_point = max_point = None

    for point, value in values:
        # Пытаемся определить значение численно
        # try:
        #     numeric_value = sp.N(value)
        #     if numeric_value < min_value:
        #         min_value, min_point = numeric_value, point
        #     if numeric_value > max_value:
        #         max_value, max_point = numeric_value, point
        # except TypeError:
        if value.is_real:
            # Если не удается, работаем с символьными значениями
            if value < min_value:
                min_value, min_point = value, point
            if value > max_value:
                max_value, max_point = value, point

    return {
        "min": (min_point, min_value),
        "max": (max_point, max_value)
    }


