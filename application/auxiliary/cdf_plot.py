from flask import jsonify, request
from .generate_cdf_plot import generate_cdf_plot

#@app.route("/cdf-plot", methods=["POST"])
def plot():
    """
    Генерация гистограммы по заданным интервалам.
    Ожидает JSON с ключами:
    - workTimes: массив значений
    - bins: количество интервалов
    """
    #
    try:
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

    except Exception as e:
        
        return jsonify({"error": str(e)}), 400