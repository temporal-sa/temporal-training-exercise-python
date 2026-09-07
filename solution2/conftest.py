"""Shared pytest setup for the solution2 tests.

The exercise modules import each other by flat module name (for example
``from banking_activities import withdraw``) so that ``start_worker.py`` can
run as a plain script. Putting this directory on ``sys.path`` lets the tests
import them the same way regardless of where pytest is invoked from.
"""

import sys
from pathlib import Path

import pytest_asyncio
from temporalio.testing import WorkflowEnvironment

sys.path.insert(0, str(Path(__file__).parent))


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def env():
    """A local Temporal server shared by every workflow test in this directory.

    Starting a server takes a few seconds, so it is worth sharing. Each test
    still gets its own task queue and workflow id so they cannot collide.
    """
    async with await WorkflowEnvironment.start_local() as environment:
        yield environment
