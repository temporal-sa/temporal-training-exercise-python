import pytest
from unittest.mock import patch
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from .money_transfer_workflow import MoneyTransferWorkflow
from .banking_activities import withdraw, deposit, refund
from .transfer_request import TransferRequest


class TestMoneyTransferWorkflow:
    
    @pytest.mark.asyncio
    async def test_approved_transfer(self):
        """Test successful transfer with approval"""
        env = await WorkflowEnvironment.start_time_skipping()
        async with env:
            task_queue = "test-queue"
            
            async with Worker(
                env.client,
                task_queue=task_queue,
                workflows=[MoneyTransferWorkflow],
                activities=[withdraw, deposit, refund]
            ):
                request = TransferRequest(
                    from_account="account-001",
                    to_account="account-002",
                    amount=100.0,
                    transfer_id="test-001"
                )
                
                with patch('random.random', return_value=1):
                    handle = await env.client.start_workflow(
                        MoneyTransferWorkflow.transfer,
                        request,
                        id="test-workflow-approved",
                        task_queue=task_queue
                    )
                    
                    # Test initial state
                    state = await handle.query(MoneyTransferWorkflow.get_transfer_state)
                    assert state == "IN_PROGRESS"
                    
                    await handle.signal(MoneyTransferWorkflow.approve, True)
                    result = await handle.result()
                    
                    # Test final state
                    final_state = await handle.query(MoneyTransferWorkflow.get_transfer_state)
                    assert final_state == "COMPLETED"
                    
                    assert result == "Transfer completed successfully"
    
    @pytest.mark.asyncio
    async def test_rejected_transfer_queries(self):
        """Test query values during rejected transfer"""
        env = await WorkflowEnvironment.start_time_skipping()
        async with env:
            task_queue = "test-queue"
            
            async with Worker(
                env.client,
                task_queue=task_queue,
                workflows=[MoneyTransferWorkflow],
                activities=[withdraw, deposit, refund]
            ):
                request = TransferRequest(
                    from_account="account-001",
                    to_account="account-002",
                    amount=100.0,
                    transfer_id="test-002"
                )
                
                with patch('random.random', return_value=1):
                    handle = await env.client.start_workflow(
                        MoneyTransferWorkflow.transfer,
                        request,
                        id="test-workflow-rejected",
                        task_queue=task_queue
                    )
                    
                    # Check state before approval
                    state = await handle.query(MoneyTransferWorkflow.get_transfer_state)
                    assert state == "IN_PROGRESS"
                    
                    await handle.signal(MoneyTransferWorkflow.approve, False)
                    result = await handle.result()
                    
                    # Check final state after rejection
                    final_state = await handle.query(MoneyTransferWorkflow.get_transfer_state)
                    assert final_state == "REJECTED"
                    
                    final_step = await handle.query(MoneyTransferWorkflow.get_current_step)
                    assert final_step == "REFUNDED"
                    
                    assert result == "Transfer rejected and refunded"
