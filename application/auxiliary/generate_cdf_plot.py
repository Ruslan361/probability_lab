import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Устанавливаем Agg backend *ПЕРЕД* импортом pyplot
import matplotlib.pyplot as plt
import scipy.stats as st
from .compute_histogram import compute_histogram_with_intervals_manual


def generate_cdf_plot(workTimes, mean, disp, bin_edges):
    """
    Генерирует гистограмму относительных частот для списка workTimes и возвращает ее как base64 закодированное SVG изображение.

    Args:
        workTimes: массив числовых значений.

    Returns:
        Строку base64, представляющую SVG изображение гистограммы, или None, если workTimes пуст или невалиден.
    """
    workTimes = np.array(workTimes)
    if np.size(workTimes) == 0:
        raise ValueError("Empty or invalid workTimes.")
    x_min = np.min(workTimes)
    x_max = np.max(workTimes)
    
    x = np.linspace(x_min, x_max, 1000)
    cdf = st.norm.cdf(x, mean, np.sqrt(disp))
    #
    if (bin_edges == 'auto'):
        count = int((np.log(workTimes.shape[0]))) + 1
        #count = max(count, 1)
        if workTimes.shape[0] > 100:
            count = 100
        count = max(count, 1)
        #count = 100
        #
        bin_edges = np.linspace(x_min, x_max, count + 1)
        
    #
    print(bin_edges)
    print(workTimes)
    hist_values, bin_centers = compute_histogram_with_intervals_manual(workTimes, bin_edges, density=True, cumulative=True)
    print(hist_values, bin_centers)
    #
    plt.figure()
    #plt.hist(workTimes, density=density, cumulative=cumulative, bins=bins, alpha=0.7, label='Время работы')
    plt.plot(x, cdf, label=r"$F_\eta(x)$")
    if (len(bin_edges) < 10):
        plt.plot(bin_centers, hist_values, "-o", label=r"$\hat{F_\eta(x)}$")
    else:
        plt.plot(bin_centers, hist_values, label=r"$\hat{F_\eta(x)}$")
    Fn = st.norm.cdf(bin_centers, mean, np.sqrt(disp))
    D = np.max(np.abs(hist_values - Fn))
    plt.xlabel('$t$')
    #plt.ylabel('Относительная частота')
    plt.title('График $\hat{F_\eta(x)}$ и $F_\eta(x)$ ' + f"D = {D}")
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='svg')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url