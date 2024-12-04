from flask import jsonify, request
from .generate_cdf_plot import generate_cdf_plot
import logging
logger = logging.getLogger(__name__)
#@app.route("/cdf-plot", methods=["POST"])
def plot():
    #
    try:
        data = request.get_json()
        
        workTimes = data.get("workTimes", [])
        mean = data.get("mean", 1)
        D = data.get("disp", 1)

        # Генерация гистограммы
        plot_url = generate_cdf_plot(workTimes, mean, D, 'auto')
        logger.info("График построен")
        # Формируем успешный ответ
        return jsonify({"plot_url": plot_url, "error": ""}), 200

    except Exception as e:
        
        return jsonify({"error": str(e)}), 400