import numpy as np
from .random_generator import RandomGenerator
from .uniform_generator import UniformRandomGenerator

#0-1/2 [(\phi*sqrt(k) - sqrt(2)*sqrt(y) - 1)/sqrt(k), (\phi*sqrt(k) + sqrt(2)*sqrt(y) - 1)/sqrt(k)]
#1/2 - 1 [(\phi*k + sqrt(k) - sqrt(2)*sqrt(k*(1 - y)))/k, (\phi*k + sqrt(k) + sqrt(2)*sqrt(k*(1 - y)))/k]

class TriangleRandomGenerator(RandomGenerator):
    def __init__(self, k, phi):
        super().__init__()
        self.k = k
        self.phi = phi
        self.uniform = UniformRandomGenerator()

    def is_in_first_interval_of_probability_density(self, x):
        return self.phi-1/np.sqrt(self.k) <= x and x <= self.phi
    
    def is_inSecond_interval_of_probability_density(self, x):
        return self.phi <= x and x <= self.phi+1/np.sqrt(self.k)
    
    def get_next_value(self, y):
        if self.is_in_first_interval_of_distribution_function(y):
            x1 = (self.phi*np.sqrt(self.k) - np.sqrt(2)*np.sqrt(y) - 1)/np.sqrt(self.k)
            x2 = (self.phi*np.sqrt(self.k) + np.sqrt(2)*np.sqrt(y) - 1)/np.sqrt(self.k)
            if self.is_in_first_interval_of_probability_density(x1) and self.is_in_first_interval_of_probability_density(x2):
                raise Exception("Не работать :( x1 и x2 принадлежать отрезку")
            if self.is_in_first_interval_of_probability_density(x1):
                return x1
            if self.is_in_first_interval_of_probability_density(x2):
                return x2
            raise Exception("something went wrong")
        if self.is_in_second_interval_of_distribution_function(y):
            x1 = (self.phi*self.k + np.sqrt(self.k) - np.sqrt(2)*np.sqrt(self.k*(1 - y)))/self.k
            x2 = (self.phi*self.k + np.sqrt(self.k) + np.sqrt(2)*np.sqrt(self.k*(1 - y)))/self.k
            if self.is_inSecond_interval_of_probability_density(x1) and self.is_inSecond_interval_of_probability_density(x2):
                raise Exception("Не работать :( x1 и x2 принадлежать отрезку")
            if self.is_inSecond_interval_of_probability_density(x1):
                return x1
            if self.is_inSecond_interval_of_probability_density(x2):
                return x2
            
    def get_variance(self):
        return 1/(6*self.k)
    def get_mean(self):
        return self.phi
    
    def is_positive(self):
        return self.phi - 1/(np.sqrt(self.k)) >= 0
            


    def is_in_first_interval_of_distribution_function(self, y):
        return 0 <= y and y <= 1/2
    
    
    def is_in_second_interval_of_distribution_function(self, y):
        return 1/2 <= y and y <= 1

    def get_next(self, N):
        y = self.uniform.get_next(N)
        x = [self.get_next_value(el) for el in y]
        return x
