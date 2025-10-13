import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from greeting_activity import create_greeting
from greeting_workflow import GreetingWorkflow

TASK_QUEUE = "hello-task-queue"

interrupt_event = asyncio.Event()

async def main():
    client = await Client.connect("localhost:7233")
    
    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[GreetingWorkflow],
        activities=[create_greeting],
    ):
        # Wait until interrupted
        print("Worker started, ctrl+c to exit")
        await interrupt_event.wait()
        print("Shutting down")


if __name__ == "__main__":
    asyncio.run(main())
