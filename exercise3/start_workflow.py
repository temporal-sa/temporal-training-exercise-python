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
    
    # TODO: Query workflow state before approval
    # - Query transfer state using get_transfer_state
    # - Query current step using get_current_step
    # - Print the results
    
    print("Sending approval signal...")
    await workflow_handle.signal(MoneyTransferWorkflow.approve, True)
    
    # TODO: Query approval status after sending signal
    # - Query approval status using is_approved
    # - Print the result
    
    result = await workflow_handle.result()
    
    # TODO: Query final workflow state
    # - Query final transfer state
    # - Query final step
    # - Print the results
    
    print(f"Transfer result: {result}")


if __name__ == "__main__":
    asyncio.run(main())