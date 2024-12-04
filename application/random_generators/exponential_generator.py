import numpy as np
from .random_generator import RandomGenerator
from .uniform_generator import UniformRandomGenerator


class ExponentialRandomGenerator(RandomGenerator):
    def __init__(self, lmbd):
        self.lmbd= lmbd
        self.uniform = UniformRandomGenerator()
    def get_next(self, N):
            y = self.uniform.get_next(N)
            return -np.log(y)/self.lmbd
    def get_variance(self):
        return 1/(self.lmbd**2)
    def get_mean(self):
        return 1 / self.lmbd
    def is_positive(self):
        return True