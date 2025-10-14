import asyncio
import uuid
from temporalio.client import Client

from money_transfer_workflow import MoneyTransferWorkflow
from transfer_request import TransferRequest


async def main():
    client = await Client.connect("localhost:7233")
    
    # Create transfer request
    request = TransferRequest(
        from_account="account-001",
        to_account="invalid-account-002",
        amount=100.0,
        reference_id=str(uuid.uuid4())
    )
    
    # Start workflow
    workflow_id = f"money-transfer-{request.reference_id}"
    await client.start_workflow(
        MoneyTransferWorkflow.transfer,
        request,
        id=workflow_id,
        task_queue="money-transfer-task-queue",
    )
    
    print(f"Started workflow: {workflow_id}")


if __name__ == "__main__":
    asyncio.run(main())
