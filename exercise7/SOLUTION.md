# Exercise 7 Solution: Manual Activity Retry

## Overview
This exercise demonstrates how to implement manual retry patterns for activities that fail due to invalid data, requiring human intervention before retry.

## Key Concepts

### Manual Retry Pattern
- Disable automatic retries for specific failure types
- Use signals to trigger manual retries after data correction
- Handle non-retryable failures gracefully

### Implementation Details

#### 1. Non-Retryable Failures
Activities throw `ApplicationError` with `non_retryable=True` for invalid data:
```python
if "invalid" in account:
    raise ApplicationError(
        f"Invalid account ID: {account}",
        type="InvalidAccount",
        non_retryable=True,
    )
```

#### 2. Execute with Retry Pattern
Workflow uses a retry loop that waits for manual intervention:
```python
async def _execute_with_manual_retry(self, operation):
    while True:
        try:
            return await operation()
        except ActivityError:
            self.status = TransferStatus.RETRYING
            self.retry_requested = False
            await workflow.wait_condition(lambda: self.retry_requested)
```

#### 3. Signal Handler for Updates
Retry signal updates request data dynamically:
```python
@workflow.signal
async def retry(self, update: RetryUpdate) -> None:
    if update.key == "fromAccount":
        self.request.from_account = update.value
    elif update.key == "toAccount":
        self.request.to_account = update.value
    elif update.key == "amount":
        self.request.amount = float(update.value)
    self.retry_requested = True
```

## Running the Exercise

1. Start worker:
```bash
uv run exercise7/start_worker.py
```

2. Run workflow with invalid account:
```bash
uv run exercise7/start_workflow.py
```

3. Send retry signal with corrected data:
```bash
temporal workflow signal \
  --workflow-id <workflow-id> \
  --name retry \
  --input '{"key":"toAccount","value":"account-456"}'
```

## Expected Behavior

1. Workflow starts with invalid account data
2. Activity fails with non-retryable error
3. Workflow waits for manual intervention
4. Admin corrects data and sends retry signal
5. Workflow retries with corrected data and completes

## Key Benefits

- Handles data validation failures gracefully
- Allows human intervention for complex error scenarios
- Maintains workflow state during correction process
- Provides clear audit trail of retry attempts