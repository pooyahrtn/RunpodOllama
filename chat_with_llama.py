#!/usr/bin/env python3
"""
Simple script to chat with the Llama-3.1-8B-Instruct model through the local proxy.
"""

import os
import argparse
from openai import OpenAI

def get_endpoint_id():
    """Prompt user for endpoint ID if not available in environment."""
    endpoint_id = os.environ.get("ENDPOINT_ID")
    
    if not endpoint_id:
        endpoint_id = input("Enter your RunPod endpoint ID: ")
        if not endpoint_id:
            print("No endpoint ID provided. Exiting.")
            exit(1)
    
    return endpoint_id

def main():
    parser = argparse.ArgumentParser(description="Chat with Llama-3.1-8B-Instruct model")
    parser.add_argument("--endpoint", help="RunPod endpoint ID")
    parser.add_argument("--port", type=int, default=5001, help="Local proxy port (default: 5001)")
    parser.add_argument("--system", default="You are a helpful, concise AI assistant.",
                      help="System message for the conversation")
    args = parser.parse_args()
    
    # Get endpoint ID
    endpoint_id = args.endpoint or get_endpoint_id()
    
    # Initialize OpenAI client
    client = OpenAI(
        base_url=f"http://127.0.0.1:{args.port}/{endpoint_id}/v1",
        api_key="ollama"  # Required but not used
    )
    
    print(f"Chat with Llama-3.1-8B-Instruct (endpoint: {endpoint_id})")
    print("Type 'exit' to quit the conversation\n")
    
    # Start with system message
    messages = [
        {"role": "system", "content": args.system}
    ]
    
    # Chat loop
    while True:
        # Get user input
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        # Add user message to conversation
        messages.append({"role": "user", "content": user_input})
        
        # Get response from model
        try:
            print("\nLlama is thinking...")
            response = client.chat.completions.create(
                model="llama-3.1-8b-instruct",
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            
            # Extract and print response
            assistant_response = response.choices[0].message.content
            print(f"\nLlama: {assistant_response}")
            
            # Add assistant message to conversation history
            messages.append({"role": "assistant", "content": assistant_response})
            
        except Exception as e:
            print(f"Error: {e}")
            print("There was an error communicating with the model.")
            print("Make sure the proxy server is running and your endpoint ID is correct.")
    
if __name__ == "__main__":
    main() 