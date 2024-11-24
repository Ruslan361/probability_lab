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
    try:
        q, r, n, num_trials, distributing_function= process_form()
        random_generator = get_random_generator_by_name(q, r, distributing_function)
        #values = random_generator.getNext(n)
        print(distributing_function)
        device = Device(n, random_generator)
        workTimes = [float(device.calculateWorkTime()) for i in range(num_trials)]
        workTimes = sorted(workTimes)
        print(np.mean(workTimes))
        print(np.var(workTimes))
        plot_url = generate_histogram(workTimes)
    except ValueError as error:
        return render_template("index.html", error=str(error))
    except Exception as error:
        return render_template("index.html", error=str(error))
    
    return render_template("index.html", q=q, r=r, n=n, num_trials=num_trials, data=workTimes, distributing_function=distributing_function, plot_url=plot_url)

def get_random_generator_by_name(q, r, distributing_function):

    if distributing_function == 'exponential':
        return getExponentialRandomGenerator(Q=q, R=r)
    if distributing_function == 'home-like':
        return getHomeLikeGenerator(Q=q, R=r)
    raise ValueError("Неправильный тип генератора")


if __name__ == "__main__":
    app.run(debug=True)