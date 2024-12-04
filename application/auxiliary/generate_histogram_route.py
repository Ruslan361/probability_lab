from flask import jsonify, request
import numpy as np
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as st
from .compute_histogram import compute_histogram

# Assuming compute_histogram is now improved and renamed.

def generate_histogram_route():  # More descriptive function name
    """Generates a histogram and returns data and plot URL."""

    try:
        data = request.get_json()

        # Data validation and type conversion
        try:
            num_intervals = int(data["intervals"])
            work_times = [float(t) for t in data["workTimes"]]  # Ensure numeric
            mean = float(data["mean"])
            variance = float(data["disp"])  # More descriptive name

            if num_intervals <= 0:
                raise ValueError("Number of intervals must be positive.")
            if not work_times:
                raise ValueError("workTimes cannot be empty.")

        except (KeyError, TypeError, ValueError) as e:
            return jsonify({"error": f"Invalid input data: {e}"}), 400 # Bad Request

        stdev = np.sqrt(variance)
        x_min = mean - 3 * stdev
        x_max = mean + 3 * stdev
        bin_edges = np.linspace(x_min, x_max, num_intervals + 1)


        hist_values, bin_centers = compute_histogram(work_times, bin_edges, density=True)
        theoretical_pdf = st.norm.pdf(bin_centers, mean, stdev)


        max_difference = np.max(np.abs(theoretical_pdf - hist_values))

        # Generate plot
        plt.figure()
        plt.xlabel('t')
        plt.ylabel('Density')  # Added y-axis label
        plt.title('Histogram of Relative Frequencies')
        plt.bar(bin_centers, hist_values, width=np.diff(bin_edges), align='center', alpha=0.7, edgecolor='black')


        img = io.BytesIO()
        plt.savefig(img, format='svg')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return jsonify({
            "empirical_pdf": hist_values.tolist(),  # More descriptive key name
            "theoretical_pdf": theoretical_pdf.tolist(),  # More descriptive key name
            "bin_centers": list(bin_centers),
            "max_difference": max_difference,  # More descriptive key name
            "graph_url": plot_url
        }), 200 # OK

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error, consider logging the exception