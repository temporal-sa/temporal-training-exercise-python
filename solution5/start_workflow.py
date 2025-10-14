import asyncio
import time
from temporalio.client import Client

from money_transfer_workflow import MoneyTransferWorkflow
from transfer_request import TransferRequest
from start_worker import TASK_QUEUE


async def main():
    client = await Client.connect("localhost:7233")
    
    workflow_id = f"money-transfer-{int(time.time() * 1000)}"
    
    workflow_handle = await client.start_workflow(
        MoneyTransferWorkflow.transfer,
        TransferRequest(
            from_account="account-123",
            to_account="account-456",
            amount=100.0,
            transfer_id=f"transfer-{int(time.time() * 1000)}"
        ),
        id=workflow_id,
        task_queue=TASK_QUEUE,
    )
    
    print("Starting money transfer workflow...")
    print(f"Workflow ID: {workflow_id}")
    print("Check Temporal Web UI to see activity summaries")
    
    # Query state while waiting for approval
    state = await workflow_handle.query(MoneyTransferWorkflow.get_transfer_state)
    step = await workflow_handle.query(MoneyTransferWorkflow.get_current_step)
    print(f"Before approval - state: {state}, step: {step}")
    
    print("Sending approval signal...")
    await workflow_handle.signal(MoneyTransferWorkflow.approve, True)
    
    # Query approval status
    approved = await workflow_handle.query(MoneyTransferWorkflow.is_approved)
    print(f"Approval status: {approved}")
    
    result = await workflow_handle.result()
    
    # Query final state
    final_state = await workflow_handle.query(MoneyTransferWorkflow.get_transfer_state)
    final_step = await workflow_handle.query(MoneyTransferWorkflow.get_current_step)
    print(f"Final state: {final_state}, step: {final_step}")
    print(f"Transfer result: {result}")


if __name__ == "__main__":
    asyncio.run(main())