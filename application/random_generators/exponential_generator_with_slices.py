import numpy as np
from .random_generator import RandomGenerator
from .uniform_generator import UniformRandomGenerator


class ExponentialRandomGeneratorWithShift(RandomGenerator):
    def __init__(self, lmbd: float, shift: float):
        super().__init__()
        self.lmbd = lmbd
        self.uniform = UniformRandomGenerator()
        self.shift = shift
    def getNext(self, N):
        y = self.uniform.getNext(N)
        return np.log(y)/(-self.lmbd) + self.shift
    def getVar(self):
        return 1/(self.lmbd**2)
    def getMean(self):
        return self.shift + 1 / self.lmbd