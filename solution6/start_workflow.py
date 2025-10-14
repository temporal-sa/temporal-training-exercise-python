import asyncio
import uuid
from temporalio.client import Client

from money_transfer_workflow import MoneyTransferWorkflow
from transfer_request import TransferRequest


async def main():
    client = await Client.connect("localhost:7233")
    
    transfer_id = str(uuid.uuid4())
    request = TransferRequest(
        from_account="account-001",
        to_account="account-002", 
        amount=100.0,
        transfer_id=transfer_id
    )
    
    handle = await client.start_workflow(
        MoneyTransferWorkflow.transfer,
        request,
        id=f"money-transfer-{transfer_id}",
        task_queue="money-transfer-task-queue",
        search_attributes={"AccountId": [request.from_account]}
    )
    
    print(f"Started workflow with ID: {handle.id}")
    
    # Send approval after a short delay
    await asyncio.sleep(2)
    await handle.signal(MoneyTransferWorkflow.approve, True)
    print("Sent approval signal")
    
    result = await handle.result()
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())