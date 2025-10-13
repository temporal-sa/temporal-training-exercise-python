# Exercise 3 Solution: Money Transfer Workflow with Queries

## Overview

This exercise demonstrates how to add query capabilities to Temporal workflows for real-time state monitoring.

## Key Implementation Points

### 1. State Tracking Variables

Add state tracking in the workflow constructor:

```python
def __init__(self) -> None:
    self.approved = False
    self.approval_received = False
    self.transfer_state = "PENDING"
    self.current_step = "INITIALIZED"
```

### 2. State Updates Throughout Workflow

Update state at each step:

```python
# At start of transfer
self.transfer_state = "IN_PROGRESS"
self.current_step = "WITHDRAWING"

# After withdrawal
self.current_step = "WAITING_FOR_APPROVAL"

# During processing
self.current_step = "DEPOSITING"  # or "REFUNDING"

# At completion
self.transfer_state = "COMPLETED"  # or "REJECTED"
self.current_step = "COMPLETED"    # or "REFUNDED"
```

### 3. Query Methods

Implement the query method bodies (decorators are already provided):

```python
@workflow.query
def get_transfer_state(self) -> str:
    return self.transfer_state

@workflow.query
def get_current_step(self) -> str:
    return self.current_step

@workflow.query
def is_approved(self) -> bool:
    return self.approved if self.approval_received else None
```

### 4. Client Query Calls

Query workflow state from the client:

```python
# Before approval
state = await workflow_handle.query(MoneyTransferWorkflow.get_transfer_state)
step = await workflow_handle.query(MoneyTransferWorkflow.get_current_step)
print(f"Before approval - state: {state}, step: {step}")

# After signal
approved = await workflow_handle.query(MoneyTransferWorkflow.is_approved)
print(f"Approval status: {approved}")

# Final state
final_state = await workflow_handle.query(MoneyTransferWorkflow.get_transfer_state)
final_step = await workflow_handle.query(MoneyTransferWorkflow.get_current_step)
print(f"Final state: {final_state}, step: {final_step}")
```

## Key Concepts Learned

- **Queries vs Signals**: Queries are read-only, signals modify state
- **State Management**: Tracking workflow progress through variables
- **Real-time Monitoring**: Querying running workflows for status
- **Workflow Introspection**: External visibility into workflow execution

## Expected Output

```
Starting money transfer workflow...
Before approval - state: IN_PROGRESS, step: WAITING_FOR_APPROVAL
Sending approval signal...
Approval status: True
Final state: COMPLETED, step: COMPLETED
Transfer result: Transfer completed successfully
```

## Complete Solution

Check the `solution3/` directory for the complete implementation.