Here’s a breakdown of the solution, including a Python script to monitor the services, create JSON files, and a simple REST API for interacting with Elasticsearch.

# Step-by-Step Instructions

## 1. Monitoring Script:

The first Python script will check the status of the httpd, rabbitmq-server, and postgresql services on a Linux machine, and generate a JSON object based on their statuses. Each service's status will be written to a separate JSON file.

#### `monitor_services.py:`
```python
import os
import json
import socket
from datetime import datetime

# List of services to monitor
SERVICES = ["httpd", "rabbitmq-server", "postgresql"]
HOST_NAME = socket.gethostname()

# Function to check if a service is running
def is_service_running(service_name):
    status = os.system(f"systemctl is-active --quiet {service_name}")
    return "UP" if status == 0 else "DOWN"

# Monitor services and create JSON files
def monitor_services():
    for service in SERVICES:
        service_status = is_service_running(service)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        json_payload = {
            "service_name": service,
            "service_status": service_status,
            "host_name": HOST_NAME
        }
        
        # Create JSON filename
        file_name = f"{service}-status-{timestamp}.json"
        
        # Write JSON to file
        with open(file_name, "w") as json_file:
            json.dump(json_payload, json_file, indent=4)
            print(f"Status for {service} written to {file_name}")

if __name__ == "__main__":
    monitor_services()

```

## 2. REST API Script:

The second script creates a simple REST API to interact with Elasticsearch using the Flask web framework. It allows data to be posted to Elasticsearch and retrieved via specific endpoints.

#### `app.py:`
```python
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import json
import os

# Initialize Flask app and Elasticsearch client
app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])  # Adjust Elasticsearch configuration as needed

# Helper function to check overall application status
def get_application_status():
    status_list = [doc['_source']['service_status'] for doc in es.search(index="services", body={"query": {"match_all": {}}})['hits']['hits']]
    return "UP" if all(status == "UP" for status in status_list) else "DOWN"

# Endpoint to add data to Elasticsearch
@app.route('/add', methods=['POST'])
def add_to_elasticsearch():
    try:
        # Get JSON data from request
        json_file = request.files['file']
        json_data = json.load(json_file)
        service_name = json_data['service_name']

        # Write to Elasticsearch index
        es.index(index="services", doc_type="_doc", id=service_name, body=json_data)
        return jsonify({"message": "Data added to Elasticsearch successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get the overall health of the application
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        app_status = get_application_status()
        return jsonify({"application_status": app_status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get the status of a specific service
@app.route('/healthcheck/<service_name>', methods=['GET'])
def healthcheck_service(service_name):
    try:
        res = es.get(index="services", doc_type="_doc", id=service_name)
        return jsonify({"service_name": service_name, "service_status": res['_source']['service_status']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True)

```

# Service Monitoring and Healthcheck API

## Overview

This project includes:
1. **`monitor_services.py`**: A script to monitor Linux services (`httpd`, `rabbitmq-server`, and `postgresql`) and create JSON files based on their status.
2. **`app.py`**: A REST API that accepts these JSON files and stores them in Elasticsearch. It also provides endpoints to check the application and service health.

## Prerequisites

1. Python 3.7+ installed.
2. Elasticsearch running locally or configured to match your server settings.
3. Required Python packages: `flask`, `elasticsearch`.
   Install with:
   
   ```bash
   pip install flask elasticsearch
4. Services to monitor (httpd, rabbitmq-server, postgresql) must be set up as Linux services.

# How to Run
## Step 1: Monitor Services

To monitor services and create JSON files, run:
```bash
python monitor_services.py
```
JSON files will be created in the same directory with the format `{serviceName}-status-{timestamp}.json`.

## Step 2: Run REST API
To start the REST API server, execute:

```bash
python app.py

```
The server will start on `http://127.0.0.1:5000`.

# API Endpoints
## 1. Add a JSON file to Elasticsearch

- POST /add
- Content-Type: multipart/form-data
- Upload the JSON file with the file parameter.
  
```bash
curl -X POST -F 'file=@httpd-status-202410230930.json' http://127.0.0.1:5000/add
```

## 2. Check overall application status

-  GET  `/healthcheck`
```bash
curl http://127.0.0.1:5000/healthcheck
```
## 3. Check specific service status

- GET `/healthcheck/{serviceName}`
```bash
curl http://127.0.0.1:5000/healthcheck/httpd
```



  