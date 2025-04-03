#!/usr/bin/env python3
"""
Direct CLI runner for RunpodOllama that doesn't rely on Poetry.
"""

import sys
import os

# Add the parent directory to the path so we can import runpod_ollama
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from runpod_ollama import run_cli
    run_cli()
except ImportError as e:
    print(f"Error importing runpod_ollama: {e}")
    print("Make sure you've installed the package with: pip install -e .")
    sys.exit(1)
except Exception as e:
    print(f"Error running CLI: {e}")
    sys.exit(1) 