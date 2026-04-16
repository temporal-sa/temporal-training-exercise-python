# Exercise 8 Solution: Workflow Versioning

## Key Implementation Points

### 1. Add Notification Activity
```python
@activity.defn
async def send_notification(account: str, amount: float) -> str:
    activity.logger.info(f"Sending notification for ${amount} to account {account}")
    return f"Notification sent to {account}"
```

### 2. Import and Use send_notification in Workflow
```python
with workflow.unsafe.imports_passed_through():
    from banking_activities import withdraw, deposit, refund, send_notification
```

### 3. Use workflow.patched() for Versioning
```python
# After deposit, before marking COMPLETED:
if workflow.patched("add-notification"):
    await workflow.execute_activity(
        send_notification,
        args=[self.request.to_account, self.request.amount],
        start_to_close_timeout=timedelta(seconds=5),
    )
```

### 4. Replay Test Implementation
```python
@pytest.mark.asyncio
async def test_replay_old_workflow_history():
    history_path = os.path.join(os.path.dirname(__file__), "workflow_history_v1.json")
    with open(history_path, "r") as f:
        history_json = json.load(f)

    replayer = Replayer(workflows=[MoneyTransferWorkflow])
    await replayer.replay_workflow(
        WorkflowHistory.from_json("money-transfer-workflow", history_json)
    )
```

## Key Concepts

### workflow.patched() Behavior
- **New workflows**: `workflow.patched("add-notification")` returns `True` → executes notification
- **Replaying old workflows**: `workflow.patched("add-notification")` returns `False` → skips notification
- **Change ID**: Must be unique and permanent (never reuse or remove)

### Why Versioning Matters
- Workflows can run for days, weeks, or months
- Code must evolve without breaking running workflows
- Temporal replays workflow history to recover state
- Non-deterministic changes break replay → workflow fails

### Safe Evolution Pattern
1. Add new code inside `if workflow.patched("change-id")` block
2. Test replay with old workflow histories
3. Deploy new code — old workflows continue, new workflows use new logic
4. Use `workflow.deprecate_patch()` once all old workflows complete
5. Eventually remove the deprecated patch call

### Replay Testing
- Validates backward compatibility
- Catches determinism errors before production
- Uses real workflow history from old version
- Replays with new workflow code
