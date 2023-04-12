import requests
import os

import yaml
from flask import Flask, jsonify, Response, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

PORT = 420

# Note: Setting CORS to allow chat.openapi.com is required for ChatGPT to access your plugin
CORS(app, origins=[f"http://localhost:{PORT}", "https://chat.openai.com"])

api_url = 'http://127.0.0.1:5000'

@app.route('/.well-known/ai-plugin.json')
def serve_manifest():
    return send_from_directory(os.path.dirname(__file__), 'ai-plugin.json')

@app.route('/openapi.yaml')
def serve_openapi_yaml():
    with open(os.path.join(os.path.dirname(__file__), 'openapi.yaml'), 'r') as f:
        yaml_data = f.read()
    yaml_data = yaml.load(yaml_data, Loader=yaml.FullLoader)
    return jsonify(yaml_data)

@app.route('/openapi.json')
def serve_openapi_json():
    return send_from_directory(os.path.dirname(__file__), 'openapi.json')

@app.route('/todos', methods=['GET', 'POST'])
@app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def wrapper(todo_id=None):
    headers = {
        'Content-Type': 'application/json',
    }

    if todo_id is None:
        url = f'{api_url}/todos'
    else:
        url = f'{api_url}/todos/{todo_id}'

    print(f'Forwarding call: {request.method} -> {url}')

    if request.method == 'GET':
        response = requests.get(url, headers=headers, params=request.args)
    elif request.method == 'POST':
        response = requests.post(url, headers=headers, params=request.args, json=request.json)
    elif request.method == 'PUT':
        response = requests.put(url, headers=headers, params=request.args, json=request.json)
    elif request.method == 'DELETE':
        response = requests.delete(url, headers=headers, params=request.args)
    else:
        raise NotImplementedError(f'Method {request.method} not implemented in wrapper for {url=}')

    return response.content

if __name__ == '__main__':
    app.run(port=PORT)
