import numpy as np

class Device:
    def __init__(self, N, randomGenerator):
        self.randomGenerator = randomGenerator
        self.amountOfSubdevices = N
    def calculateWorkTime(self):
        return np.sum(self.randomGenerator.getNext(self.amountOfSubdevices))