#!/bin/bash
set -e

# Function to handle cleanup on exit
cleanup() {
    echo "Received exit signal. Cleaning up..."

    # Kill the background processes
    kill "$pid1" "$pid2"

    # Wait for both processes to exit
    wait "$pid1" "$pid2"

    echo "Cleanup complete. Exiting."
    exit
}

# Register the cleanup function to be called on exit
trap cleanup EXIT

poetry run run_proxy &
pid1=$!

litellm --config $PWD/../runpod_ollama/litellm/config.yaml &
pid2=$!

# Keep the script running
echo "Script is running. Press Ctrl+C to exit."

# Wait for the exit signal
wait
