#!/usr/bin/env python3
"""
Fixes Poetry installation issues by pre-installing problematic packages
with pip and then running Poetry install.

This script is useful for Python 3.12 compatibility.
"""

import os
import sys
import subprocess
import platform

# Python 3.12 compatible packages
BINARY_PACKAGES = [
    "aiohttp==3.9.1",
    "multidict==6.0.4",
    "yarl==1.9.2",
    "frozenlist==1.4.0",
    "aiosignal==1.3.1"
]

def run_command(cmd, shell=False):
    """Run a command and print its output in real-time."""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    
    if shell:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    output = []
    for line in iter(process.stdout.readline, ''):
        if not line:
            break
        print(line.rstrip())
        output.append(line)
    
    process.wait()
    return process.returncode, ''.join(output)

def clean_environment():
    """Clean up existing installation artifacts for a fresh start."""
    print("Cleaning up existing installation artifacts...")
    
    # Remove the poetry.lock file if it exists
    if os.path.exists("poetry.lock"):
        os.remove("poetry.lock")
        print("Removed poetry.lock")
    
    # Clean up any .venv directory
    if os.path.exists(".venv"):
        print("Removing existing .venv directory...")
        if platform.system() == "Windows":
            run_command("rmdir /s /q .venv", shell=True)
        else:
            run_command(["rm", "-rf", ".venv"])

def install_build_dependencies():
    """Install build dependencies for a better environment."""
    print("Installing build dependencies...")
    
    # Install latest pip, setuptools, and wheel
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

def install_binary_packages():
    """Pre-install binary packages to avoid compilation issues."""
    print("Installing binary packages...")
    for package in BINARY_PACKAGES:
        print(f"Installing {package}...")
        run_command([sys.executable, "-m", "pip", "install", package])

def create_py312_compatible_toml():
    """Create a Python 3.12 compatible poetry.toml."""
    print("Creating Python 3.12 compatible poetry.toml...")
    with open("poetry.toml", "w") as f:
        f.write("""[virtualenvs]
in-project = true
create = true
""")

def run_poetry_install():
    """Run poetry install with all extras."""
    print("Running poetry install...")
    run_command(["poetry", "lock", "--no-update"])
    run_command(["poetry", "install", "--all-extras"])

def main():
    """Main function to fix Poetry installation."""
    print("Starting RunpodOllama Poetry installation fix for Python 3.12...")
    
    # Check if Poetry is installed
    returncode, _ = run_command(["poetry", "--version"], shell=True)
    if returncode != 0:
        print("Poetry not found! Installing Poetry...")
        run_command("curl -sSL https://install.python-poetry.org | python3 -", shell=True)
        
        # Add Poetry to PATH if not already there
        poetry_path = os.path.expanduser("~/.local/bin")
        if poetry_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{poetry_path}:{os.environ.get('PATH', '')}"
    
    # Configure Poetry to use the current directory's virtualenv
    run_command(["poetry", "config", "virtualenvs.in-project", "true"])
    
    # Clean the environment
    clean_environment()
    
    # Create a Python 3.12 compatible poetry.toml
    create_py312_compatible_toml()
    
    # Install build dependencies
    install_build_dependencies()
    
    # Install binary packages
    install_binary_packages()
    
    # Run poetry install
    run_poetry_install()
    
    print("\nSetup complete! To run RunpodOllama, use: poetry run runpod-ollama")

if __name__ == "__main__":
    main() 