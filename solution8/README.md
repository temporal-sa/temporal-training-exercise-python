# Solution 8: Workflow Versioning with Patched API

Complete implementation of workflow versioning using `workflow.patched()`.

## What's Implemented

- `send_notification` activity in `banking_activities.py`
- `workflow.patched("add-notification")` in `money_transfer_workflow.py`
- Replay test in `test_money_transfer_workflow.py`
- Pre-generated workflow history in `workflow_history_v1.json`

## Running

```bash
# Terminal 1: Start worker
uv run solution8/start_worker.py

# Terminal 2: Start workflow
uv run solution8/start_workflow.py
```

## Running Tests

```bash
uv run pytest solution8/test_money_transfer_workflow.py -v
```

## Generating Your Own History File

To regenerate `workflow_history_v1.json` from a pre-patch workflow:

1. Run a workflow using solution7 (pre-notification code)
2. Export the history:
```bash
temporal workflow show --workflow-id <workflow-id> --output json > solution8/workflow_history_v1.json
```
