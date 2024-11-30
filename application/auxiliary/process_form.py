from flask import request
import numpy as np

def process_form():
    q = None
    r = None
    n = None
    num_trials = None
    distributing_function = None
    table = None
    error_message = None
    if request.method == "POST":
        try:
            q = float(request.form.get("q"))
            r = float(request.form.get("r"))
            n = int(request.form.get("n"))
            num_trials = int(request.form.get("num_trials"))
            distributing_function = request.form.get("distributing_function")
            
            #
            results = []
            for _ in range(num_trials):
                trial_data = []
                for _ in range(n):
                    measurement = np.random.normal(loc=q, scale=np.sqrt(r))
                    trial_data.append(measurement)
                results.append(trial_data)


        except ValueError:
            raise ValueError("Ошибка: Введите корректные числовые значения.")
        if q is None and r is None and n is None and num_trials is None and distributing_function is None:
            raise ValueError("Ошибка: Введите корректные числовые значения.")
    return q,r,n,num_trials,distributing_function