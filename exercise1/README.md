# Exercise 1: Hello Temporal (30 min)

## Learning Objectives
- Understand Temporal Workflow and Activity concepts
- Learn how to register workflows and activities with a Worker
- Execute your first Temporal workflow

## Key Concepts

### Workflow
- **@workflow.defn**: Marks a class as a Temporal workflow
- **@workflow.run**: Defines the main workflow entry point
- Workflows orchestrate activities and contain business logic

### Activity
- **@activity.defn**: Marks a function as a Temporal activity
- Activities handle external interactions (API calls, database operations, etc.)

### Worker
- Polls task queues for work
- Executes workflow and activity code
- Must register workflow implementations and activity implementations

## Tasks
1. Complete the activity implementation in `greeting_activity.py`
2. Complete the workflow implementation in `greeting_workflow.py`
3. Complete the worker setup in `start_worker.py`
4. Complete the workflow starter in `start_workflow.py`
5. Run the workflow

## Running the Exercise
1. Start worker: `uv run exercise1/start_worker.py`
2. Execute workflow: `uv run exercise1/start_workflow.py`

## Expected Output
"Hello, Temporal!"

## Solution
Check the `solution1/` directory for the complete implementation.
