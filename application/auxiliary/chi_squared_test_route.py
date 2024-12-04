from flask import jsonify, request
import numpy as np
import scipy.stats as st
from .compute_histogram import compute_histogram  # Assuming improved and renamed

def calculate_expected_frequencies(intervals, mean, variance, total_count):
    """Calculates expected frequencies for each interval based on the normal distribution."""
    sigma = np.sqrt(variance)
    expected_frequencies = []
    for i in range(len(intervals) - 1):
        prob = st.norm.cdf(intervals[i+1], mean, sigma) - st.norm.cdf(intervals[i], mean, sigma)
        expected_frequencies.append(prob * total_count)
    return np.array(expected_frequencies)

def calculate_chi2_statistic(observed_frequencies, expected_frequencies):
    """Calculates the chi-squared statistic."""
    if len(observed_frequencies) != len(expected_frequencies):
        raise ValueError("Observed and expected frequencies must have the same length.")
    if np.any(expected_frequencies <= 0):  # Check for zero or negative expected frequencies
        raise ValueError("Expected frequencies must be positive.")

    return np.sum((observed_frequencies - expected_frequencies)**2 / expected_frequencies)


def chi_squared_test_route():
    """Performs a chi-squared test and returns the results."""
    try:
        data = request.get_json()
        
        # Data validation and type conversion
        try:
            num_intervals = int(data["intervals"])
            work_times = [float(t) for t in data["workTimes"]]
            mean = float(data["mean"])
            variance = float(data["disp"])
            alpha = float(data["a"])  # Use alpha instead of 'a'

            if num_intervals <= 0:
                raise ValueError("Number of intervals must be positive.")
            if not work_times:
                raise ValueError("workTimes cannot be empty.")
            if not 0 < alpha < 1:
                raise ValueError("alpha must be between 0 and 1.")


        except (KeyError, TypeError, ValueError) as e:
            return jsonify({"error": f"Invalid input data: {e}"}), 400 # Bad Request


        expected_frequencies, chi2_statistic, p_value, message = chi_squared_test(num_intervals, work_times, mean, variance, alpha)
        print(message)
        #message = "Гипотеза отклонена" if hypothesis_rejected else "Гипотеза не отклонена"
        return jsonify({
            "q": expected_frequencies.tolist(),  # Renamed and to list
            "R0": chi2_statistic,       # Renamed
            "F": p_value,                  # Added p-value
            "message": message
        }), 200  # OK


    except Exception as e:
        return jsonify({"error": str(e)}), 500 

def chi_squared_test(num_intervals, work_times, mean, variance, alpha):
    stdev = np.sqrt(variance)
    ppf = np.linspace(0, 1, num_intervals + 1)
    intervals = st.norm.ppf(ppf, mean, stdev)  # Use ppf to define intervals

    hist_values, _ = compute_histogram(work_times, intervals)
    k = len(hist_values)  # Degrees of freedom
        
    expected_frequencies = calculate_expected_frequencies(intervals, mean, variance, np.sum(hist_values))
    print(expected_frequencies)
    print(hist_values)
    chi2_statistic = np.sum((hist_values - expected_frequencies)**2 / expected_frequencies)
    p_value = 1 - st.chi2.cdf(chi2_statistic, k - 1) # k-1 degrees of freedom
    print(chi2_statistic)
    hypothesis_rejected = p_value <= alpha
    print(hypothesis_rejected)
    if hypothesis_rejected:
        message = "Гипотеза отклонена"
    else:
        message = "Гипотеза не отклонена"
    return expected_frequencies,chi2_statistic,p_value,message # Internal Server Error, consider logging exception