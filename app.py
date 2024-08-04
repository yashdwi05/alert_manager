from flask import Flask, request, jsonify
import requests
import os
from prometheus_api_client import PrometheusConnect, PrometheusApiClientException

app = Flask(__name__)

# Get Slack webhook URL from environment variable
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

# Prometheus connection
prometheus_url = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    This endpoint receives incoming alerts.
    """
    alert = request.json
    
    # Filter for only critical alerts
    if alert['labels'].get('severity', '').upper() != 'CRITICAL':
        return jsonify({"message": "Alert ignored (not critical)"}), 200
    
    # Enrich the alert data
    enriched_data = enrich_alert(alert)
    
    # Take action based on the enriched data
    take_action(enriched_data)
    
    return jsonify({"message": "Critical alert received and processed"}), 200

def enrich_alert(alert):
    """
    Enrich the alert data with memory and CPU usage percentages.
    """
    memory_usage, cpu_usage = get_pod_metrics()

    # Add the metrics to the alert data
    alert['enriched'] = {
        'memory_usage': f"{memory_usage:.2f}%",
        'cpu_usage': f"{cpu_usage:.2f}%"
    }
    return alert

def get_pod_metrics():
    """
    Fetch memory and CPU usage percentages from Prometheus.
    """
    try:
        # Prometheus queries to get memory and CPU usage percentages
        memory_query = 'memory_usage_percent'
        cpu_query = 'cpu_usage_percent'

        # Execute the Prometheus queries
        memory_data = prom.custom_query(query=memory_query)
        cpu_data = prom.custom_query(query=cpu_query)

        # Extract the metric values from the query results
        memory_usage = float(memory_data[0]['value'][1]) if memory_data else 0.0
        cpu_usage = float(cpu_data[0]['value'][1]) if cpu_data else 0.0

    except PrometheusApiClientException as e:
        # Log any errors that occur during the query
        app.logger.error(f"Error fetching metrics: {e}")
        memory_usage = 0.0
        cpu_usage = 0.0

    return memory_usage, cpu_usage

def take_action(alert):
    """
    Take action based on the enriched alert data, such as sending a notification to Slack.
    """
    message = format_alert(alert)
    send_to_slack(message)

def format_alert(alert):
    """
    Format the alert data into a message string.
    """
    return (f"Alert: {alert['labels']['alertname']}\n"
            f"Severity: {alert['labels']['severity']}\n"
            f"Description: {alert['annotations']['description']}\n"
            f"Memory Usage: {alert['enriched']['memory_usage']}\n"
            f"CPU Usage: {alert['enriched']['cpu_usage']}")

def send_to_slack(message):
    """
    Send a message to Slack using the webhook URL.
    """
    if not SLACK_WEBHOOK_URL:
        raise ValueError("Slack webhook URL is not set")

    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)
