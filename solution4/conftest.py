"""Shared pytest setup for the solution4 tests.

The exercise modules import each other by flat module name (for example
``from banking_activities import withdraw``) so that ``start_worker.py`` can
run as a plain script. Putting this directory on ``sys.path`` lets the tests
import them the same way regardless of where pytest is invoked from.
"""

import sys
from pathlib import Path

import pytest_asyncio
from temporalio.common import SearchAttributeKey
from temporalio.testing import WorkflowEnvironment

sys.path.insert(0, str(Path(__file__).parent))

# Matches the attribute name the workflow upserts.
ACCOUNT_ID = SearchAttributeKey.for_keyword("AccountId")


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def env():
    """A local Temporal server shared by every workflow test in this directory.

    Starting a server takes a few seconds, so it is worth sharing. Each test
    still gets its own task queue and workflow id so they cannot collide.
    """
    # The workflow upserts AccountId, so the attribute has to exist on the
    # server before a workflow can set it. A real deployment registers it once
    # with `temporal operator search-attribute create`.
    async with await WorkflowEnvironment.start_local(
        search_attributes=[ACCOUNT_ID],
    ) as environment:
        yield environment
