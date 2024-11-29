# app.py
from flask import Flask, jsonify, render_template, request
import numpy as np
import pandas as pd
from random_generators import getExponentialRandomGenerator, getHomeLikeGenerator
from device import Device
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import scipy.stats as st


matplotlib.use('Agg')  # Устанавливаем Agg backend *ПЕРЕД* импортом pyplot

app = Flask(__name__)

@app.route('/interval', methods=['POST'])
def intervals():
    # try:
        # Получаем данные
        intervals = request.form.get("intervals")
        work_times = request.form.get("workTimes")
        mean = float(request.form.get("mean"))
        disp = float(request.form.get("disp"))
        print(disp)

        # Преобразуем строку JSON в объекты Python
        intervals = np.array(eval(intervals))
        work_times = np.array(eval(work_times))

        if len(intervals) < 2:
            raise ValueError("Интервалы должны содержать хотя бы два значения.")

        hist_values, bin_centers = compute_histogram_with_intervals_manual(work_times, intervals, density=True)
        pdf_real = st.norm.pdf(bin_centers, mean, np.sqrt(disp))
        #print(pdf_real)
        max_sub = np.max(np.abs(pdf_real - hist_values))
        # Вычисление гистограммы
        #hist_values, _ = np.histogram(work_times, bins=intervals)
        #bin_centers = [(intervals[i] + intervals[i + 1]) / 2 for i in range(len(intervals) - 1)]
        plt.figure()
        #plt.hist(workTimes, density=density, cumulative=cumulative, bins=bins, alpha=0.7, label='Время работы')

        plt.xlabel('$t$')
        #plt.ylabel('Относительная частота')
        plt.title('Гистограмма относительных частот')
        #plt.legend()
        plt.bar(bin_centers, hist_values, width=np.diff(intervals), align='center', alpha=0.7, edgecolor='black')
        img = io.BytesIO()
        plt.savefig(img, format='svg')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        # Возвращаем данные
        return jsonify({
            "pdf_select": hist_values.tolist(),
            "pdf_real": pdf_real.tolist(),
            "bin_centers": list(bin_centers),
            "max_sub": max_sub,
            "graph_url":  plot_url})
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

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


def compute_histogram_with_intervals_manual(data, bin_edges, density=False, cumulative=False):
    """
    Вычисляет значения гистограммы для данных с использованием циклов, без использования np.histogram.
    
    :param data: Список или массив данных для гистограммы.
    :param bin_edges: Массив с границами интервалов.
    :param density: Если True, гистограмма будет нормализована (относительная частота).
    :param cumulative: Если True, гистограмма будет накопительной.
    
    :return: (values, bin_centers) - значения гистограммы и середины интервалов.
    """
    
    # Преобразуем data в numpy-массив для более быстрого вычисления
    data = np.array(data)
    #hist_values, _ = plt.hist(data, bins='auto', cumulative=True, density=True)

    #Инициализируем массив для значений гистограммы
    hist_values = np.zeros(len(bin_edges) - 1)
    
    # Цикл по каждому элементу данных
    for value in data:
        # Для каждого значения находим, в какой интервал оно попадает
        for i in range(len(bin_edges) - 1):
            if bin_edges[i] <= value and value < bin_edges[i + 1]:
                hist_values[i] += 1
                break
    

    
    #Если нужно накопительное распределение (cumulative=True)
    if cumulative:
        hist_values = np.cumsum(hist_values)

    # Нормализация по желанию (density=True)
    if density and cumulative:
        total_count = data.shape[0]
        bin_widths = np.diff(bin_edges)
        # hist_values = hist_values / (total_count * bin_widths)
        hist_values = hist_values / total_count
    if density and not cumulative:
        total_count = data.shape[0]
        bin_widths = np.diff(bin_edges)
        hist_values = hist_values / (total_count * bin_widths)
    
    # Вычисляем середины интервалов
    bin_centers = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)]
    
    return hist_values, bin_centers

def generate_cdf_plot(workTimes, mean, disp, bin_edges):
    """
    Генерирует гистограмму относительных частот для списка workTimes и возвращает ее как base64 закодированное SVG изображение.

    Args:
        workTimes: массив числовых значений.

    Returns:
        Строку base64, представляющую SVG изображение гистограммы, или None, если workTimes пуст или невалиден.
    """
    workTimes = np.array(workTimes)
    if np.size(workTimes) == 0:
        raise ValueError("Empty or invalid workTimes.")
    x_min = np.min(workTimes)
    x_max = np.max(workTimes)
    
    x = np.linspace(x_min, x_max, 1000)
    cdf = st.norm.cdf(x, mean, np.sqrt(disp))
    #
    if (bin_edges == 'auto'):
        count = int((np.log(workTimes.shape[0]))) + 1
        #count = max(count, 1)
        if workTimes.shape[0] > 100:
            count = 100
        count = max(count, 1)
        #count = 100
        #
        bin_edges = np.linspace(x_min, x_max, count + 1)
        
    #
    print(bin_edges)
    print(workTimes)
    hist_values, bin_centers = compute_histogram_with_intervals_manual(workTimes, bin_edges, density=True, cumulative=True)
    print(hist_values, bin_centers)
    #
    plt.figure()
    #plt.hist(workTimes, density=density, cumulative=cumulative, bins=bins, alpha=0.7, label='Время работы')
    plt.plot(x, cdf, label=r"$F_\eta(x)$")
    if (len(bin_edges) < 10):
        plt.plot(bin_centers, hist_values, "-o", label=r"$\hat{F_\eta(x)}$")
    else:
        plt.plot(bin_centers, hist_values, label=r"$\hat{F_\eta(x)}$")
    Fn = st.norm.cdf(bin_centers, mean, np.sqrt(disp))
    D = np.max(np.abs(hist_values - Fn))
    plt.xlabel('$t$')
    #plt.ylabel('Относительная частота')
    plt.title('График $\hat{F_\eta(x)}$ и $F_\eta(x)$ ' + f"D = {D}")
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='svg')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url

@app.route("/cdf-plot", methods=["POST"])
def plot():
        """
        Генерация гистограммы по заданным интервалам.
        Ожидает JSON с ключами:
        - workTimes: массив значений
        - bins: количество интервалов
        """
    #
    #try:
        # Извлечение данных из запроса
        data = request.get_json()
        
        workTimes = data.get("workTimes", [])
        #bin_edges = data.get("bin_edges", "auto")
        mean = data.get("mean", 1)
        D = data.get("disp", 1)

        # # Проверка данных
        # if not isinstance(workTimes, list) or not all(isinstance(x, (int, float)) for x in workTimes):
        #     raise ValueError("Invalid 'workTimes', must be a list of numbers.")

        # Генерация гистограммы
        plot_url = generate_cdf_plot(workTimes, mean, D, 'auto')

        # Формируем успешный ответ
        return jsonify({"plot_url": plot_url, "error": ""}), 200

    #except Exception as e:
        
        return jsonify({"error": str(e)}), 400


@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Обработка данных формы
        q, r, n, num_trials, distributing_function = process_form()
        random_generator = get_random_generator_by_name(q, r, distributing_function)

        # Генерация данных
        isPositive = random_generator.isPositive()
        workTimes = get_work_time_series(n, num_trials, random_generator)
        
        # Проверка предупреждений
        warning = ""
        if not isPositive:
            warning = "Могут быть отрицательные значения"

        # Вычисление характеристик
        E = n * random_generator.getMean()
        mean = np.sum(workTimes) / num_trials
        D = n * random_generator.getVar()
        squared_S = np.sum((np.array(workTimes) - mean) ** 2) / num_trials
        Me = get_Me(workTimes)

        # Расчет размаха
        sorted_workTimes = sorted(workTimes)
        length = len(sorted_workTimes)
        R = 0 if length <= 1 else sorted_workTimes[-1] - sorted_workTimes[0]

        # Формируем характеристики и их метки
        characteristics_labels = [
            r"E_\eta", r"\bar{x}", r"\left| E_\eta - \bar{x} \right|", 
            r"D\eta", r"S^2", r"\left| D_\eta - S^2 \right|", 
            r"\hat{Me}", r"\hat{R}"
        ]
        characteristics = [
            E, mean, abs(E - mean), D, squared_S, 
            abs(D - squared_S), Me, R
        ]

        # Формирование ответа
        message = {
            "workTimes": workTimes,
            "warning": warning,
            "error": "",
            "labels": characteristics_labels,
            "characteristics": characteristics
        }
        
        return jsonify(message), 200

    except ValueError as e:
        
        message = {
            "workTimes": [],
            "warning": "",
            "error": str(e),
            "labels": [],
            "characteristics": []
        }
        return jsonify(message), 400

    except Exception as e:
        
        message = {
            "workTimes": [],
            "warning": "",
            "error": str(e),
            "labels": [],
            "characteristics": []
        }
        return jsonify(message), 500



@app.route("/", methods=["GET", "POST"])
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

def get_Me(workTimes):
    length = len(workTimes)
    if length == 1:
        return workTimes[0]
    if length == 2:
        return (workTimes[0] + workTimes[1]) / 2
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