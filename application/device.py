import numpy as np

class Device:
    def __init__(self, N, randomGenerator):
        self.randomGenerator = randomGenerator
        self.amountOfSubdevices = N
    def calculate_work_time(self):
        return np.sum(self.randomGenerator.get_next(self.amountOfSubdevices))