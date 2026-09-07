---
slug: queries
id: csx8afxbryfo
type: challenge
title: 'Exercise 3: Money Transfer with Queries'
teaser: Ask a running Workflow what it is doing right now, without touching a database.
notes:
- type: text
  contents: |-
    # Where do you look to find out what a Workflow is doing?

    Not a status table. Not a log aggregator. Not a metrics dashboard.

    The Workflow itself holds the state, in ordinary Python variables. A
    Query reads those variables out of a running execution.
- type: text
  contents: |-
    # Signals in, Queries out

    A Signal changes Workflow state and gets written to history. A Query
    reads state and is never written to history at all.

    That is why a Query handler must not mutate anything and must not
    call an Activity. Break that rule and replay stops matching.
tabs:
- id: cgfxaxdrju4z
  title: Code Editor
  type: code
  hostname: workshop
  path: /root/workshop/exercise3
- id: cuujmpqgrqq3
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: nspjaoxyr5ly
  title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: hummo0clzvmb
  title: Temporal UI
  type: service
  hostname: workshop
  path: /
  port: 8233
- id: jxzk1q2w3zxt
  title: Solution
  type: code
  hostname: workshop
  path: /root/workshop/solution3
- id: mobsqvx9nkzg
  title: Network Control Panel
  type: service
  hostname: workshop
  path: /
  port: 5000
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

# Money Transfer with Queries

Same transfer as exercise 2. This time it can answer questions while it runs.

# The Code

Open the [button label="Code Editor" background="#444CE7"](tab-0).

### `money_transfer_workflow.py`

The Query method signatures are already there. You write the bodies and the
state they read.

- Track `transfer_state` through `PENDING`, `IN_PROGRESS`, `COMPLETED`, `REJECTED`.
- Track `current_step` through `WITHDRAWING`, `WAITING_APPROVAL`, `DEPOSITING`, `REFUNDED`.
- Track the approval decision.
- Each `@workflow.query` method returns one of those. Nothing else.

> [!WARNING]
> A Query handler runs during replay. Do not mutate state in one, do not
> execute an Activity from one, and do not sleep in one. Read a variable and
> return it.

### `start_workflow.py`

Call the Query methods on the Workflow handle between the start and the
approval, so you can see the state move.

# Start the Worker

Click the [button label="Worker" background="#444CE7"](tab-1):

```bash,run
uv run exercise3/start_worker.py
```

# Run It

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
uv run exercise3/start_workflow.py
```

The state should read `IN_PROGRESS` and `WAITING_APPROVAL` before the approval
goes out, then `COMPLETED` after.

# Query From Outside

The starter is not special. Ask the most recent Workflow yourself, from the
[button label="Terminal" background="#444CE7"](tab-2):

```bash,run
WORKFLOW_ID=$(temporal workflow list --query 'TaskQueue="MoneyTransferTaskQueue"' --limit 1 -o json | jq -r '.[0].execution.workflowId')
echo "$WORKFLOW_ID"
temporal workflow query --workflow-id "$WORKFLOW_ID" --name get_transfer_state
```

Use the query names you implemented. `temporal workflow describe` lists the
handlers a Workflow exposes if you forget them.

> [!NOTE]
> A Query is answered by a Worker, not by the server. Leave the Worker running
> in the [button label="Worker" background="#444CE7"](tab-1) tab or you get
> `no poller seen for task queue recently`.

# Key Takeaways

- `@workflow.query` exposes Workflow state to any client. Read-only.
- Query results never enter the event history, which is why mutation is banned.
- The state lives in plain Python attributes. Temporal rebuilds them by replay.
- Signals write, Queries read. Reach for a Signal when you need to change something.

Click **Check** when the transfer completes.
