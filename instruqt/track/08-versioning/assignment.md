---
slug: versioning
id: hpmyakvbvng0
type: challenge
title: 'Exercise 8: Workflow Versioning with the Patched API'
teaser: Add a step to a Workflow that already has executions in flight. Prove the
  old histories still replay.
notes:
- type: text
  contents: |-
    # You shipped it. Four thousand are still running. Now change the logic.

    Add one Activity call in the middle of a Workflow and every execution
    started before the deploy has a history that no longer matches the
    code.

    Temporal calls that a non-determinism error, and it will not guess.
- type: text
  contents: |-
    # Did you know?

    `workflow.patched("add-notification")` returns `False` when replaying a
    history recorded before the patch existed, and `True` for anything
    new.

    One boolean, two versions of the same Workflow, running on the same
    Worker at the same time.
tabs:
- id: 5chyuwxeadwy
  title: Code Editor
  type: code
  hostname: workshop
  path: /root/workshop/exercise8
- id: b36seg0ids0o
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: e6ljndfmaadi
  title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: o1abawwsj8yx
  title: Temporal UI
  type: service
  hostname: workshop
  path: /
  port: 8233
- id: zhoy94x3dvbp
  title: Solution
  type: code
  hostname: workshop
  path: /root/workshop/solution8
- id: 6d7yacx7assj
  title: Network Control Panel
  type: service
  hostname: workshop
  path: /
  port: 5000
difficulty: advanced
timelimit: 1800
enhanced_loading: null
---

# Workflow Versioning with the Patched API

Version 1 withdraws, waits, deposits. Version 2 also sends a notification.
Both have to work, on the same Worker, at the same time.

# The Code

Open the [button label="Code Editor" background="#444CE7"](tab-0). Eight TODOs
across four files.

### Task 1: the new Activity

In `banking_activities.py`, add it:

```python
@activity.defn
async def send_notification(account: str, amount: float) -> str:
```

Then import it in `money_transfer_workflow.py` and register it in
`start_worker.py`. Three of the eight TODOs are that one Activity threaded
through three files.

### Task 2: gate it behind a patch

In `money_transfer_workflow.py`, after the deposit:

```python
if workflow.patched("add-notification"):
    await workflow.execute_activity(
        send_notification,
        args=[request.to_account, request.amount],
        start_to_close_timeout=timedelta(seconds=5),
    )
```

Only on the approved path. A rejected transfer refunds and sends nothing.

> [!WARNING]
> Change IDs are permanent. `add-notification` goes into the event history
> as a marker. Renaming it later breaks every history that recorded the old
> name.

### Task 3: the replay test

In `test_money_transfer_workflow.py`, uncomment and finish
`test_replay_old_workflow_history`. It loads a pre-patch event history from
`workflow_history_v1.json`, feeds it to a `Replayer` running your new code, and
passes only if replay produces no non-determinism error.

> [!NOTE]
> `workflow_history_v1.json` is already in `exercise8/`, recorded from the
> pre-patch version of this Workflow. Task 4 in the exercise README walks
> through generating your own if you want to see where it comes from.

# Run the New Version

Click the [button label="Worker" background="#444CE7"](tab-1):

```bash,run
uv run exercise8/start_worker.py
```

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
uv run exercise8/start_workflow.py
```

Open the [button label="Temporal UI" background="#444CE7"](tab-3) and look at
the event history. Two things to find: a `MarkerRecorded` event for the patch,
and the `send_notification` Activity after the deposit.

# Prove the Old One Still Replays

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
PYTHONPATH=exercise8 uv run pytest exercise8/test_money_transfer_workflow.py -v
```

```bash,nocopy
test_new_workflow_with_notification PASSED
test_replay_old_workflow_history PASSED
```

Two tests. The first proves the new path runs the notification. The second
proves a history recorded before the patch existed still replays against the
new code.

Now break it deliberately. Delete the `if workflow.patched(...)` line, leave
the `send_notification` call in place, and rerun the tests. The replay test
fails with a non-determinism error, because the old history has no record of
that Activity. Put the patch back.

> [!NOTE]
> `PYTHONPATH=exercise8` is needed because these test files import their
> modules by bare name rather than as a package.

Click **Check** when both tests pass.

# Key Takeaways

- `workflow.patched(id)` is `False` for histories recorded before the patch,
  `True` for new executions.
- The patch decision is written to history as a marker, so replay makes the
  same choice every time.
- Change IDs are permanent. Pick a name you can live with.
- `Replayer` against a saved history is the test that catches non-determinism
  before your users do.
- Once every pre-patch execution has finished, `workflow.deprecate_patch()`
  starts the cleanup.
