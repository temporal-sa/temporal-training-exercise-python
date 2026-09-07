import asyncio
import time
import uuid

import pytest
from temporalio import activity
from temporalio.client import WorkflowExecutionStatus
from temporalio.worker import Worker

from money_transfer_workflow import MoneyTransferWorkflow
from transfer_request import TransferRequest

# The real activities fail at random, which is useful in a demo and useless in
# a test. These stubs are registered under the same activity names, so the
# workflow code under test is unchanged, and they record what was called.
calls: list[tuple[str, str, float]] = []


@activity.defn(name="withdraw")
async def withdraw_stub(account: str, amount: float) -> None:
    calls.append(("withdraw", account, amount))


@activity.defn(name="deposit")
async def deposit_stub(account: str, amount: float) -> None:
    calls.append(("deposit", account, amount))


@activity.defn(name="refund")
async def refund_stub(account: str, amount: float) -> None:
    calls.append(("refund", account, amount))


ACTIVITY_STUBS = [withdraw_stub, deposit_stub, refund_stub]


@pytest.fixture(autouse=True)
def clear_calls():
    calls.clear()


def transfer_request() -> TransferRequest:
    return TransferRequest(
        from_account="account-123",
        to_account="account-456",
        amount=100.0,
        transfer_id=str(uuid.uuid4()),
    )


async def wait_until(predicate, description: str, timeout: float = 10.0) -> None:
    """Poll until `predicate` holds, so tests never depend on sleep lengths."""
    deadline = time.monotonic() + timeout
    while not predicate():
        assert time.monotonic() < deadline, f"timed out waiting for {description}"
        await asyncio.sleep(0.05)


@pytest.mark.asyncio(loop_scope="session")
async def test_approved_transfer_deposits_into_the_target_account(env):
    task_queue = str(uuid.uuid4())
    request = transfer_request()

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=ACTIVITY_STUBS,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            request,
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        # The workflow withdraws first, then blocks on wait_condition.
        await wait_until(lambda: calls, "the withdrawal")
        assert calls == [("withdraw", request.from_account, request.amount)]
        assert (await handle.describe()).status == WorkflowExecutionStatus.RUNNING

        await handle.signal(MoneyTransferWorkflow.approve, True)
        result = await handle.result()

    assert result == "Transfer completed successfully"
    assert calls == [
        ("withdraw", request.from_account, request.amount),
        ("deposit", request.to_account, request.amount),
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_rejected_transfer_refunds_the_source_account(env):
    task_queue = str(uuid.uuid4())
    request = transfer_request()

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=ACTIVITY_STUBS,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            request,
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        await handle.signal(MoneyTransferWorkflow.approve, False)
        result = await handle.result()

    assert result == "Transfer rejected and refunded"
    assert calls == [
        ("withdraw", request.from_account, request.amount),
        ("refund", request.from_account, request.amount),
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_signal_sent_before_the_wait_is_not_lost(env):
    """A signal that arrives while the withdrawal is still running is buffered.

    The workflow only reaches `wait_condition` after the withdrawal completes,
    yet signalling immediately after start still approves the transfer.
    """
    task_queue = str(uuid.uuid4())
    request = transfer_request()

    handle = await env.client.start_workflow(
        MoneyTransferWorkflow.transfer,
        request,
        id=str(uuid.uuid4()),
        task_queue=task_queue,
    )
    await handle.signal(MoneyTransferWorkflow.approve, True)

    # Only now does a worker pick the workflow up, with the signal already queued.
    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=ACTIVITY_STUBS,
    ):
        result = await handle.result()

    assert result == "Transfer completed successfully"
