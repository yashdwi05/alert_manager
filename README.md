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

<img width="712" alt="image" src="https://github.com/user-attachments/assets/438dccd3-be99-42ac-8fd1-6dfc04ee6ab2">

## Setup Prerequisites

### Web Application
1. Clone the repository and navigate to the webserver directory.
2. Create the kubernetes namespace (if it doesn't exist)
    ```bash
    kubectl create ns <namespace>
    ```
3. Deploy the application to Kubernetes:
    ```bash
    kubectl apply -f webserver-deployment.yaml
    ```
4. Update Prometheus.yaml file and deploy on kubernetes (Read Comment in Yaml file).
    ```bash
    kubectl apply -f prometheus.yaml
    ```
5. Access the Prometheus UI: Open your web browser and navigate to the Prometheus UI. Use the node IP and NodePort you configured earlier, e.g., http://<PROMETHEUS_IP>:30090.
6. Check Targets: In the Prometheus UI, go to Status -> Targets and ensure the flask-app target is listed and UP.
7. Query Metrics: Use the expression {job="flask-app"} to see the CPU and memory usage metrics being scraped from the Flask service.

## Alert Manager Setup

1. Navigate to the project directory (alert_manager).
2. Create the Docker Image using Dockerfile and push it to docker hub repository:
    ```bash
    docker build -t <username>/alert-manager:<tag> .
    docker push <username>/alert-manager:<tag>
    ```
3. Update the configmap file PROMETHEUS_URL and SLACK_WEBHOOK_URL and apply the configmap:
    ```bash
    kubectl apply -f configmap.yaml
    ```
4. Update deployment for earlier build image and Apply the deployment:
    ```bash
    kubectl apply -f deployment.yaml
    ```
5. 

## Docker

To run the application using Docker:

1. Build the Docker image:
    ```bash
    docker build -t <username>/alert-manager:<tag>  .
    ```
2. Run the Docker container:
    ```bash
    docker run -p 5000:5000 <username>/alert-manager:<tag> 
    ```

## Kubernetes

To deploy the application to Kubernetes:

1. Update the configmap file PROMETHEUS_URL and SLACK_WEBHOOK_URL and apply the configmap.
   ```bash
    kubectl apply -f configmap.yaml
    ```
2. Apply the deployment:
    ```bash
    kubectl apply -f deployment.yaml
    ```

## Testing

1. Ensure Webserver, Prometheus and Alertmanager are running.
2. Get the node IP and NodePort.
   ```bash
   #Get Node IP
   kubectl get po -n <namespace> -o wide
   #Get Service NodePort
   kubectl get service -n <namespace>
   ```
4. Trigger an alert and check the Slack channel for notifications. Use the node IP and NodePort you configured for the service.

   #### Test Alert 1:
   
   ```bash
    curl -X POST http://<AlertManagerIP>:<NodePort>/webhook -H "Content-Type: application/json" -d '{
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
   
   #### Test Alert 2:

   ```bash
    curl -X POST http://<AlertManagerIP>:<NodePort>/webhook -H "Content-Type: application/json" -d '{
   "annotations": {
    "description": "Pod customer/customer-rs-transformer-9b75b488c-cpfd7 (rs-transformer) is restarting 2.11 times / 10 minutes.",
    "summary": "Pod is crash looping."
   },
   "labels": {
    "alertname": "KubePodCrashLooping",
    "namespace": "customer",
    "pod": "customer-rs-transformer-9b75b488c-cpfd7",
    "severity": "CRITICAL"
   },
   "startsAt": "2022-03-02T07:31:57.339Z",
   "status": "firing"
   }'
    ```

## Extending

To extend the system to handle more types of alerts and actions, modify the `enrich_alert` and `take_action` functions in the `app.py` file.

Feel free to reach out if you have any questions.
