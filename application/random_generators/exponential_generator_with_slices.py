import numpy as np
from .random_generator import RandomGenerator
from .uniform_generator import UniformRandomGenerator


class ExponentialRandomGeneratorWithShift(RandomGenerator):
    def __init__(self, lmbd: float, shift: float):
        super().__init__()
        # if shift < 0:
        #     raise ValueError("")
        self.lmbd = lmbd
        self.uniform = UniformRandomGenerator()
        self.shift = shift

    def get_next(self, N):
        y = self.uniform.get_next(N)
        return np.log(y)/(-self.lmbd) + self.shift
    
    def get_variance(self):
        return 1/(self.lmbd**2)
    
    def get_mean(self):
        return self.shift + 1 / self.lmbd
    
    def is_positive(self):
        return self.shift >= 0