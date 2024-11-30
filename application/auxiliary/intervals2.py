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
        intervals = request.form.get("intervals")
        # intervals = sorted(intervals)
        work_times = request.form.get("workTimes")
        mean = float(request.form.get("mean"))
        disp = float(request.form.get("disp"))
        a = float(request.form.get("a"))
        

        # Преобразуем строку JSON в объекты Python
        intervals = np.array(eval(intervals))
        intervals = np.hstack([-np.inf, intervals, np.inf])
        work_times = np.array(eval(work_times))

        if len(intervals) < 1:
            raise ValueError("Интервалы должны содержать хотя бы одно значение.")

        hist_values, bin_centers = compute_histogram_with_intervals_manual(work_times, intervals)
        k = len(bin_centers)
        q = calculateQ(intervals, mean, disp)
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