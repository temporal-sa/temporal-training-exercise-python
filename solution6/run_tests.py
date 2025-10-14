#!/usr/bin/env python3
"""Test runner for solution6 unit tests."""

import subprocess
import sys
from pathlib import Path

def main():
    """Run all tests in the solution6 directory."""
    # Change to solution6 directory
    solution_dir = Path(__file__).parent
    
    # Run pytest with verbose output
    cmd = [sys.executable, "-m", "pytest", "-v", "."]
    
    try:
        result = subprocess.run(cmd, cwd=solution_dir, check=True)
        print("\n✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    sys.exit(main())