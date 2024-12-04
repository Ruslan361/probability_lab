from flask import jsonify, request
import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Устанавливаем Agg backend *ПЕРЕД* импортом pyplot
import matplotlib.pyplot as plt
import scipy.stats as st
from .compute_histogram import compute_histogram_with_intervals_manual

def calculateQ(intervals, mean, disp):
    Q = np.zeros(len(intervals)-1)
    sigma = np.sqrt(disp)
    
    for i in range(1, len(intervals)):
        
        Q[i-1] = st.norm.cdf(intervals[i], mean, sigma) - st.norm.cdf(intervals[i-1], mean, sigma)
    
    return Q

def intervals_2():
    try:
        # Получаем данные
        data = request.get_json()
        num_intervals = data.get("intervals")
        # intervals = sorted(intervals)
        work_times = data.get("workTimes")
        mean = float(data.get("mean"))
        disp = float(data.get("disp"))
        a = float(data.get("a"))
        sigma = np.sqrt(disp)
        #x_min, x_max = mean - 3*sigma, mean + 3*sigma

        #ppf = np.linspace(0, 1, )
        # Преобразуем строку JSON в объекты Python
        # if num_intervals == 1:
        #     ppf = np.array([0.5])
        # else:
        ppf = np.linspace(0, 1, num_intervals + 2)
        #ppf = np.hstack([-np.inf, ppf, np.inf])
        #intervals = np.array([st.norm.ppf(el, mean, sigma) for el in ppf])
        intervals = st.norm.ppf(ppf, mean, sigma)
        #intervals = np.hstack([-np.inf, intervals, np.inf])
        print(intervals)
        work_times = np.array(work_times)


        hist_values, bin_centers = compute_histogram_with_intervals_manual(work_times, intervals)
        k = len(bin_centers)
        q = calculateQ(intervals, mean, disp)
        print(q)
        n = np.sum(hist_values)
        R0 = np.sum((hist_values - n * q) ** 2 / n / q)
        F = 1 - st.chi2.cdf(R0, k)
        if F <= a:
            message = "Гипотеза не отвергается"
        else:
            message = "Гипотеза отвергается"
        # Возвращаем данные
        return jsonify({
            "q": q.tolist(),
            "R0": R0,
            "F": F,
            "message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500