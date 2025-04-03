import requests
import os
import json
import time
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file
def load_env():
    # Try to load from current directory first
    env_path = pathlib.Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    
    # Then try from the RunpodOllama directory
    env_path = pathlib.Path("RunpodOllama/.env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

load_env()

def call_runpod_api(prompt, model=None, api_key=None, endpoint_id=None, wait_for_result=False, poll_interval=1, max_retries=10):
    """
    Call the RunPod API with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the model
        model (str, optional): Override the model used on the server
        api_key (str, optional): Your RunPod API key (will use RUNPOD_API_KEY or RUNPOD_API_TOKEN env var if not provided)
        endpoint_id (str, optional): Your RunPod endpoint ID (will use RUNPOD_ENDPOINT_ID env var if not provided)
        wait_for_result (bool, optional): Whether to wait for the result (default: False)
        poll_interval (float, optional): How often to check for result in seconds (default: 1)
        max_retries (int, optional): Maximum number of retries when checking status (default: 10)
    
    Returns:
        dict: The API response
    """
    # Get API key from parameters or environment variables
    api_key = api_key or os.environ.get("RUNPOD_API_KEY") or os.environ.get("RUNPOD_API_TOKEN")
    if not api_key:
        raise ValueError("API key is required. Provide it as a parameter or set RUNPOD_API_KEY/RUNPOD_API_TOKEN environment variable.")
    
    # Get endpoint ID from parameters or environment variable
    endpoint_id = endpoint_id or os.environ.get("RUNPOD_ENDPOINT_ID")
    if not endpoint_id:
        raise ValueError("Endpoint ID is required. Provide it as a parameter or set RUNPOD_ENDPOINT_ID environment variable.")
    
    # Set up headers with authentication
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Prepare request payload
    data = {
        'input': {
            'method_name': 'generate',
            'input': {
                'prompt': prompt
            }
        }
    }
    
    # Add model to request if provided
    if model:
        data['input']['input']['model'] = model
    
    # Make the API request
    api_url = f'https://api.runpod.ai/v2/{endpoint_id}/run'
    response = requests.post(api_url, headers=headers, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        
        # If not waiting for result, return immediately
        if not wait_for_result:
            return result
        
        # Otherwise, poll for result
        return wait_for_runpod_result(result['id'], api_key, endpoint_id, poll_interval, max_retries)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def check_runpod_status(job_id, api_key, endpoint_id):
    """
    Check the status of a RunPod job.
    
    Args:
        job_id (str): The ID of the job to check
        api_key (str): Your RunPod API key
        endpoint_id (str): Your RunPod endpoint ID
        
    Returns:
        dict: The status response
    """
    status_url = f'https://api.runpod.ai/v2/{endpoint_id}/status/{job_id}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking status: {str(e)}")
        return None

def get_runpod_output(job_id, api_key, endpoint_id):
    """
    Get the output of a completed RunPod job.
    
    Args:
        job_id (str): The ID of the job to get output for
        api_key (str): Your RunPod API key
        endpoint_id (str): Your RunPod endpoint ID
        
    Returns:
        dict: The output response
    """
    # In RunPod, the status endpoint can also return the result when it's complete
    status_url = f'https://api.runpod.ai/v2/{endpoint_id}/status/{job_id}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Check if the result is already included in the status response
        if 'output' in data:
            return data
        
        # If not, try the output endpoint
        output_url = f'https://api.runpod.ai/v2/{endpoint_id}/output/{job_id}'
        response = requests.get(output_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting output: {str(e)}")
        # Return the status response as fallback
        return {"status": "COMPLETED", "error": str(e)}

def wait_for_runpod_result(job_id, api_key, endpoint_id, poll_interval=1, max_retries=10):
    """
    Wait for a RunPod job to complete and return the result.
    
    Args:
        job_id (str): The ID of the job to wait for
        api_key (str): Your RunPod API key
        endpoint_id (str): Your RunPod endpoint ID
        poll_interval (float): How often to check for result in seconds
        max_retries (int): Maximum number of retries for checking result
        
    Returns:
        dict: The job result
    """
    print(f"Job submitted with ID: {job_id}")
    print("Waiting for result...", end='', flush=True)
    
    retries = 0
    
    while retries < max_retries:
        status_response = check_runpod_status(job_id, api_key, endpoint_id)
        
        if not status_response:
            retries += 1
            if retries >= max_retries:
                print(f" Failed after {max_retries} retries!")
                return {"error": "Max retries exceeded", "status": "FAILED"}
            print("x", end='', flush=True)
            time.sleep(poll_interval)
            continue
        
        status = status_response.get('status')
        
        # If job is completed, get the output
        if status == 'COMPLETED':
            print(" Done!")
            # Check if the output is already in the status response
            if 'output' in status_response:
                return status_response
            return get_runpod_output(job_id, api_key, endpoint_id)
        
        # If job failed, return the status
        elif status in ['FAILED', 'CANCELLED']:
            print(f" {status}!")
            return status_response
        
        # Otherwise, wait and try again
        print(".", end='', flush=True)
        time.sleep(poll_interval)
    
    print(" Timed out!")
    return {"error": "Timed out waiting for result", "status": "TIMEOUT"}

def stream_output(response):
    """
    Extract and print the streaming output from a RunPod response.
    """
    if not response:
        print("No response received")
        return
    
    if 'error' in response:
        print(f"\nError: {response['error']}")
        return
    
    if 'output' not in response:
        print("\nRunPod response:")
        print(json.dumps(response, indent=2))
        return
    
    output = response['output']
    
    # Extract the model's text output
    if isinstance(output, dict) and 'response' in output:
        print("\nResponse from model:\n")
        print(output['response'])
    elif isinstance(output, dict) and 'generation' in output:
        print("\nResponse from model:\n")
        print(output['generation'])
    elif isinstance(output, dict):
        print("\nResponse from model:\n")
        print(json.dumps(output, indent=2))
    else:
        print("\nRaw output:\n")
        print(output)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Call the RunPod API")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to send to the model")
    parser.add_argument("--model", type=str, help="Model to use (overrides server default)")
    parser.add_argument("--api-key", type=str, help="RunPod API key (defaults to RUNPOD_API_KEY env var)")
    parser.add_argument("--endpoint-id", type=str, help="RunPod endpoint ID (defaults to RUNPOD_ENDPOINT_ID env var)")
    parser.add_argument("--wait", action="store_true", help="Wait for the result and display it")
    parser.add_argument("--poll-interval", type=float, default=1.0, help="How often to check for result in seconds")
    parser.add_argument("--max-retries", type=int, default=60, help="Maximum number of status check retries")
    
    args = parser.parse_args()
    
    result = call_runpod_api(
        prompt=args.prompt,
        model=args.model,
        api_key=args.api_key,
        endpoint_id=args.endpoint_id,
        wait_for_result=args.wait,
        poll_interval=args.poll_interval,
        max_retries=args.max_retries
    )
    
    if result:
        if args.wait:
            # Stream the output
            stream_output(result)
        else:
            # Print the job info
            print(json.dumps(result, indent=2)) 