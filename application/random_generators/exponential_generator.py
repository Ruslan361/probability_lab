import numpy as np
from .random_generator import RandomGenerator
from .uniform_generator import UniformRandomGenerator


class ExponentialRandomGenerator(RandomGenerator):
        def __init__(self, lmbd):
            self.lmbd= lmbd
            self.uniform = UniformRandomGenerator()
        def getNext(self, N):
             y = self.uniform.getNext(N)
             return -np.log(y)/self.lmbd