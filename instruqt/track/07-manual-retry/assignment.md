---
slug: manual-retry
id: moydiyhk2xkk
type: challenge
title: 'Exercise 7: Manual Activity Retry'
teaser: An Activity fails on bad data. Automatic retry cannot help. Fix the data with
  a Signal and let it continue.
notes:
- type: text
  contents: |-
    # The account number is wrong. How many times should Temporal retry?

    Automatic retry is the right answer when the failure is transient.
    A network blip, a rate limit, a restarted database.

    A typo in an account number is not transient. Retrying it a hundred
    times gets you the same error a hundred times.
- type: text
  contents: |-
    # Did you know?

    `ApplicationError(..., non_retryable=True)` tells Temporal to stop
    retrying immediately and surface the failure to the Workflow.

    The Workflow can then park, wait for a human to send corrected data,
    and pick the Activity back up. The withdrawal that already succeeded
    stays succeeded.
tabs:
- id: 1m9kpdrv2pz2
  title: Code Editor
  type: code
  hostname: workshop
  path: /root/workshop/exercise7
- id: 8icc0ytdd9e6
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: hrifyxxvlyqs
  title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: 1ccytfuhyiqt
  title: Temporal UI
  type: service
  hostname: workshop
  path: /
  port: 8233
- id: ckxmgrzi6nyp
  title: Solution
  type: code
  hostname: workshop
  path: /root/workshop/solution7
- id: w4u3hafzih4o
  title: Network Control Panel
  type: service
  hostname: workshop
  path: /
  port: 5000
- id: daz5yxw8u07i
  title: Signals
  type: terminal
  hostname: workshop
  workdir: /root/workshop
difficulty: intermediate
timelimit: 1800
enhanced_loading: null
---

# Manual Activity Retry

The transfer stops on a bad account number and waits for you to fix it. The
withdrawal that already went through does not get undone.

> [!IMPORTANT]
> This exercise has a seventh tab. Use
> [button label="Signals" background="#444CE7"](tab-6) to send Signals while
> the starter is still waiting in the
> [button label="Terminal" background="#444CE7"](tab-2).

# The Code

Open the [button label="Code Editor" background="#444CE7"](tab-0). Eight TODOs
across two files.

### `banking_activities.py`

Five TODOs. Implement `withdraw`, `deposit` and `refund`. Each of the first two
raises a non-retryable error when the account name contains `invalid`:

```python
if "invalid" in account:
    raise ApplicationError(
        f"Invalid toAccount ID: {account}",
        type="InvalidAccount",
        non_retryable=True,
    )
```

`non_retryable=True` is the whole trick. Without it Temporal retries forever
and the Workflow never gets a chance to intervene.

### `money_transfer_workflow.py`

Three TODOs.

Implement `_execute_with_manual_retry(operation)`. Loop: run the operation,
and on `ActivityError` set the status to `RETRYING`, clear the retry flag, and
wait for a retry Signal before going round again.

Then wrap the `withdraw` and `deposit` calls in it.

The `retry` Signal handler takes a `RetryUpdate` with a `key` and a `value`,
writes the new value onto `self.request`, and sets the retry flag. The keys are
`fromAccount`, `toAccount` and `amount`.

# Break It On Purpose

The starter ships with two valid accounts, which completes on the first try. To
see the retry path, open `start_workflow.py` in the
[button label="Code Editor" background="#444CE7"](tab-0) and change the target:

```python
to_account="invalid-account-002",
```

# Start the Worker

Click the [button label="Worker" background="#444CE7"](tab-1):

```bash,run
PYTHONPATH=exercise7 uv run python -m exercise7.start_worker
```

> [!NOTE]
> `exercise7` mixes relative and flat imports, so it runs as a module with
> `exercise7` on the path. The other exercises run as plain scripts.

# Run It

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
PYTHONPATH=exercise7 uv run python -m exercise7.start_workflow
```

The starter prints a Workflow ID and sends the approval. Withdraw succeeds.
Deposit hits `invalid-account-002` and fails once, with no retry. The starter
is now waiting for a result that will not arrive until you fix the data.

# Check Where It Parked

Click the [button label="Signals" background="#444CE7"](tab-6). Grab the
Workflow that is still running and ask it what it is doing:

```bash,run
WORKFLOW_ID=$(temporal workflow list --query 'ExecutionStatus="Running"' --limit 1 -o json | jq -r '.[0].execution.workflowId')
echo "$WORKFLOW_ID"
temporal workflow query --workflow-id "$WORKFLOW_ID" --name get_status
```

```bash,nocopy
RETRYING
```

That is the Workflow parked mid-transfer, holding the state of a withdrawal
that already succeeded.

# Fix It

Still in the [button label="Signals" background="#444CE7"](tab-6), send the
corrected account. `$WORKFLOW_ID` is already set from the previous step:

```bash,run
temporal workflow signal \
  --workflow-id "$WORKFLOW_ID" \
  --name retry \
  --input '{"key":"toAccount","value":"account-456"}'
```

Back in the [button label="Terminal" background="#444CE7"](tab-2), the starter
prints the result. The deposit ran against the corrected account. Withdraw
never ran twice.

Open the [button label="Temporal UI" background="#444CE7"](tab-3) and look at
the event history: one `ActivityTaskFailed` for the deposit, then the Signal,
then a fresh `ActivityTaskScheduled` for the same Activity.

Click **Check** when the transfer completes.

# Key Takeaways

- `non_retryable=True` stops automatic retry for failures that data changes,
  not time, will fix.
- A Workflow can catch the failure, park on `wait_condition`, and resume.
- Work already completed stays completed. That is the difference from
  restarting the process.
- Signals carry the corrected data in, so no redeploy and no manual database edit.
