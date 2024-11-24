# app.py
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from random_generators import getExponentialRandomGenerator, getHomeLikeGenerator
from device import Device
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Устанавливаем Agg backend *ПЕРЕД* импортом pyplot

app = Flask(__name__)

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
            print(distributing_function)
            #print(distributing_function)
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

def generate_histogram(workTimes):
    """
    Генерирует гистограмму относительных частот для списка workTimes и возвращает ее как base64 закодированное SVG изображение.

    Args:
        workTimes: Список числовых значений.

    Returns:
        Строку base64, представляющую SVG изображение гистограммы, или None, если workTimes пуст или невалиден.
    """

    if not workTimes or not all(isinstance(x, (int, float)) for x in workTimes):  # Проверка на пустой или невалидный список
        return None

    plt.figure()
    plt.hist(workTimes, density=True, bins='auto', alpha=0.7, label='Время работы')  # bins='auto' для автоматического выбора количества корзин
    plt.xlabel('Значение')
    plt.ylabel('Относительная частота')
    plt.title('Гистограмма относительных частот')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='svg')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url

@app.route("/", methods=["GET", "POST"])
def index():
    #q, r, n, num_trials, distributing_function = None, None, None, None, None
    try:
        q, r, n, num_trials, distributing_function= process_form()
        
        random_generator = get_random_generator_by_name(q, r, distributing_function)
        workTimes = get_work_time_series(n, num_trials, random_generator)
        plot_url = generate_histogram(workTimes)
        characteristics_labels = [r"E_\eta", r"\bar{x}", r"\left| E_\eta - \bar{x} \right|" , r"D\eta", r"S^2", r"\left| D_\eta - S^2 \right|", r"\hat{Me}", r"\hat{R}"]

        E = n * random_generator.getMean()
        mean = np.sum(workTimes) / num_trials
        D = n * random_generator.getVar()
        squared_S = np.sum((np.array(workTimes) - mean)**2) / num_trials
        #squared_S = np.var(workTimes)

        Me = get_Me(workTimes)

        print(np.median(workTimes))
        length = len(workTimes)
        if length == 1:
            R = 0
        else:
            R = workTimes[length-1] - workTimes[0]
        #print(3)
        characteristics = [E, mean, np.abs(E - mean), D, squared_S, np.abs(D - squared_S), Me, R]

    except ValueError as error:
        return render_template("index.html", error=str(error))
    except Exception as error:
        return render_template("index.html", error=str(error))
    return render_template("index.html", q=q, r=r, n=n, num_trials=num_trials, data=workTimes, distributing_function=distributing_function, plot_url=plot_url, labels=characteristics_labels, characteristics=characteristics)

def get_Me(workTimes):
    length = len(workTimes)
    if length == 1:
        return workTimes[0]
    if length % 2 == 0:
        return (workTimes[length//2] + workTimes[length//2 + 1]) / 2
    else:
        return (workTimes[(length - 1)//2 + 1])


def get_work_time_series(n, num_trials, random_generator):
    device = Device(n, random_generator)
    workTimes = [float(device.calculateWorkTime()) for i in range(num_trials)]
    workTimes = sorted(workTimes)
    return workTimes

def get_random_generator_by_name(q, r, distributing_function):

    if distributing_function == 'exponential':
        return getExponentialRandomGenerator(Q=q, R=r)
    if distributing_function == 'home-like':
        return getHomeLikeGenerator(Q=q, R=r)
    raise ValueError("Неправильный тип генератора")


if __name__ == "__main__":
    app.run(debug=True)