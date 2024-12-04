from flask import Flask
from auxiliary import setup_routes
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

app = Flask(__name__)
setup_routes(app)

if __name__ == "__main__":
    logger.info("Запуск сервера")
    app.run(debug=True)