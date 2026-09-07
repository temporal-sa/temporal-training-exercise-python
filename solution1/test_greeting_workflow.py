import uuid

import pytest
from temporalio import activity
from temporalio.worker import Worker

from greeting_activity import create_greeting
from greeting_workflow import GreetingWorkflow


@activity.defn(name="create_greeting")
async def create_greeting_stub(name: str) -> str:
    """Stand-in for the real activity, registered under the same activity name."""
    return f"Stubbed greeting for {name}"


@pytest.mark.asyncio(loop_scope="session")
async def test_greet_returns_the_activity_result(env):
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[GreetingWorkflow],
        activities=[create_greeting],
    ):
        result = await env.client.execute_workflow(
            GreetingWorkflow.greet,
            "Temporal",
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

    assert result == "Hello, Temporal!"


@pytest.mark.asyncio(loop_scope="session")
async def test_greet_delegates_to_the_activity(env):
    """Swapping the activity for a stub shows the workflow does no formatting itself."""
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[GreetingWorkflow],
        activities=[create_greeting_stub],
    ):
        result = await env.client.execute_workflow(
            GreetingWorkflow.greet,
            "Temporal",
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

    assert result == "Stubbed greeting for Temporal"
