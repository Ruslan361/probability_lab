import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as st

def generate_cdf_plot(work_times, mean, variance):  # Renamed disp to variance
    """Generates a CDF plot (empirical and theoretical)."""
    if not work_times:
        raise ValueError("work_times cannot be empty.")

    stdev = np.sqrt(variance)
    x_min = mean - 3 * stdev
    x_max = mean + 3 * stdev

    x = np.linspace(x_min, x_max, 1000)
    theoretical_cdf = st.norm.cdf(x, mean, stdev)

    # Keep original logic but make it more concise
    work_times_sorted = np.sort(np.concatenate(([x_min], work_times, [x_max])))
    empirical_cdf = np.hstack((np.arange(len(work_times) + 1), 0)) / len(work_times)
    empirical_cdf[-1] = 1

    plt.figure()
    plt.plot(x, theoretical_cdf, label=r"$F_\eta(x)$") # Theoretical
    plt.step(work_times_sorted, empirical_cdf, where='post',label=r"$\hat{F_\eta(x)}$")  # Empirical

    work_times_sorted = np.sort(work_times)
    n = len(work_times)
    empirical_cdf = np.arange(1, n + 1) / n  # Empirical CDF values at jump points

    # Calculate theoretical CDF *only* at the data points (jump points)
    theoretical_cdf_values = st.norm.cdf(work_times_sorted, mean, stdev)

    # Calculate differences *only* at the jump points
    differences = np.abs(empirical_cdf - theoretical_cdf_values)

    # Also check the difference at the point *just before* each jump
    differences_before_jump = np.abs(np.arange(n) / n - theoretical_cdf_values)
    ks_statistic = np.max(np.concatenate([differences, differences_before_jump]))
    plt.xlabel('$t$')
    plt.ylabel('CDF') # Add y-axis label
    plt.title(r'$\hat{F_\eta(x)}$ and $F_\eta(x)$ (D = ' + f"{ks_statistic:.4f})") # D-statistic in title
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='svg')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url