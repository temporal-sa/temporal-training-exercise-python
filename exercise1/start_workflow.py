import asyncio
from temporalio.client import Client

from greeting_workflow import GreetingWorkflow
from start_worker import TASK_QUEUE


async def main():
    # TODO: Connect to Temporal server at localhost:7233
    client = None  # Replace with client connection
    
    # TODO: Execute the workflow with:
    # - GreetingWorkflow.greet method
    # - "Temporal" as the name parameter
    # - id="greeting-workflow"
    # - task_queue=TASK_QUEUE
    
    # TODO: Print the result
    print("TODO: Print workflow result")


if __name__ == "__main__":
    asyncio.run(main())