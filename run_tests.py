#!/usr/bin/env python3
"""Run the unit tests for every solution, one pytest process per directory.

Each exercise directory is self-contained and imports its modules by flat name
(``from banking_activities import withdraw``), so a name like
``money_transfer_workflow`` means something different in each one. A single
pytest process would import whichever directory it reached first and hand those
modules to the rest, so every directory gets its own process and its own
working directory.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main() -> int:
    directories = sorted(d for d in ROOT.glob("solution*") if any(d.glob("test_*.py")))
    failures = []

    for directory in directories:
        print(f"\n=== {directory.name} ===", flush=True)
        result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=directory)
        if result.returncode != 0:
            failures.append(directory.name)

    if failures:
        print(f"\nFAILED: {', '.join(failures)}")
        return 1

    print(f"\nAll tests passed in {len(directories)} solution directories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
