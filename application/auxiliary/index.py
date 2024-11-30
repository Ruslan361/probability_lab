from flask import render_template


#@app.route("/", methods=["GET", "POST"])
def index():
    # #q, r, n, num_trials, distributing_function = None, None, None, None, None
    # isPositive = None
    # try:
    #     q, r, n, num_trials, distributing_function= process_form()
        
    #     random_generator = get_random_generator_by_name(q, r, distributing_function)
    #     isPositive = random_generator.isPositive()
    #     workTimes = get_work_time_series(n, num_trials, random_generator)
    #     plot_url = generate_histogram(workTimes)
    #     characteristics_labels = [r"E_\eta", r"\bar{x}", r"\left| E_\eta - \bar{x} \right|" , r"D\eta", r"S^2", r"\left| D_\eta - S^2 \right|", r"\hat{Me}", r"\hat{R}"]

    #     E = n * random_generator.getMean()
    #     mean = np.sum(workTimes) / num_trials
    #     D = n * random_generator.getVar()
    #     squared_S = np.sum((np.array(workTimes) - mean)**2) / num_trials
    #     #squared_S = np.var(workTimes)

    #     Me = get_Me(workTimes)

    #     
    #     length = len(workTimes)
    #     if length == 1:
    #         R = 0
    #     else:
    #         R = workTimes[length-1] - workTimes[0]
    #     #
    #     characteristics = [E, mean, np.abs(E - mean), D, squared_S, np.abs(D - squared_S), Me, R]

    # except ValueError as error:
    #     return render_template("index.html", error=str(error))
    # except Exception as error:
    #     return render_template("index.html", error=str(error))
    # if isPositive:
    #     return render_template("index.html", q=q, r=r, n=n, num_trials=num_trials, data=workTimes, distributing_function=distributing_function, plot_url=plot_url, labels=characteristics_labels, characteristics=characteristics)
    # return render_template("index.html", q=q, r=r, n=n, num_trials=num_trials, data=workTimes, distributing_function=distributing_function, plot_url=plot_url, labels=characteristics_labels, characteristics=characteristics, error="Неправильные параметры, время не может быть отрицательным")
    return render_template("index.html")