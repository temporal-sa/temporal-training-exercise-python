# Exercise 2 Solution: Money Transfer Workflow with Signals

This solution shows the complete implementation for the remaining TODO items in exercise2.

## banking_activities.py

```python
import random
from temporalio import activity


@activity.defn
async def withdraw(account: str, amount: float) -> None:
    activity.logger.info(f"Withdrawing ${amount} from account {account}")
    if random.random() < 0.1:
        raise RuntimeError("Withdrawal failed - insufficient funds")


@activity.defn
async def deposit(account: str, amount: float) -> None:
    activity.logger.info(f"Depositing ${amount} to account {account}")
    if random.random() < 0.05:
        raise RuntimeError("Deposit failed - account not found")


@activity.defn
async def refund(account: str, amount: float) -> None:
    activity.logger.info(f"Refunding ${amount} to account {account}")
```

## money_transfer_workflow.py

```python
# Complete the __init__ method:
def __init__(self) -> None:
    self.approved = False
    self.approval_received = False

# Add the missing activity executions and wait condition:
# Step 2: Wait for approval
await workflow.wait_condition(lambda: self.approval_received)

# Step 3a: Deposit activity
await workflow.execute_activity(
    deposit,
    args=[request.to_account, request.amount],
    start_to_close_timeout=timedelta(seconds=5),
)

# Step 3b: Refund activity
await workflow.execute_activity(
    refund,
    args=[request.from_account, request.amount],
    start_to_close_timeout=timedelta(seconds=5),
)

# Complete the signal handler:
@workflow.signal
async def approve(self, approved: bool) -> None:
    workflow.logger.info(f"Approval received: {approved}")
    self.approved = approved
    self.approval_received = True
```



## Key Implementation Points

1. **Activities**: Each activity logs operations and includes realistic error simulation
2. **Workflow State**: Uses instance variables to track approval status
3. **Signal Handling**: The `approve` signal updates workflow state to unblock execution
4. **Conditional Logic**: Workflow branches based on approval decision
5. **Error Handling**: Activities can fail and will be automatically retried by Temporal