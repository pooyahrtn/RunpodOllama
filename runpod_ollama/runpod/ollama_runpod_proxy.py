from flask import Flask, request
from .. import ENVIRONMENT
from .runpod_repository import RunpodRepository
import json


app = Flask(__name__)


# Define a dynamic endpoint that includes the route name as a parameter
@app.route("/<pod_id>/api/generate", methods=["POST"])
def receive_post(pod_id: str):
    # Get the request data
    data = request.json
    runpod_repository = RunpodRepository(
        api_key=ENVIRONMENT.RUNPOD_API_TOKEN, pod_id=pod_id
    )
    response = runpod_repository.generate(data)
    print(str(response))
    return json.dumps(response)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
