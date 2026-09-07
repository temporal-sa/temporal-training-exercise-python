import asyncio
import time
import uuid

import pytest
from temporalio import activity
from temporalio.common import SearchAttributeKey
from temporalio.worker import Worker

from money_transfer_workflow import MoneyTransferWorkflow
from transfer_request import TransferRequest

# The same attribute the workflow upserts; conftest registers it on the server.
ACCOUNT_ID = SearchAttributeKey.for_keyword("AccountId")


@activity.defn(name="withdraw")
async def withdraw_stub(account: str, amount: float) -> None:
    pass


@activity.defn(name="deposit")
async def deposit_stub(account: str, amount: float) -> None:
    pass


@activity.defn(name="refund")
async def refund_stub(account: str, amount: float) -> None:
    pass


ACTIVITY_STUBS = [withdraw_stub, deposit_stub, refund_stub]


def transfer_request(from_account: str) -> TransferRequest:
    return TransferRequest(
        from_account=from_account,
        to_account="account-456",
        amount=100.0,
        transfer_id=str(uuid.uuid4()),
    )


async def run_transfer(env, task_queue: str, from_account: str) -> str:
    """Start a transfer, approve it, and return the workflow id."""
    handle = await env.client.start_workflow(
        MoneyTransferWorkflow.transfer,
        transfer_request(from_account),
        id=str(uuid.uuid4()),
        task_queue=task_queue,
    )
    await handle.signal(MoneyTransferWorkflow.approve, True)
    assert await handle.result() == "Transfer completed successfully"
    return handle.id


async def wait_for_ids(env, query: str, expected: set[str], timeout: float = 10.0):
    """Visibility is eventually consistent, so poll until the index catches up."""
    deadline = time.monotonic() + timeout
    while True:
        found = {wf.id async for wf in env.client.list_workflows(query)}
        if expected <= found:
            return found
        assert time.monotonic() < deadline, f"timed out waiting for {query}"
        await asyncio.sleep(0.1)


@pytest.mark.asyncio(loop_scope="session")
async def test_transfer_tags_itself_with_the_source_account(env):
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=ACTIVITY_STUBS,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            transfer_request("account-123"),
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        # The attribute is set before the first activity, so it is visible on a
        # running workflow rather than only on a completed one.
        await wait_for_ids(env, 'AccountId = "account-123"', {handle.id})

        description = await handle.describe()
        assert description.typed_search_attributes[ACCOUNT_ID] == "account-123"

        await handle.signal(MoneyTransferWorkflow.approve, True)
        assert await handle.result() == "Transfer completed successfully"


@pytest.mark.asyncio(loop_scope="session")
async def test_workflows_are_filterable_by_account(env):
    """The point of the search attribute: find one account's transfers only."""
    task_queue = str(uuid.uuid4())
    account_a = f"account-{uuid.uuid4()}"
    account_b = f"account-{uuid.uuid4()}"

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=ACTIVITY_STUBS,
    ):
        first_a = await run_transfer(env, task_queue, account_a)
        second_a = await run_transfer(env, task_queue, account_a)
        only_b = await run_transfer(env, task_queue, account_b)

    matches_a = await wait_for_ids(
        env, f'AccountId = "{account_a}"', {first_a, second_a}
    )
    assert matches_a == {first_a, second_a}
    assert only_b not in matches_a

    matches_b = await wait_for_ids(env, f'AccountId = "{account_b}"', {only_b})
    assert matches_b == {only_b}
