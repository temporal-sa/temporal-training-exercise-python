---
slug: activity-summaries
id: s8qmq2sw9uu1
type: challenge
title: 'Exercise 5: Activity Summaries and Metadata'
teaser: Make the event history readable. Attach a one-line summary to every Activity
  and to the execution itself.
notes:
- type: text
  contents: |-
    # Three Activities named withdraw, deposit and refund. Which account?

    You are on a call. Someone shares an event history. It says
    `withdraw`, `deposit`, `refund`.

    It does not say whose money, or how much. That detail was in the
    payload, and nobody wants to click into three payloads on a call.
- type: text
  contents: |-
    # Did you know?

    Activity summaries are user metadata. They render in the Web UI beside
    the event, they cost nothing at runtime, and they are not part of
    Workflow logic. Changing a summary string does not break replay.
tabs:
- id: xslo2ayfgy2s
  title: Code Editor
  type: code
  hostname: workshop
  path: /root/workshop/exercise5
- id: zyxjmmwhavab
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: wlje2hzqagjz
  title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: tx7bsgiyfxd6
  title: Temporal UI
  type: service
  hostname: workshop
  path: /
  port: 8233
- id: soz870nqjetk
  title: Solution
  type: code
  hostname: workshop
  path: /root/workshop/solution5
- id: 9m6r1efnfbxn
  title: Network Control Panel
  type: service
  hostname: workshop
  path: /
  port: 5000
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

# Activity Summaries and Metadata

The Workflow already works. This exercise makes it legible to whoever debugs
it at 3am.

# The Code

Open the [button label="Code Editor" background="#444CE7"](tab-0).

### `money_transfer_workflow.py`

Six TODOs, three Activities. Add a `summary=` argument to each
`workflow.execute_activity` call and interpolate the account into it:

```python
await workflow.execute_activity(
    withdraw,
    args=[request.from_account, request.amount],
    start_to_close_timeout=timedelta(seconds=5),
    summary=f"Withdrawing funds from account {request.from_account}",
)
```

Do the same for `deposit` and `refund`.

### `banking_activities.py`

Three TODOs, same Activity bodies as exercise 2. Fill them in if you are
starting fresh here.

### `start_workflow.py`

Two TODOs for a summary on the execution itself. Pass `static_summary=` to
`client.start_workflow`:

```python
static_summary=f"Money transfer from {request.from_account} to {request.to_account}"
```

> [!NOTE]
> The TODO comment in the file suggests `memo={"summary": ...}`. `memo` is
> arbitrary key-value data that the UI shows in its own panel.
> `static_summary` is the metadata field the UI renders as the execution's
> title. Use `static_summary`.

# Run It

Click the [button label="Worker" background="#444CE7"](tab-1):

```bash,run
uv run exercise5/start_worker.py
```

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
uv run exercise5/start_workflow.py
```

# See the Difference

Click the [button label="Temporal UI" background="#444CE7"](tab-3). Click your
Workflow at the top of the list. Refresh if it is not there.

The summary shows next to the execution name. Open the **Event History** and
look at the Activity rows: each one now says which account it touched and
which direction the money went. Compare that against the exercise 2 execution
further down the list.

Click **Check** when the summaries show up.

# Key Takeaways

- `summary=` on `execute_activity` labels one Activity in the UI.
- `static_summary=` on `start_workflow` labels the whole execution.
- Both are user metadata. They do not affect Workflow logic or replay.
- Keep summaries short and specific. They are read at a glance, under pressure.
