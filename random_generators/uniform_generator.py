import numpy as np
from .random_generator import RandomGenerator


class UniformRandomGenerator(RandomGenerator):
    def __init__(self, a = 0, b=1):
        self.a=a
        self.b=b
    def getNext(self, N):
        return np.random.uniform(self.a, self.b, N)