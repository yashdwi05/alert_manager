# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary system packages
RUN apt-get update && apt-get install -y gcc python3-dev

# Install Flask, psutil and Prometheus client library
RUN pip install --no-cache-dir Flask==2.3.3 psutil==5.9.5 prometheus_client==0.16.0

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
