import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from banking_activities import withdraw, deposit, refund
from money_transfer_workflow import MoneyTransferWorkflow

TASK_QUEUE = "money-transfer-task-queue"


async def main():
    client = await Client.connect("localhost:7233")
    
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[MoneyTransferWorkflow],
        activities=[withdraw, deposit, refund],
    )
    
    print("Starting worker...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())