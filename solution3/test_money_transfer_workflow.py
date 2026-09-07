import asyncio
import time
import uuid

import pytest
from temporalio import activity
from temporalio.worker import Worker

from money_transfer_workflow import MoneyTransferWorkflow
from transfer_request import TransferRequest

# Stubs registered under the real activity names, so the workflow under test is
# unchanged but never hits the random failures the demo activities simulate.


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


def transfer_request() -> TransferRequest:
    return TransferRequest(
        from_account="account-123",
        to_account="account-456",
        amount=100.0,
        transfer_id=str(uuid.uuid4()),
    )


async def wait_for_step(handle, step: str, timeout: float = 10.0) -> None:
    """Poll the query handler until the workflow reports the expected step."""
    deadline = time.monotonic() + timeout
    while await handle.query(MoneyTransferWorkflow.get_current_step) != step:
        assert time.monotonic() < deadline, f"timed out waiting for step {step}"
        await asyncio.sleep(0.05)


@pytest.mark.asyncio(loop_scope="session")
async def test_queries_report_progress_of_an_approved_transfer(env):
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=ACTIVITY_STUBS,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            transfer_request(),
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        await wait_for_step(handle, "WAITING_FOR_APPROVAL")
        assert await handle.query(MoneyTransferWorkflow.get_transfer_state) == "IN_PROGRESS"
        # No approval yet, so the workflow reports "unknown" rather than False.
        assert await handle.query(MoneyTransferWorkflow.is_approved) is None

        await handle.signal(MoneyTransferWorkflow.approve, True)
        result = await handle.result()

        assert result == "Transfer completed successfully"
        # Queries still work once the workflow has closed.
        assert await handle.query(MoneyTransferWorkflow.get_transfer_state) == "COMPLETED"
        assert await handle.query(MoneyTransferWorkflow.get_current_step) == "COMPLETED"
        assert await handle.query(MoneyTransferWorkflow.is_approved) is True


@pytest.mark.asyncio(loop_scope="session")
async def test_queries_report_progress_of_a_rejected_transfer(env):
    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=ACTIVITY_STUBS,
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            transfer_request(),
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        await wait_for_step(handle, "WAITING_FOR_APPROVAL")
        await handle.signal(MoneyTransferWorkflow.approve, False)
        result = await handle.result()

        assert result == "Transfer rejected and refunded"
        assert await handle.query(MoneyTransferWorkflow.get_transfer_state) == "REJECTED"
        assert await handle.query(MoneyTransferWorkflow.get_current_step) == "REFUNDED"
        assert await handle.query(MoneyTransferWorkflow.is_approved) is False


@pytest.mark.asyncio(loop_scope="session")
async def test_query_observes_the_deposit_in_flight(env):
    """Hold the deposit open so the intermediate step is observable."""
    deposit_started = asyncio.Event()
    let_deposit_finish = asyncio.Event()

    @activity.defn(name="deposit")
    async def blocking_deposit(account: str, amount: float) -> None:
        deposit_started.set()
        await let_deposit_finish.wait()

    task_queue = str(uuid.uuid4())

    async with Worker(
        env.client,
        task_queue=task_queue,
        workflows=[MoneyTransferWorkflow],
        activities=[withdraw_stub, blocking_deposit, refund_stub],
    ):
        handle = await env.client.start_workflow(
            MoneyTransferWorkflow.transfer,
            transfer_request(),
            id=str(uuid.uuid4()),
            task_queue=task_queue,
        )

        await wait_for_step(handle, "WAITING_FOR_APPROVAL")
        await handle.signal(MoneyTransferWorkflow.approve, True)

        await asyncio.wait_for(deposit_started.wait(), timeout=10)
        assert await handle.query(MoneyTransferWorkflow.get_current_step) == "DEPOSITING"
        assert await handle.query(MoneyTransferWorkflow.get_transfer_state) == "IN_PROGRESS"

        let_deposit_finish.set()
        assert await handle.result() == "Transfer completed successfully"
