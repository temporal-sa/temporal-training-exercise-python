# Exercise 1 Solutions

## greeting_activity.py
```python
@activity.defn
async def create_greeting(name: str) -> str:
    return f"Hello, {name}!"
```

## greeting_workflow.py
```python
@workflow.run
async def greet(self, name: str) -> str:
    return await workflow.execute_activity(
        create_greeting,
        name,
        start_to_close_timeout=timedelta(seconds=5),
    )
```

## start_worker.py
```python
async def main():
    client = await Client.connect("localhost:7233")
    
    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[GreetingWorkflow],
        activities=[create_greeting],
    ):
        print("Worker started, ctrl+c to exit")
        await interrupt_event.wait()
        print("Shutting down")
```

## start_workflow.py
```python
async def main():
    client = await Client.connect("localhost:7233")
    
    result = await client.execute_workflow(
        GreetingWorkflow.greet,
        "Temporal",
        id="greeting-workflow",
        task_queue=TASK_QUEUE,
    )
    
    print(result)
```

## Running the Exercise
1. Start worker: `uv run exercise1/start_worker.py`
2. Execute workflow: `uv run exercise1/start_workflow.py`
