import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from banking_activities import withdraw, deposit, refund
# TODO: Task 1 - Import send_notification
from money_transfer_workflow import MoneyTransferWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="money-transfer-task-queue",
        workflows=[MoneyTransferWorkflow],
        activities=[withdraw, deposit, refund],
        # TODO: Task 1 - Add send_notification to activities list
    )

    print("Worker started. Ctrl+C to exit.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
