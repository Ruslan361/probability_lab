import numpy as np
from .exponential_generator import ExponentialRandomGenerator
from .exponential_generator_with_slices import ExponentialRandomGeneratorWithShift


def getExponentialRandomGeneratorFromQ(Q):
    return ExponentialRandomGenerator(1/Q)
    
def getExponentialRandomGeneratorFromR(R):
    return ExponentialRandomGenerator(1/np.sqrt(R))

def getExponentialRandomGenerator(**kwargs):
    if len(kwargs) == 1:
        if 'Q' in kwargs:
            return ExponentialRandomGenerator(1/kwargs['Q'])
        if 'R' in kwargs:
            return ExponentialRandomGenerator(1/np.sqrt(kwargs['R']))
        if 'mean' in kwargs:
            return ExponentialRandomGenerator(1/kwargs['mean'])
        if 'var' in kwargs:
            return ExponentialRandomGenerator(1/np.sqrt(kwargs['var']))
        if 'lmbd' in kwargs:
            return ExponentialRandomGenerator(kwargs['lmbd'])
        raise ValueError(f"unexpected values {kwargs}")
    if len(kwargs) == 2:
        if 'mean' in kwargs and 'var' in kwargs:
            lmbd, phi = calculateLambdaAndPhiForExponentialRandomGeneratorWithShift(kwargs['mean'], kwargs['var'])
            return ExponentialRandomGeneratorWithShift(lmbd, phi)
        if 'Q' in kwargs and 'R' in kwargs:
            lmbd, phi = calculateLambdaAndPhiForExponentialRandomGeneratorWithShift(kwargs['Q'], kwargs['R'])
            return ExponentialRandomGeneratorWithShift(lmbd, phi)
        if 'lmbd' in kwargs and 'phi' in kwargs:
            return ExponentialRandomGeneratorWithShift(kwargs['lmbd'], kwargs['phi'])
        raise ValueError(f"unexpected values {kwargs}")
    raise ValueError(f"too many values {kwargs}")
        

def calculateLambdaAndPhiForExponentialRandomGeneratorWithShift(mean, var):
    lmbd = 1/np.sqrt(var)
    phi = mean - 1/lmbd
    return lmbd, phi

from .strange_generator import TwoLinesRandomGenerator