from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Slack webhook URL
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/your/slack/webhook/url'

@app.route('/webhook', methods=['POST'])
def webhook():
    alert = request.json
    
    # Enrich the alert data (dummy enrichment for demonstration)
    enriched_data = enrich_alert(alert)
    
    # Take action based on the enriched data
    take_action(enriched_data)
    
    return jsonify({"message": "Alert received"}), 200

def enrich_alert(alert):
    # Example of enrichment (dummy data for demonstration)
    alert['enriched'] = {
        'cpu': '75%',
        'memory': '60%'
    }
    return alert

def take_action(alert):
    message = format_alert(alert)
    send_to_slack(message)

def format_alert(alert):
    return f"Alert: {alert['labels']['alertname']}\nSeverity: {alert['labels']['severity']}\nDescription: {alert['annotations']['description']}\nCPU Usage: {alert['enriched']['cpu']}\nMemory Usage: {alert['enriched']['memory']}"

def send_to_slack(message):
    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
