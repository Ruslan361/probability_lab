import numpy as np
from .random_generator import RandomGenerator


class UniformRandomGenerator(RandomGenerator):
    def __init__(self, a = 0, b=1):
        self.a=a
        self.b=b
    def get_next(self, N):
        return np.random.uniform(0, 1, N) * (self.b - self.a) + self.a
    def getNextAB(self, N, a, b):
        return np.random.uniform(0, 1, N) * (b - a) + a
    def get_variance(self):
        return (self.b - self.a)**2 / 12
    def get_mean(self):
        return (self.b + self.a) / 2
    def is_positive(self):
        return self.a >= 0