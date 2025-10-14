# Exercise 7: Manual Activity Retry

## Objective
Learn how to implement manual retry patterns using signals when automatic retries are insufficient for handling invalid data scenarios.

## Key Concepts
- Disabling automatic activity retries
- Manual retry pattern using signals
- Interactive error correction
- Dynamic request updates during workflow execution

## What You'll Implement

### 1. Manual Retry Logic
Implement the `_execute_with_manual_retry` method that:
- Executes operations in a loop
- Waits for retry signal before continuing

### 2. Signal Handlers
- `retry()`: Handle retry signals with updated data (fromAccount, toAccount, amount)

## Testing the Exercise

1. Start the worker:
```bash
uv run exercise7/start_worker.py
```

2. Run the workflow (uses invalid account to trigger retry):
```bash
uv run exercise7/start_workflow.py
```

3. Use Temporal CLI to interact with the workflow:

Send approval:
```bash
temporal workflow signal \
  --workflow-id <workflow-id> \
  --name approve \
  --input true
```

Retry with corrected data:
```bash
temporal workflow signal \
  --workflow-id <workflow-id> \
  --name retry \
  --input '{"key":"toAccount","value":"account-456"}'
```

## Expected Behavior
1. Workflow starts and attempts withdrawal (succeeds)
2. Workflow waits for approval signal
3. After approval, attempts deposit with invalid account (fails)
4. Workflow enters RETRYING status
5. Send retry signal with corrected account data
6. Workflow completes successfully

## Key Learning Points
- When to use manual vs automatic retries
- Signal-based error correction patterns
- Interactive workflow debugging
- Handling invalid data scenarios gracefully
