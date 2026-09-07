import asyncio
import time
import uuid

import pytest
from temporalio import activity
from temporalio.worker import Worker

import banking_activities
from money_transfer_workflow import MoneyTransferWorkflow
from retry_update import RetryUpdate
from transfer_request import TransferRequest

VALID_FROM = "account-123"
VALID_TO = "account-456"
INVALID = "invalid-account"

# The real activities are deterministic, so the tests use them as-is and only
# wrap them to record what the workflow asked for on each attempt.
calls: list[tuple[str, str, float]] = []


@activity.defn(name="withdraw")
async def withdraw(account: str, amount: float) -> str:
    calls.append(("withdraw", account, amount))
    return await banking_activities.withdraw(account, amount)


@activity.defn(name="deposit")
async def deposit(account: str, amount: float) -> str:
    calls.append(("deposit", account, amount))
    return await banking_activities.deposit(account, amount)


@activity.defn(name="refund")
async def refund(account: str, amount: float) -> str:
    calls.append(("refund", account, amount))
    return await banking_activities.refund(account, amount)


RECORDING_ACTIVITIES = [withdraw, deposit, refund]


@pytest.fixture(autouse=True)
def clear_calls():
    calls.clear()


def transfer_request(from_account: str = VALID_FROM, to_account: str = VALID_TO):
    return TransferRequest(
        from_account=from_account,
        to_account=to_account,
        amount=100.0,
        reference_id=str(uuid.uuid4()),
    )


async def wait_until(predicate, description: str, timeout: float = 10.0) -> None:
    """Poll until `predicate` holds, so tests never depend on sleep lengths."""
    deadline = time.monotonic() + timeout
    while not predicate():
        assert time.monotonic() < deadline, f"timed out waiting for {description}"
        await asyncio.sleep(0.05)


async def wait_for_status(handle, status: str, timeout: float = 10.0) -> None:
    """Poll the status query until the workflow reports the expected status."""
    deadline = time.monotonic() + timeout
    while await handle.query(MoneyTransferWorkflow.get_status) != status:
        assert time.monotonic() < deadline, f"timed out waiting for {status}"
        await asyncio.sleep(0.05)


@pytest.mark.asyncio(loop_scope="session")
async def test_valid_transfer_completes_after_approval(env):
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=RECORDING_ACTIVITIES,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            transfer_request(),
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        await wait_for_status(handle, "IN_PROGRESS")
        assert await handle.query(MoneyTransferWorkflow.is_approved) is False

        await handle.signal(MoneyTransferWorkflow.approve, True)

        assert await handle.result() == "Transfer completed successfully"
        assert await handle.query(MoneyTransferWorkflow.get_status) == "COMPLETED"
        assert await handle.query(MoneyTransferWorkflow.is_approved) is True
        assert calls == [
            ("withdraw", VALID_FROM, 100.0),
            ("deposit", VALID_TO, 100.0),
        ]


@pytest.mark.asyncio(loop_scope="session")
async def test_bad_source_account_parks_the_workflow_until_it_is_corrected(env):
    """A non-retryable failure leaves the workflow waiting, not failed."""
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=RECORDING_ACTIVITIES,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            transfer_request(from_account=INVALID),
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        await wait_for_status(handle, "RETRYING")
        assert calls == [("withdraw", INVALID, 100.0)]

        await handle.signal(
            MoneyTransferWorkflow.retry, RetryUpdate(key="fromAccount", value=VALID_FROM)
        )
        await handle.signal(MoneyTransferWorkflow.approve, True)

        assert await handle.result() == "Transfer completed successfully"
        assert calls == [
            ("withdraw", INVALID, 100.0),
            ("withdraw", VALID_FROM, 100.0),
            ("deposit", VALID_TO, 100.0),
        ]


@pytest.mark.asyncio(loop_scope="session")
async def test_bad_target_account_is_corrected_after_approval(env):
    """The deposit is behind the approval gate, so its retry happens later."""
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=RECORDING_ACTIVITIES,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            transfer_request(to_account=INVALID),
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        await handle.signal(MoneyTransferWorkflow.approve, True)
        await wait_for_status(handle, "RETRYING")
        assert calls == [
            ("withdraw", VALID_FROM, 100.0),
            ("deposit", INVALID, 100.0),
        ]

        await handle.signal(
            MoneyTransferWorkflow.retry, RetryUpdate(key="toAccount", value=VALID_TO)
        )

        assert await handle.result() == "Transfer completed successfully"
        assert calls[-1] == ("deposit", VALID_TO, 100.0)


@pytest.mark.asyncio(loop_scope="session")
async def test_retry_signal_can_correct_the_amount_and_repeat(env):
    """An unhelpful correction just retries; the workflow keeps waiting."""
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=RECORDING_ACTIVITIES,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            transfer_request(from_account=INVALID),
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        await wait_for_status(handle, "RETRYING")

        # Fixing the amount does not fix the account, so withdraw fails again.
        # The status is already RETRYING, so wait on the second attempt itself.
        await handle.signal(
            MoneyTransferWorkflow.retry, RetryUpdate(key="amount", value="250")
        )
        await wait_until(lambda: len(calls) == 2, "the second withdrawal attempt")
        await wait_for_status(handle, "RETRYING")
        assert calls == [
            ("withdraw", INVALID, 100.0),
            ("withdraw", INVALID, 250.0),
        ]

        await handle.signal(
            MoneyTransferWorkflow.retry, RetryUpdate(key="fromAccount", value=VALID_FROM)
        )
        await handle.signal(MoneyTransferWorkflow.approve, True)

        assert await handle.result() == "Transfer completed successfully"
        assert calls[-2:] == [
            ("withdraw", VALID_FROM, 250.0),
            ("deposit", VALID_TO, 250.0),
        ]
