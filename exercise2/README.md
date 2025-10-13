# Exercise 2: Money Transfer Workflow with Signals

This exercise demonstrates a more complex workflow that uses Temporal signals for human-in-the-loop approval processes.

## Scenario

You're building a money transfer system that requires approval for transactions. The workflow:

1. Withdraws money from the source account
2. Waits for human approval via a signal
3. If approved: deposits money to the target account
4. If rejected: refunds money to the source account

## Learning Objectives

- Implement Temporal activities with error handling
- Create workflows that wait for external signals
- Handle conditional logic based on signal data
- Use workflow state to track approval status

## Tasks

Complete the TODO items in the following files:

1. `banking_activities.py` - Implement withdraw, deposit, and refund activities with logging and error simulation
2. `money_transfer_workflow.py` - Complete the workflow logic with signal handling and activity execution
3. `start_workflow.py` - Implement signal sending to approve the transfer

Note: `transfer_request.py` and `start_worker.py` are already implemented for you.

## Running the Exercise

1. Start the worker:
   ```bash
   uv run exercise2/start_worker.py
   ```

2. In another terminal, start the workflow:
   ```bash
   uv run exercise2/start_workflow.py
   ```

## Key Concepts

- **Signals**: External events that can modify workflow state
- **Conditions**: Waiting for specific state changes in workflows
- **Activity Retries**: Temporal automatically retries failed activities
- **Workflow State**: Maintaining state across workflow execution
