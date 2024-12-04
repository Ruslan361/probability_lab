from .generate_cdf_plot_route import generate_cdf_plot_route
from .index import index
from .generate_histogram_route import generate_histogram_route
from .submit_data import submit_data
from .chi_squared_test_route import chi_squared_test_route, chi_squared_test

def setup_routes(app):
    @app.route("/cdf-plot", methods=["POST"])
    def plot1():
        return generate_cdf_plot_route()
    
    @app.route("/", methods=["GET"])
    def index1():
        return index()
    
    @app.route('/interval', methods=['POST'])
    def interval():
        return generate_histogram_route()
    
    @app.route("/submit", methods=["POST"])
    def submit1():
        return submit_data()
    
    @app.route("/intervals2", methods=["POST"])
    def intervals3():
        return chi_squared_test_route()
    