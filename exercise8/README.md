# Exercise 8: Workflow Versioning with Patched API

## Objective
Learn how to safely evolve workflows using Temporal's `workflow.patched()` API for versioning, ensuring backward compatibility with running workflows.

## Scenario
We'll evolve the money transfer workflow by adding a new notification step after deposit. Using versioning ensures existing workflows continue running correctly while new workflows use the updated logic.

## Key Concepts
- Workflow versioning and why it's needed
- Using `workflow.patched()` to introduce non-deterministic changes
- Writing replay tests to verify version compatibility
- Handling multiple workflow versions in production

## Background: Why Versioning?

Temporal workflows are deterministic — replaying history must produce the same result. Adding new activities or changing execution order breaks this. The `workflow.patched()` API allows safe evolution:

```python
# Version 1: Original workflow (no patched call)
await workflow.execute_activity(withdraw, ...)
await workflow.execute_activity(deposit, ...)

# Version 2: Add notification (with patched)
await workflow.execute_activity(withdraw, ...)
await workflow.execute_activity(deposit, ...)
if workflow.patched("add-notification"):
    await workflow.execute_activity(send_notification, ...)
```

**How it works:**
- Old workflows: `workflow.patched()` returns `False` (skip new code)
- New workflows: `workflow.patched()` returns `True` (run new code)
- Change IDs must be unique and permanent

## Tasks

### Task 1: Add Notification Activity
Create a `send_notification` activity in `banking_activities.py`:
```python
@activity.defn
async def send_notification(account: str, amount: float) -> str:
```

### Task 2: Version the Workflow
In `money_transfer_workflow.py`, after the deposit activity:
1. Use `workflow.patched("add-notification")` to conditionally call `send_notification`
2. Only send notification when transfer is approved and completed

### Task 3: Write Replay Test
In `test_money_transfer_workflow.py`:
1. Load pre-generated workflow history from `workflow_history_v1.json`
2. Use `Replayer` to replay old history against new workflow code
3. Verify replay succeeds without errors

### Task 4: Generate History File

1. Start Temporal dev server:
```bash
temporal server start-dev --search-attribute AccountId=Text
```

2. In another terminal, start the worker (using solution7 code — the pre-patch version):
```bash
uv run solution7/start_worker.py
```

3. Run a workflow:
```bash
uv run solution7/start_workflow.py
```

4. Download history from Temporal Web UI:
   - Open http://localhost:8233
   - Find your workflow execution
   - Click "Download" → "Download Event History JSON"
   - Save as `exercise8/workflow_history_v1.json`

Alternatively, use the CLI:
```bash
temporal workflow show --workflow-id <your-workflow-id> --output json > exercise8/workflow_history_v1.json
```

## Testing Your Solution

### Run the workflow:
```bash
# Terminal 1: Start worker
uv run exercise8/start_worker.py

# Terminal 2: Start workflow
uv run exercise8/start_workflow.py
```

### Run replay tests:
```bash
uv run pytest exercise8/test_money_transfer_workflow.py -v
```

## Expected Behavior

**New workflow execution:**
1. Withdraw from account
2. Wait for approval signal
3. If approved: deposit + send notification
4. If rejected: refund (no notification)

**Replay of old workflow:**
- Skips notification step
- Completes successfully without errors

## Tips

- Change IDs are permanent — never reuse or remove them
- Test replay before deploying versioned workflows
- Use descriptive change IDs (e.g., `add-notification`)
- Multiple `workflow.patched()` calls can coexist in one workflow
- Use `workflow.deprecate_patch()` once all old workflows have completed
