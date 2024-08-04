# Alert Manager

### Problem Statement:

We need to set up a monitoring solution for a Flask application to gather and expose real-time CPU and memory usage metrics. This setup will be used for dummy testing purposes. The metrics should be collected and exposed in a format that Prometheus can scrape and monitor.

**Description**

This project demonstrates how to:

1. Create a Flask application that collects real-time CPU and memory metrics.
2. Dockerize the Flask application.
3. Deploy the Flask application to a Kubernetes cluster.
4. Configure Prometheus to scrape the metrics from the Flask application.

## Overview

This project implements an Alert Manager system to handle specific alerts **CRITICAL** programmatically. It receives alerts, enriches the data, and takes actions such as sending notifications to Slack.

### Prerequisites
- Docker
- Kubernetes cluster
- kubectl configured to interact with your Kubernetes cluster
- Application to expose metrics
- Prometheus

### Architecture

<img width="737" alt="image" src="https://github.com/user-attachments/assets/eb2a6597-ce6e-4b96-90a3-102582e6c76d">

## Setup Prerequisites

### Web Application
1. Clone the repository and navigate to the webserver directory.
2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Create the kubernetes namespace (if it doesn't exist)
    ```bash
    kubectl create ns <namespace>
    ```
5. Deploy the application to Kubernetes:
    ```bash
    kubectl apply -f webserver-deployment.yaml
    ```
6. Update Prometheus.yaml file and deploy on kubernetes (Read Comment in Yaml file).
    ```bash
    kubectl apply -f prometheus.yaml
    ```
7. Access the Prometheus UI: Open your web browser and navigate to the Prometheus UI. Use the node IP and NodePort you configured earlier, e.g., http://<PROMETHEUS_IP>:30090.
8. Check Targets: In the Prometheus UI, go to Status -> Targets and ensure the flask-app target is listed and UP.
9. Query Metrics: Use the expression {job="flask-app"} to see the CPU and memory usage metrics being scraped from the Flask service.

## Alert Manager Setup

1. Clone the repository and navigate to the project directory(alert_manager).
2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up your Slack webhook URL in the `app.py` file.
5. Run the Flask application:
    ```bash
    python3 app.py
    ```

## Docker

To run the application using Docker:

1. Build the Docker image:
    ```bash
    docker build -t alert-manager .
    ```
2. Run the Docker container:
    ```bash
    docker run -p 5000:5000 alert-manager
    ```

## Kubernetes

To deploy the application to Kubernetes:

1. Update the configmap file PROMETHEUS_URL and SLACK_WEBHOOK_URL and apply the configmap.
   ```bash
    kubectl apply -f deployment.yaml
    ```
2. Apply the deployment:
    ```bash
    kubectl apply -f deployment.yaml
    ```

## Testing

1. Ensure Webserver, Prometheus and Alertmanager are running.
2. Trigger an alert and check the Slack channel for notifications.
   ```bash
    curl -X POST http://192.168.123.219:30000/webhook -H "Content-Type: application/json" -d '{
   "annotations": {
    "description": "Pod customer/customer-rs-transformer-9b75b488c-cpfd7 (rs-transformer) is restarting 2.11 times / 10 minutes.",
    "summary": "Pod is crash looping."
   },
   "labels": {
    "alertname": "KubePodCrashLooping",
    "namespace": "customer",
    "pod": "customer-rs-transformer-9b75b488c-cpfd7",
    "severity": "WARNING"
   },
   "startsAt": "2022-03-02T07:31:57.339Z",
   "status": "firing"
   }'
    ```

## Extending

To extend the system to handle more types of alerts and actions, modify the `enrich_alert` and `take_action` functions in the `app.py` file.

Feel free to reach out if you have any questions.
