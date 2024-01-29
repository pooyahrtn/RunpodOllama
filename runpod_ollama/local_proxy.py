"""A local proxy for the Runpod Ollama service.

Runs a local proxy to forward requests to the Runpod Ollama service. 
The API mimicks Ollama's API, but adds a pod_id parameter to the route.
"""


from flask import Flask, request
from runpod_ollama import ENVIRONMENT
from runpod_ollama.runpod_repository import RunpodRepository
import json

app = Flask(__name__)


@app.route("/<pod_id>/api/<endpoint>", methods=["POST"])
def endpoint(pod_id: str, endpoint: str):
    """Forwards"""
    data = request.json
    runpod_repository = RunpodRepository(
        api_key=ENVIRONMENT.RUNPOD_API_TOKEN,
        pod_id=pod_id,
    )
    response = runpod_repository.call_endpoint(endpoint, data)

    return response


def run_local_proxy():
    app.run(debug=True)
