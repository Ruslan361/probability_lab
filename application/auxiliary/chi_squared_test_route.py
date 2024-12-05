from flask import jsonify, request
import numpy as np
import scipy.stats as st
from .compute_histogram import compute_histogram
import logging
logger = logging.getLogger(__name__)
def calculate_chi2_statistic(observed_frequencies, expected_frequencies):
    """Calculates the chi-squared statistic."""
    if len(observed_frequencies) != len(expected_frequencies):
        raise ValueError("Observed and expected frequencies must have the same length.")
    # Check for non-positive expected frequencies, adding a small value to avoid division by zero
    
    expected_frequencies = np.where(expected_frequencies <= 0, 1e-9, expected_frequencies)  # Correct handling of zero expected frequencies
    return np.sum((observed_frequencies - expected_frequencies)**2 / expected_frequencies)


def chi_squared_test_route():
    """Performs a chi-squared test and returns the results."""
    try:
        data = request.get_json()
        logger.info("Start chi squared test")

        try:
            num_intervals = int(data["intervals"])
            work_times = [float(t) for t in data["workTimes"]]
            mean = float(data["mean"])
            variance = float(data["disp"]) # Use variance consistently
            alpha = float(data["a"])

            if num_intervals <= 0:
                raise ValueError("Number of intervals must be positive.")
            if not work_times:
                raise ValueError("workTimes cannot be empty.")
            if not 0 < alpha < 1:
                raise ValueError("alpha must be between 0 and 1.")

        except (KeyError, TypeError, ValueError) as e:
            return jsonify({"error": f"Invalid input data: {e}"}), 400

        expected_probabilities, chi2_statistic, p_value, message = chi_squared_test(num_intervals, work_times, mean, variance, alpha) # Fixed name here
        logger.info("Chi squared return result")
        return jsonify({
            "q": expected_probabilities.tolist(),  # Use correct name in response
            "R0": chi2_statistic,
            "F": p_value,
            "message": message
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Consider logging the exception for debugging

def calculate_expected_probabilities(intervals, mean, variance):
    """Calculates the expected probabilities for each interval based on the normal distribution."""
    probabilities = []
    for i in range(len(intervals) - 1):
        probabilities.append(st.norm.cdf(intervals[i+1], mean, np.sqrt(variance)) - st.norm.cdf(intervals[i], mean, np.sqrt(variance)))
    return np.array(probabilities)

def chi_squared_test(num_intervals, work_times, mean, variance, alpha):
    """Performs the chi-squared goodness-of-fit test."""
    n = len(work_times)
    stdev = np.sqrt(variance)
    ppf = np.linspace(0, 1, num_intervals + 1)
    intervals = st.norm.ppf(ppf, mean, stdev)

    hist_values, _ = np.histogram(work_times, bins=intervals) # Use numpy's histogram function

    expected_probabilities = calculate_expected_probabilities(intervals, mean, variance)
    expected_frequencies = expected_probabilities * n

    chi2_statistic = np.sum((hist_values - expected_frequencies)**2 / expected_frequencies)
    degrees_of_freedom = num_intervals -1 # k - p - 1
    p_value = 1 - st.chi2.cdf(chi2_statistic, degrees_of_freedom)

    if p_value <= alpha:
        message = "Гипотеза отвергается"  # Reject the null hypothesis
    else:
        message = "Гипотеза не отвергается"  # Fail to reject the null hypothesis

    # print(f"Chi-squared statistic: {chi2_statistic}")
    # print(f"P-value: {p_value}")
    # print(f"Significance level: {alpha}")
    # print(message)

    return expected_probabilities, chi2_statistic, p_value, message