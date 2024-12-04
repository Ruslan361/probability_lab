from flask import jsonify, request
import numpy as np
from random_generators import get_exponential_generator, get_home_like_generator  # Assuming updated names
from device import Device
from .process_form_data import process_form_data
import logging

logger = logging.getLogger(__name__)

def generate_work_times(n, num_trials, random_generator):
    """Generates a sorted list of device work times."""
    device = Device(n, random_generator)
    return sorted([float(device.calculate_work_time()) for _ in range(num_trials)])


def get_random_generator(distribution_type, q, r):
    """Returns a random number generator based on distribution type."""
    if distribution_type == 'exponential':
        return get_exponential_generator(Q=q, R=r)  # Consistent naming
    if distribution_type == 'home-like':
        return get_home_like_generator(Q=q, R=r)  # Consistent naming
    raise ValueError("Invalid distribution type")


def calculate_median(data):
    """Calculates the median of a dataset."""
    n = len(data)
    return (data[n // 2 - 1] + data[n // 2]) / 2 if n % 2 == 0 else data[n // 2]



def submit_data():
    """Handles the submission of form data and returns calculated characteristics."""
    try:
        q, r, n, num_trials, distribution_type = process_form_data()
        logger.info("process form...")
        random_generator = get_random_generator(distribution_type, q, r)
        
        is_positive = random_generator.is_positive() # Use snake_case
        
        logger.info("Generating work times...")
        work_times = generate_work_times(n, num_trials, random_generator)
        logger.info("Work times generated.")
        
        warning = "Negative values possible" if not is_positive else ""  # Simplified

        # Calculations using NumPy for efficiency
        mean = np.mean(work_times)
        variance_sample = np.var(work_times)
        median = calculate_median(work_times)
        range_ = np.ptp(work_times)  # Use np.ptp for range
        
        expected_mean = n * random_generator.get_mean() # Renamed for clarity
        variance_theoretical = n * random_generator.get_variance()


        characteristics_labels = [
            r"E_\eta", r"\bar{x}", r"\left| E_\eta - \bar{x} \right|",
            r"D\eta", r"S^2", r"\left| D_\eta - S^2 \right|",
            r"\hat{Me}", r"\hat{R}"
        ]
        characteristics = [
            expected_mean, mean, abs(expected_mean - mean),
            variance_theoretical, variance_sample, abs(variance_theoretical - variance_sample),
            median, range_
        ]

        return jsonify({
            "workTimes": work_times,
            "warning": warning,
            "labels": characteristics_labels,
            "characteristics": characteristics
        }), 200  # OK - No need for explicit "error" key when no error

    except ValueError as e:  # Handle invalid input
        return jsonify({"error": str(e), "workTimes": [], "warning": "", "labels": [], "characteristics": []}), 400  # Bad Request

    except Exception as e:  # Handle other unexpected errors
        logger.exception("Error during data submission")  # Log the exception with traceback
        return jsonify({"error": "An unexpected error occurred.", "workTimes": [], "warning": "", "labels": [], "characteristics": [] }), 500  # Internal Server Error