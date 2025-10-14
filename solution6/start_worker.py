import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from banking_activities import withdraw, deposit, refund
from money_transfer_workflow import MoneyTransferWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    
    worker = Worker(
        client,
        task_queue="money-transfer-task-queue",
        workflows=[MoneyTransferWorkflow],
        activities=[withdraw, deposit, refund],
    )
    
    print("Worker started, listening on task queue: money-transfer-task-queue")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())