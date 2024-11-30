from flask import jsonify, request
import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Устанавливаем Agg backend *ПЕРЕД* импортом pyplot
import matplotlib.pyplot as plt
import scipy.stats as st
from .compute_histogram import compute_histogram_with_intervals_manual

#@app.route('/interval', methods=['POST'])
def intervals():
    try:
        # Получаем данные
        intervals = request.form.get("intervals")
        work_times = request.form.get("workTimes")
        mean = float(request.form.get("mean"))
        disp = float(request.form.get("disp"))
        print(disp)

        # Преобразуем строку JSON в объекты Python
        intervals = np.array(eval(intervals))
        work_times = np.array(eval(work_times))

        if len(intervals) < 2:
            raise ValueError("Интервалы должны содержать хотя бы два значения.")

        hist_values, bin_centers = compute_histogram_with_intervals_manual(work_times, intervals, density=True)
        pdf_real = st.norm.pdf(bin_centers, mean, np.sqrt(disp))
        #print(pdf_real)
        max_sub = np.max(np.abs(pdf_real - hist_values))
        # Вычисление гистограммы
        #hist_values, _ = np.histogram(work_times, bins=intervals)
        #bin_centers = [(intervals[i] + intervals[i + 1]) / 2 for i in range(len(intervals) - 1)]
        plt.figure()
        #plt.hist(workTimes, density=density, cumulative=cumulative, bins=bins, alpha=0.7, label='Время работы')

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