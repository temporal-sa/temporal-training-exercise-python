import pytest
from temporalio.testing import ActivityEnvironment

from greeting_activity import create_greeting


@pytest.mark.asyncio
async def test_create_greeting():
    """ActivityEnvironment runs an activity on its own, with no server."""
    result = await ActivityEnvironment().run(create_greeting, "Temporal")

    assert result == "Hello, Temporal!"


@pytest.mark.asyncio
async def test_create_greeting_uses_the_name_it_is_given():
    result = await ActivityEnvironment().run(create_greeting, "Alice")

    assert result == "Hello, Alice!"
