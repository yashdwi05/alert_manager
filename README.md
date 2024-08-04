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

This project implements an Alert Manager system to handle alerts programmatically. It receives alerts, enriches the data, and takes actions such as sending notifications to Slack.

###Prerequisites
- Docker
- Kubernetes cluster
- kubectl configured to interact with your Kubernetes cluster
- Prometheus

### Architecture

<img width="737" alt="image" src="https://github.com/user-attachments/assets/eb2a6597-ce6e-4b96-90a3-102582e6c76d">

## Setup

1. Clone the repository and navigate to the project directory.
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
    python app.py
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

1. Apply the deployment:
    ```bash
    kubectl apply -f deployment.yaml
    ```

2. Configure Prometheus to send alerts to the Alert Manager webhook.

## Testing

1. Ensure Prometheus and Alertmanager are running.
2. Trigger an alert and check the Slack channel for notifications.

## Extending

To extend the system to handle more types of alerts and actions, modify the `enrich_alert` and `take_action` functions in the `app.py` file.

Feel free to reach out if you have any questions.
