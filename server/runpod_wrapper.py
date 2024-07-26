import runpod
from typing import Any, TypedDict
import requests
import sys


class HandlerInput(TypedDict):
    """The data for calling the Ollama service."""

    method_name: str
    """The url endpoint of the Ollama service to make a post request to."""

    input: Any
    """The body of the post request to the Ollama service."""


class HandlerJob(TypedDict):
    input: HandlerInput


def handler(job: HandlerJob):
    base_url = "http://0.0.0.0:11434"
    input = job["input"]

    # streaming is not supported in serverless mode
    input["input"]["stream"] = False
    print(sys.argv)
    model = sys.argv[1]
    input["input"]["model"] = model

    response = requests.post(
        url=f"{base_url}/{input['method_name']}",
        headers={"Content-Type": "application/json"},
        json=input["input"],
    )
    response.encoding = "utf-8"

    # TODO: handle errors
    return response.json()


runpod.serverless.start({"handler": handler})
