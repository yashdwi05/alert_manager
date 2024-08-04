from flask import Flask, Response
from prometheus_client import start_http_server, Gauge, generate_latest
import psutil
import time
from threading import Thread

# Initialize the Flask application
app = Flask(__name__)

# Define Prometheus metrics to track CPU and memory usage
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory usage percentage')

# Function to collect CPU and memory metrics
def collect_metrics():
    while True:
        CPU_USAGE.set(psutil.cpu_percent(interval=1))
        MEMORY_USAGE.set(psutil.virtual_memory().percent)
        time.sleep(5)

# Define a route for the root URL that returns a simple message
@app.route('/')
def hello():
    return "Hello, World!"

# Define a route for the /metrics URL that returns the metrics in Prometheus format
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

# Main entry point of the application
if __name__ == '__main__':
    # Start a Prometheus HTTP server on port 8000
    start_http_server(8000)
    # Start a new thread to collect metrics continuously
    Thread(target=collect_metrics).start()
    # Start the Flask application on port 5000
    app.run(host='0.0.0.0', port=5000)
