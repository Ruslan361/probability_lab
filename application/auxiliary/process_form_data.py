from flask import request

def process_form_data():
    """Processes form data from a POST request and returns validated parameters."""
    if request.method != "POST":
        raise ValueError("Invalid request method. Expected POST.") # Or return None, depending on how you want to handle non-POST requests


    try:
        data = request.get_json()

        # Validate and convert data types, raise specific exceptions for better error handling
        try:
            q = float(data["q"])
            r = float(data["r"])
            n = int(data["n"])
            num_trials = int(data["num_trials"])
            distribution_type = data["distributing_function"]  # More descriptive name

            if n <= 0:
                raise ValueError("n (number of devices) must be positive.")
            if num_trials <= 0:
                raise ValueError("num_trials must be positive.")
            if r < 0:
                raise ValueError("r (variance or scale) cannot be negative.") # Depending on distribution


        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid input data: {str(e)}") from e # Chain exceptions, more informative error messages



        return q, r, n, num_trials, distribution_type


    except ValueError as e:
        raise  # Re-raise the ValueError for the calling function to handle