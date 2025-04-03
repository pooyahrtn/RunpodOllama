#!/bin/bash

echo "Setting up Poetry for RunpodOllama..."

# Install Poetry if not installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    # Add Poetry to PATH
    export PATH="$HOME/.local/bin:$PATH"
fi

# First cleanup any existing lock files to ensure a fresh start
rm -f poetry.lock

# Configure Poetry to use the current directory's virtualenv
poetry config virtualenvs.in-project true

# Generate a fresh lock file with the updated dependencies
echo "Generating a new Poetry lock file..."
poetry lock --no-update

# Install dependencies
echo "Installing dependencies with Poetry..."
poetry install --all-extras

echo "Setup complete! To run RunpodOllama, use: poetry run runpod-ollama" 