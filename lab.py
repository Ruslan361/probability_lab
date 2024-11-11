import numpy as np
import matplotlib.pyplot as plt
from random_generators import getExponentialRandomGenerator
from random_generators import TwoLinesRandomGenerator
from device import Device

N = 10
amountOfSubdevices = 1
randomGenerator = getExponentialRandomGenerator(mean=2, var=1)
device = Device(amountOfSubdevices, randomGenerator)

times = [device.calculateWorkTime() for i in range(N)]

#print(times)
sorted(times)
print(times)

# Функция для проверки генератора
def test_two_lines_random_generator():
    # Параметры для генератора
    k_val = 1/2  # Пример значения k
    phi_val = 0  # Пример значения phi

    # Создаем объект генератора
    generator = TwoLinesRandomGenerator(k_val, phi_val)

    # Проверяем интервалы, на которых генерируются случайные значения
    # print("Interval 1:", (generator.interval_1[0], generator.interval_1[1]))
    # print("Interval 2:", (generator.interval_2[0], generator.interval_2[1]))

    # Генерация случайных чисел
    N = 100000  # Количество случайных чисел для генерации
    random_values = generator.getNext(N)

    # Выводим первые 10 случайных значений
    print("First 10 random values:")
    print(random_values[:10])
    plt.hist(random_values, density=True)
    plt.show()



# Пример использования
if __name__ == "__main__":
    test_two_lines_random_generator()