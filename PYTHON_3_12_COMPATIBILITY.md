# Python 3.12 Compatibility Guide

This document outlines the changes made to ensure RunpodOllama works well with Python 3.12.

## Issues with Python 3.12

Python 3.12 introduced changes that affect C extensions and build processes for certain packages. In particular, the following packages were causing issues:

- `aiohttp`: Relies on C extensions that need updating for Python 3.12
- `multidict`: Has compilation issues with Python 3.12
- `yarl`, `frozenlist`, `aiosignal`: Related dependencies that might have compatibility issues

## Solutions Implemented

We've implemented several solutions to ensure a smooth experience with Python 3.12:

### 1. Binary Installation Script (`install_binary.sh`)

The most reliable method for Python 3.12 users is our new binary installation script. This script:

- Creates a virtual environment
- Installs pre-built binary wheels instead of compiling from source
- Uses specific compatible versions of problematic packages
- Avoids Poetry's build process entirely

### 2. Updated `poetry.toml`

For users who prefer Poetry, we updated the `poetry.toml` configuration:

```toml
[virtualenvs]
in-project = true
create = true
```

This ensures Poetry creates a project-local virtual environment with the correct Python version.

### 3. Python-based Installer Script (`fix_poetry_install.py`)

For cases where the binary installation isn't sufficient, we created a Python-based installer that:

- Pre-installs binary versions of problematic packages
- Configures Poetry correctly
- Creates a clean installation environment

### 4. Updated Package Versions

We updated the dependencies in `pyproject.toml` to use versions known to work with Python 3.12:

- `aiohttp`: Updated to version 3.9.1 (with wheels for Python 3.12)
- Other dependencies updated to compatible versions

### 5. Test Mode

Added a test mode that uses a dummy API token, allowing users to explore the CLI interface without needing a real RunPod API key.

## Recommended Installation for Python 3.12

1. Use the binary installation script: `./install_binary.sh`
2. Activate the virtual environment: `source .venv/bin/activate`
3. Create a `.env` file with your RunPod API key
4. Run the application: `python run_cli.py` or `python -m runpod_ollama`

## Troubleshooting

If you encounter any issues:

1. Make sure you're using the binary installation for Python 3.12
2. Check that your environment variables are set correctly
3. Try running in test mode to verify the CLI functionality
4. If compilation errors persist, try the `fix_poetry_install.py` script

## Technical Details

The primary challenges with Python 3.12 revolve around C extension compatibility:

1. **Deprecated APIs**: Python 3.12 removed or deprecated several C APIs used by extensions
2. **Compilation warnings**: The stricter compiler flags in 3.12 turn warnings into errors
3. **ABI changes**: Changes to Python's Application Binary Interface affect how extensions interact with the interpreter

Our solutions focus on using pre-built binary packages that have already been compiled for Python 3.12, avoiding the need to build these packages from source during installation. 