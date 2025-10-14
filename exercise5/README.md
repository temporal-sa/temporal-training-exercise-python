# Exercise 5: User Metadata & Activity Summaries

This exercise demonstrates how to add user metadata and activity summaries to improve workflow observability in the Temporal Web UI.

## Scenario

Enhance the money transfer workflow with:
- Activity summaries providing context for each activity execution

## Learning Objectives

- Implement activity summaries for runtime context
- Improve workflow observability and debugging capabilities
- Understand metadata best practices

## Tasks

Complete the TODO items in the following files:

1. `money_transfer_workflow.py` - Add activity summaries to activity options

Note: Activity and query implementations are already complete from previous exercises.

## Running the Exercise

1. Start the worker:
   ```bash
   uv run exercise5/start_worker.py
   ```

2. In another terminal, start the workflow:
   ```bash
   uv run exercise5/start_workflow.py
   ```

3. Check the Temporal Web UI to see the summaries in action

## Key Concepts

- **Activity Summary**: Provides runtime context for each activity execution
- **Observability**: Both summaries appear in Temporal Web UI for monitoring
- **Metadata**: Additional information to help with debugging and operations

## Expected Behavior

- Each activity shows contextual summary during execution
- Improved visibility into workflow purpose and progress