import runpod
from typing import Any, Literal, TypedDict
import requests
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HandlerInput(TypedDict):
    """The data for calling the Ollama service."""

    method_name: Literal["generate"]
    """The url endpoint of the Ollama service to make a post request to."""

    input: Any
    """The body of the post request to the Ollama service."""


class HandlerJob(TypedDict):
    input: HandlerInput


def handler(job: HandlerJob):
    # Get base URL from environment variable or use default
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://0.0.0.0:11434")
    
    # Verify API key if authentication is enabled
    api_key = os.environ.get("RUNPOD_API_KEY")
    if api_key and "authorization" in job.get("headers", {}):
        auth_header = job.get("headers", {}).get("authorization", "")
        if not auth_header.startswith("Bearer ") or auth_header[7:] != api_key:
            logger.error("Invalid API key provided")
            return {"error": "Unauthorized: Invalid API key", "status": "failed"}
    
    input = job["input"]
    logger.info(f"Received request for method: {input['method_name']}")

    # Streaming is not supported in serverless mode
    input["input"]["stream"] = False
    
    # Get the model name from arguments
    model = sys.argv[1]
    input["input"]["model"] = model
    
    logger.info(f"Using model: {model}")
    logger.info(f"Sending request to: {base_url}/api/{input['method_name']}/")

    try:
        response = requests.post(
            url=f"{base_url}/api/{input['method_name']}/",
            headers={"Content-Type": "application/json"},
            json=input["input"],
            timeout=120  # Add timeout to prevent hanging indefinitely
        )
        response.encoding = "utf-8"
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return {"error": str(e), "status": "failed"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": str(e), "status": "failed"}


runpod.serverless.start({"handler": handler})
