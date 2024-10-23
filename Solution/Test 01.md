Here’s a breakdown of the solution, including a Python script to monitor the services, create JSON files, and a simple REST API for interacting with Elasticsearch.

# Step-by-Step Instructions

## 1. Monitoring Script:

The first Python script will check the status of the httpd, rabbitmq-server, and postgresql services on a Linux machine, and generate a JSON object based on their statuses. Each service's status will be written to a separate JSON file.

monitor_services.py
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
