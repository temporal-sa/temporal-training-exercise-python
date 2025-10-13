import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from banking_activities import withdraw, deposit, refund
from money_transfer_workflow import MoneyTransferWorkflow

TASK_QUEUE = "MoneyTransferTaskQueue"

interrupt_event = asyncio.Event()

async def main():
    client = await Client.connect("localhost:7233")
    
    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[MoneyTransferWorkflow],
        activities=[withdraw, deposit, refund],
    ):
        print(f"Worker started for task queue: {TASK_QUEUE}")
        await interrupt_event.wait()
        print("Shutting down")


if __name__ == "__main__":
    asyncio.run(main())