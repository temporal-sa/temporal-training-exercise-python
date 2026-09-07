"""Shared pytest setup for the solution8 tests.

The exercise modules import each other by flat module name (for example
``from banking_activities import withdraw``) so that ``start_worker.py`` can
run as a plain script. Putting this directory on ``sys.path`` lets the tests
import them the same way regardless of where pytest is invoked from.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
