from flask import jsonify, request
import numpy as np
from random_generators import getExponentialRandomGenerator, getHomeLikeGenerator
from device import Device
from .process_form import process_form
from concurrent.futures import ThreadPoolExecutor

import logging
logger = logging.getLogger(__name__)

def get_work_time_series(n, num_trials, random_generator):
    device = Device(n, random_generator)
    workTimes = [float(device.calculateWorkTime()) for i in range(num_trials)]
    workTimes = sorted(workTimes)
    return workTimes


def get_random_generator_by_name(q, r, distributing_function):

    if distributing_function == 'exponential':
        return getExponentialRandomGenerator(Q=q, R=r)
    if distributing_function == 'home-like':
        return getHomeLikeGenerator(Q=q, R=r)
    raise ValueError("Неправильный тип генератора")

def get_Me(workTimes):
    length = len(workTimes)
    if length % 2 == 0:
        return (workTimes[length//2 - 1] + workTimes[length//2]) / 2
    else:
        return (workTimes[(length)//2])


def submit():
    #try:
        
        q, r, n, num_trials, distributing_function = process_form()
        random_generator = get_random_generator_by_name(q, r, distributing_function)

        
        isPositive = random_generator.isPositive()
        logger.info("Начало генерации случайных чисел")
        workTimes = get_work_time_series(n, num_trials, random_generator)
        logger.info("Конец генерации случайных чисел")
        
        
        warning = ""
        if not isPositive:
            warning = "Могут быть отрицательные значения"

        
        E = n * random_generator.getMean()
        mean = np.sum(workTimes) / num_trials
        D = n * random_generator.getVar()
        squared_S = np.sum((np.array(workTimes) - mean) ** 2) / num_trials
        Me = get_Me(workTimes)

        
        sorted_workTimes = sorted(workTimes)
        length = len(sorted_workTimes)
        R = 0 if length <= 1 else sorted_workTimes[-1] - sorted_workTimes[0]

        
        characteristics_labels = [
            r"E_\eta", r"\bar{x}", r"\left| E_\eta - \bar{x} \right|", 
            r"D\eta", r"S^2", r"\left| D_\eta - S^2 \right|", 
            r"\hat{Me}", r"\hat{R}"
        ]
        characteristics = [
            E, mean, abs(E - mean), D, squared_S, 
            abs(D - squared_S), Me, R
        ]

        
        message = {
            "workTimes": workTimes,
            "warning": warning,
            "error": "",
            "labels": characteristics_labels,
            "characteristics": characteristics
        }
        
        return jsonify(message), 200

    #except ValueError as e:
        
        message = {
            "workTimes": [],
            "warning": "",
            "error": str(e),
            "labels": [],
            "characteristics": []
        }
        return jsonify(message), 400

    #except Exception as e:
        
        message = {
            "workTimes": [],
            "warning": "",
            "error": str(e),
            "labels": [],
            "characteristics": []
        }
        return jsonify(message), 500