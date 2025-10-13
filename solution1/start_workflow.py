import asyncio
from temporalio.client import Client

from greeting_workflow import GreetingWorkflow
from start_worker import TASK_QUEUE


async def main():
    client = await Client.connect("localhost:7233")
    
    result = await client.execute_workflow(
        GreetingWorkflow.greet,
        "Temporal",
        id="greeting-workflow",
        task_queue=TASK_QUEUE,
    )
    
    print(result)


if __name__ == "__main__":
    asyncio.run(main())