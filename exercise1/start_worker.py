import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from greeting_activity import create_greeting
from greeting_workflow import GreetingWorkflow

TASK_QUEUE = "hello-task-queue"

interrupt_event = asyncio.Event()

async def main():
    # TODO: Connect to Temporal server at localhost:7233
    client = None  # Replace with client connection
    
    # TODO: Create a Worker with:
    # - The client
    # - task_queue set to TASK_QUEUE
    # - workflows list containing GreetingWorkflow
    # - activities list containing create_greeting
    
    # TODO: Start the worker and wait for interruption
    print("Worker started, ctrl+c to exit")
    await interrupt_event.wait()
    print("Shutting down")


if __name__ == "__main__":
    asyncio.run(main())