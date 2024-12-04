from flask import jsonify, request
import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import scipy.stats as st
from .compute_histogram import compute_histogram_with_intervals_manual


def intervals():
    try:
        # Получаем данные
        data = request.get_json()

        num_intervals = data.get("intervals")
        work_times = data.get("workTimes")
        mean = float(data.get("mean"))
        disp = float(data.get("disp"))
        sigma = np.sqrt(disp)
        x_min, x_max = mean-3*sigma, mean+3*sigma
        intervals = np.linspace(x_min, x_max, num_intervals + 1)


        hist_values, bin_centers = compute_histogram_with_intervals_manual(work_times, intervals, density=True)
        pdf_real = st.norm.pdf(bin_centers, mean, np.sqrt(disp))

        max_sub = np.max(np.abs(pdf_real - hist_values))
        plt.figure()
        plt.xlabel('$t$')
        #plt.ylabel('Относительная частота')
        plt.title('Гистограмма относительных частот')
        #plt.legend()
        plt.bar(bin_centers, hist_values, width=np.diff(intervals), align='center', alpha=0.7, edgecolor='black')
        img = io.BytesIO()
        plt.savefig(img, format='svg')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        # Возвращаем данные
        return jsonify({
            "pdf_select": hist_values.tolist(),
            "pdf_real": pdf_real.tolist(),
            "bin_centers": list(bin_centers),
            "max_sub": max_sub,
            "graph_url":  plot_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500