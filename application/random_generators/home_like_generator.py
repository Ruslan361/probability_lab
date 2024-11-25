import numpy as np
from .random_generator import RandomGenerator
from .uniform_generator import UniformRandomGenerator

#0-1/2 [(\phi*sqrt(k) - sqrt(2)*sqrt(y) - 1)/sqrt(k), (\phi*sqrt(k) + sqrt(2)*sqrt(y) - 1)/sqrt(k)]
#1/2 - 1 [(\phi*k + sqrt(k) - sqrt(2)*sqrt(k*(1 - y)))/k, (\phi*k + sqrt(k) + sqrt(2)*sqrt(k*(1 - y)))/k]

class HomeLikeRandomGenerator(RandomGenerator):
    def __init__(self, k, phi):
        super().__init__()
        self.k = k
        self.phi = phi
        self.uniform = UniformRandomGenerator()

    def isInFirstIntervalOfProbabilityDensity(self, x):
        return self.phi-1/np.sqrt(self.k) <= x and x <= self.phi
    
    def isInSecondIntervalOfProbabilityDensity(self, x):
        return self.phi <= x and x <= self.phi+1/np.sqrt(self.k)
    
    def getNextValue(self, y):
        if self.isInFirstIntervalOfDistributionFunction(y):
            x1 = (self.phi*np.sqrt(self.k) - np.sqrt(2)*np.sqrt(y) - 1)/np.sqrt(self.k)
            x2 = (self.phi*np.sqrt(self.k) + np.sqrt(2)*np.sqrt(y) - 1)/np.sqrt(self.k)
            if self.isInFirstIntervalOfProbabilityDensity(x1) and self.isInFirstIntervalOfProbabilityDensity(x2):
                raise Exception("Не работать :( x1 и x2 принадлежать отрезку")
            if self.isInFirstIntervalOfProbabilityDensity(x1):
                return x1
            if self.isInFirstIntervalOfProbabilityDensity(x2):
                return x2
            raise Exception("something went wrong")
        if self.isInSecondIntervalOfDistributionFunction(y):
            x1 = (self.phi*self.k + np.sqrt(self.k) - np.sqrt(2)*np.sqrt(self.k*(1 - y)))/self.k
            x2 = (self.phi*self.k + np.sqrt(self.k) + np.sqrt(2)*np.sqrt(self.k*(1 - y)))/self.k
            if self.isInSecondIntervalOfProbabilityDensity(x1) and self.isInSecondIntervalOfProbabilityDensity(x2):
                raise Exception("Не работать :( x1 и x2 принадлежать отрезку")
            if self.isInSecondIntervalOfProbabilityDensity(x1):
                return x1
            if self.isInSecondIntervalOfProbabilityDensity(x2):
                return x2
            
    def getVar(self):
        return 1/(6*self.k)
    def getMean(self):
        return self.phi
    
    def isPositive(self):
        return self.phi - 1/(np.sqrt(self.k)) >= 0
            


    def isInFirstIntervalOfDistributionFunction(self, y):
        return 0 <= y and y <= 1/2
    
    
    def isInSecondIntervalOfDistributionFunction(self, y):
        return 1/2 <= y and y <= 1

    def getNext(self, N):
        y = self.uniform.getNext(N)
        x = [self.getNextValue(el) for el in y]
        return x
