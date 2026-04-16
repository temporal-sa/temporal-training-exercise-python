import json
import os
import pytest
from temporalio.client import WorkflowHistory
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Replayer, Worker

from money_transfer_workflow import MoneyTransferWorkflow
from transfer_request import TransferRequest
from banking_activities import withdraw, deposit, refund
# TODO: Task 1 - Import send_notification


@pytest.mark.asyncio
async def test_new_workflow_with_notification():
    """Test that new workflow executes with notification."""
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-queue",
            workflows=[MoneyTransferWorkflow],
            activities=[withdraw, deposit, refund],
            # TODO: Task 1 - Add send_notification to activities list
        ):
            request = TransferRequest(
                from_account="account-123",
                to_account="account-456",
                amount=100.0,
                reference_id="transfer-1",
            )

            handle = await env.client.start_workflow(
                MoneyTransferWorkflow.transfer,
                request,
                id=f"test-transfer-{request.reference_id}",
                task_queue="test-queue",
            )

            await handle.signal(MoneyTransferWorkflow.approve, True)
            result = await handle.result()
            assert result == "Transfer completed successfully"


# TODO: Task 3 - Add replay test
# @pytest.mark.asyncio
# async def test_replay_old_workflow_history():
#     """Replay old workflow history (without notification) against new code."""
#     history_path = os.path.join(os.path.dirname(__file__), "workflow_history_v1.json")
#     with open(history_path, "r") as f:
#         history_json = json.load(f)
#
#     replayer = Replayer(workflows=[MoneyTransferWorkflow])
#     await replayer.replay_workflow(
#         WorkflowHistory.from_json("money-transfer-workflow", history_json)
#     )
