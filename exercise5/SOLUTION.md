# Exercise 5 Solution: User Metadata & Activity Summaries

## Overview

This exercise demonstrates how to add user metadata and activity summaries to improve workflow observability in the Temporal Web UI.

## Key Implementation Points

### 1. Activity Summaries

Add summary parameter to each activity execution:

```python
# Withdraw activity
await workflow.execute_activity(
    withdraw,
    args=[request.from_account, request.amount],
    start_to_close_timeout=timedelta(seconds=5),
    summary=f"Withdrawing funds from account {request.from_account}",
)

# Deposit activity
await workflow.execute_activity(
    deposit,
    args=[request.to_account, request.amount],
    start_to_close_timeout=timedelta(seconds=5),
    summary=f"Depositing funds to account {request.to_account}",
)

# Refund activity
await workflow.execute_activity(
    refund,
    args=[request.from_account, request.amount],
    start_to_close_timeout=timedelta(seconds=5),
    summary=f"Refunding funds to account {request.from_account}",
)
```



## Key Concepts Learned

- **Activity Summary**: Provides runtime context for each activity execution
- **Observability**: Summaries appear in Temporal Web UI for better monitoring
- **Best Practice**: Use descriptive, contextual summaries that help with debugging

## Expected Behavior

- Each activity shows contextual summary during execution
- Improved visibility into activity context
- Better debugging and monitoring capabilities

## Complete Solution

Check the `solution5/` directory for the complete implementation.