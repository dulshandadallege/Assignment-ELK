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
