from flask import jsonify, request
from .generate_cdf_plot import generate_cdf_plot
import logging

logger = logging.getLogger(__name__)

def generate_cdf_plot_route():
    """Handles the route for generating a CDF plot."""
    try:
        data = request.get_json()

        # Explicitly convert to correct types and handle potential errors
        try:
            work_times = [float(t) for t in data.get("workTimes", [])]  # Enforce numeric
            mean = float(data["mean"])
            variance = float(data["disp"])  # Use more descriptive name 
        except (KeyError, TypeError, ValueError) as e:
            return jsonify({"error": f"Invalid input data: {e}"}), 400  # Bad Request

        if not work_times:
            return jsonify({"error": "workTimes cannot be empty."}), 400

        plot_url = generate_cdf_plot(work_times, mean, variance)
        logger.info("CDF plot generated successfully.")
        return jsonify({"plot_url": plot_url}), 200  # OK - No need to send an empty "error"

    except Exception as e:  # Catch any other unexpected errors
        logger.exception("Error generating CDF plot") # Log the full traceback for debugging
        return jsonify({"error": "An unexpected error occurred."}), 500  # Internal Server Error