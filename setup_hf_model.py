#!/usr/bin/env python3
"""
Script to set up and deploy Hugging Face's Llama-3.1-8B-Instruct model with RunpodOllama.
"""

import os
import sys
import argparse
import subprocess
import time
from dotenv import load_dotenv
from runpod_ollama.config import ENVIRONMENT

def setup_env():
    """Ensure environment variables are properly set."""
    # Load environment variables
    load_dotenv()
    
    # Check for HF token
    hf_token = ENVIRONMENT.HF_TOKEN
    if not hf_token:
        print("ERROR: HF_TOKEN not found in environment or .env file.")
        print("Please add your Hugging Face token to a .env file or set it as an environment variable.")
        sys.exit(1)
    
    # Check for RunPod token
    runpod_token = ENVIRONMENT.RUNPOD_API_TOKEN
    if runpod_token == "test_mode_token":
        print("WARNING: Using test mode token for RunPod API. This will not work for actual deployments.")
        print("Please add your RunPod API token to a .env file or set it as an environment variable.")
        return False
    
    return True

def create_model_endpoint(model_id="llama-3.1-8b-instruct", disk_size=20):
    """Create a RunPod template and endpoint for the specified model."""
    try:
        cmd = ["python", "run_cli.py", "create-model", model_id, str(disk_size)]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        # Check if endpoint was created successfully
        if "Created endpoint" in result.stdout:
            print(f"✅ Successfully created endpoint for {model_id}")
            return True
        else:
            print(f"⚠️ Endpoint creation might have failed, check the output above.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create model endpoint: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def start_proxy():
    """Start the local proxy server."""
    try:
        cmd = ["python", "run_cli.py", "start-proxy"]
        print("Starting local proxy server...")
        print("The proxy will run in the foreground. Press Ctrl+C to stop it.")
        print("If you want to run it in the background, open a new terminal and use:")
        print("cd ~/RBT/LocalBrain/RunpodOllama && python run_cli.py start-proxy &")
        time.sleep(3)  # Give user time to read the message
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print("\nProxy server stopped by user.")
        return True
    except Exception as e:
        print(f"❌ Failed to start proxy server: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Set up and deploy a Hugging Face model with RunpodOllama')
    parser.add_argument('--model', default="llama-3.1-8b-instruct", help='Hugging Face model ID (default: llama-3.1-8b-instruct)')
    parser.add_argument('--disk-size', type=int, default=20, help='Disk size in GB (default: 20)')
    parser.add_argument('--proxy-only', action='store_true', help='Only start the proxy server without creating a new endpoint')
    
    args = parser.parse_args()
    
    # Ensure environment is properly set up
    env_ready = setup_env()
    
    if not env_ready and not args.proxy_only:
        print("Environment not fully configured. You can still start the proxy with --proxy-only.")
        sys.exit(1)
    
    if args.proxy_only:
        start_proxy()
        return
    
    # Create model endpoint
    endpoint_created = create_model_endpoint(args.model, args.disk_size)
    
    if endpoint_created:
        print("\nNow you need to:")
        print("1. Go to your RunPod dashboard: https://www.runpod.io/console/serverless")
        print("2. Find your newly created endpoint")
        print("3. Edit the endpoint to select the appropriate GPU type")
        print("4. Save your changes")
        
        print("\nWould you like to start the proxy server now? (y/n)")
        choice = input().lower()
        if choice == 'y':
            start_proxy()
        else:
            print("\nWhen you're ready to start the proxy server, run:")
            print("python run_cli.py start-proxy")
    
    print("\nTo test your endpoint once the proxy is running, use the following Python code:")
    print("""
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:5000/{your_endpoint_id}/v1",
    api_key="ollama"  # Required but not used
)

response = client.chat.completions.create(
    model="llama-3.1-8b-instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain how quantum computing works."}
    ]
)

print(response.choices[0].message.content)
""")
    print("\nReplace {your_endpoint_id} with the actual endpoint ID from your RunPod dashboard.")

if __name__ == "__main__":
    main() 