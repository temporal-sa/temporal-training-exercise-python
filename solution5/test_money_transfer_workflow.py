import uuid

import pytest
from temporalio import activity
from temporalio.api.enums.v1 import EventType
from temporalio.client import Client, WorkflowHandle
from temporalio.worker import Worker

from money_transfer_workflow import MoneyTransferWorkflow
from transfer_request import TransferRequest

FROM_ACCOUNT = "account-123"
TO_ACCOUNT = "account-456"


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
        from_account=FROM_ACCOUNT,
        to_account=TO_ACCOUNT,
        amount=100.0,
        transfer_id=str(uuid.uuid4()),
    )


async def activity_summaries(client: Client, handle: WorkflowHandle) -> list[str]:
    """The summaries the Web UI shows, read straight out of event history.

    A summary rides along on the ActivityTaskScheduled event as user metadata,
    so asserting on it needs the history rather than the workflow result.
    """
    converter = client.data_converter.payload_converter
    history = await handle.fetch_history()
    return [
        converter.from_payload(event.user_metadata.summary, str)
        for event in history.events
        if event.event_type == EventType.EVENT_TYPE_ACTIVITY_TASK_SCHEDULED
        and event.HasField("user_metadata")
        and event.user_metadata.HasField("summary")
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_approved_transfer_summarizes_withdrawal_and_deposit(env):
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
        await handle.signal(MoneyTransferWorkflow.approve, True)

        assert await handle.result() == "Transfer completed successfully"
        assert await activity_summaries(env.client, handle) == [
            f"Withdrawing funds from account {FROM_ACCOUNT}",
            f"Depositing funds to account {TO_ACCOUNT}",
        ]


@pytest.mark.asyncio(loop_scope="session")
async def test_rejected_transfer_summarizes_the_refund(env):
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
        await handle.signal(MoneyTransferWorkflow.approve, False)

        assert await handle.result() == "Transfer rejected and refunded"
        assert await activity_summaries(env.client, handle) == [
            f"Withdrawing funds from account {FROM_ACCOUNT}",
            f"Refunding funds to account {FROM_ACCOUNT}",
        ]


@pytest.mark.asyncio(loop_scope="session")
async def test_summaries_do_not_change_the_workflow_behaviour(env):
    """Summaries are metadata only: queries still report the same states."""
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
        await handle.signal(MoneyTransferWorkflow.approve, True)
        await handle.result()

        assert await handle.query(MoneyTransferWorkflow.get_transfer_state) == "COMPLETED"
        assert await handle.query(MoneyTransferWorkflow.get_current_step) == "COMPLETED"
        assert await handle.query(MoneyTransferWorkflow.is_approved) is True
