# Exercise 3: Money Transfer Workflow with Queries

This exercise extends the money transfer workflow by adding query capabilities to monitor workflow state and progress.

## Scenario

Building on Exercise 2, you'll add query methods to track:
- Transfer state (PENDING, IN_PROGRESS, COMPLETED, REJECTED)
- Current step in the process
- Approval status

## Learning Objectives

- Implement Temporal queries to expose workflow state
- Track workflow progress through different states
- Query workflow state from external clients
- Understand the difference between signals and queries

## Tasks

Complete the TODO items in the following files:

1. `money_transfer_workflow.py` - Implement state tracking variables and query method bodies
2. `start_workflow.py` - Add query calls to monitor workflow progress

Note: Query method signatures are provided - implement the method bodies.

## Running the Exercise

1. Start the worker:
   ```bash
   uv run exercise3/start_worker.py
   ```

2. In another terminal, start the workflow:
   ```bash
   uv run exercise3/start_workflow.py
   ```

## Key Concepts

- **Queries**: Read-only operations to inspect workflow state
- **State Management**: Tracking workflow progress through different phases
- **Real-time Monitoring**: Querying workflow state while it's running
- **Workflow Introspection**: Understanding workflow execution from outside

## Expected Output

The workflow should display state transitions and allow querying of:
- Transfer state at different points
- Current processing step
- Approval status after signal is sent