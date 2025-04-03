#!/bin/bash

echo "Setting up RunpodOllama with binary packages..."

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies with specific binary packages
echo "Installing dependencies..."
pip install --upgrade pip wheel setuptools

# Install specific binary packages
pip install aiohttp==3.9.1
pip install multidict==6.0.4 yarl==1.9.2 frozenlist==1.4.0 aiosignal==1.3.1

# Install other primary dependencies
pip install flask==3.0.0 requests==2.31.0 python-dotenv==1.0.0
pip install types-requests==2.31.0.20240125 typer==0.9.0 rich==13.7.0 inquirer==3.2.3
pip install runpod==1.5.3

# Install litellm with proxy extras
pip install "litellm[proxy]==1.20.2"

# Install example dependencies
pip install openai==1.10.0 langchain-community==0.0.16 langchain==0.1.4

# Install the package in development mode
pip install -e .

echo "Setup complete! To use RunpodOllama, first activate the virtual environment:"
echo "source .venv/bin/activate"
echo "Then run: python -m runpod_ollama or python run_cli.py" 