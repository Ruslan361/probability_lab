from .cdf_plot import plot
from .index import index
from .intervals import intervals
from .submit import submit
from .intervals2 import intervals_2

def setup_routes(app):
    @app.route("/cdf-plot", methods=["POST"])
    def plot1():
        return plot()
    
    @app.route("/", methods=["GET"])
    def index1():
        return index()
    
    @app.route('/interval', methods=['POST'])
    def interval():
        return intervals()
    
    @app.route("/submit", methods=["POST"])
    def submit1():
        return submit()
    
    @app.route("/intervals2", methods=["POST"])
    def intervals3():
        return intervals_2()
    