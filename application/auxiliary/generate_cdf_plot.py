import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Устанавливаем Agg backend *ПЕРЕД* импортом pyplot
import matplotlib.pyplot as plt
import scipy.stats as st
from .compute_histogram import compute_histogram_with_intervals_manual


def generate_cdf_plot(workTimes, mean, disp, bin_edges):
    if np.size(workTimes) == 0:
        raise ValueError("Empty or invalid workTimes.")
    
    sigma = np.sqrt(disp)
    x_min = mean - 3 * sigma
    x_max = mean + 3 * sigma
    
    x = np.linspace(x_min, x_max, 1000)
    cdf = st.norm.cdf(x, mean, np.sqrt(disp))
    
    print(bin_edges)
    print(workTimes)
    
    plt.figure()

    plt.plot(x, cdf, label=r"$F_\eta(x)$")

    print(type(workTimes))
    print(len(workTimes))
    workTimes_sorted = list(workTimes)
    workTimes_sorted.insert(0, x_min)
    workTimes_sorted.insert(-1, x_max)
    workTimes_sorted = np.sort(workTimes_sorted)
    
    cdf_ = [i for i in range(len(workTimes) + 1)]
    cdf_.append(0)
    #print(100000)
    cdf_ = np.array(cdf_)
    cdf_ = cdf_ / len(workTimes)
    cdf_[-1]  = 1
    print(cdf_.shape)
    print(workTimes_sorted.shape)

    # Рисуем график
    plt.step(workTimes_sorted, cdf_, where='post')
    print("draw")
    Fn = st.norm.cdf(workTimes_sorted, mean, sigma)
    D = np.max(np.abs(cdf_ - Fn))
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