---
slug: signals
id: yxyes1vwveuh
type: challenge
title: 'Exercise 2: Money Transfer with Signals'
teaser: A transfer that stops and waits for a human to approve it, then deposits or
  refunds.
notes:
- type: text
  contents: |-
    # A Workflow is waiting on a human. Who pays for the wait?

    The money left the source account. Now a person has to approve the
    deposit. That person is at lunch.

    No polling loop. No cron job. No row in a "pending approvals" table.
    The Workflow just waits, and the wait costs you nothing.
- type: text
  contents: |-
    # Did you know?

    A Workflow blocked on `workflow.wait_condition` holds no worker
    thread and no memory. Temporal takes it off the Worker entirely and
    brings it back when the Signal arrives. A wait of ten seconds and a
    wait of ten months cost the same.
tabs:
- id: kqlbrmata9r6
  title: Code Editor
  type: code
  hostname: workshop
  path: /root/workshop/exercise2
- id: hhmmxvaofhhc
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: ik8atbtcqhaz
  title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: uhsvkhvrvk3x
  title: Temporal UI
  type: service
  hostname: workshop
  path: /
  port: 8233
- id: n4eyotm2fgyj
  title: Solution
  type: code
  hostname: workshop
  path: /root/workshop/solution2
- id: lsa90b3jk3by
  title: Network Control Panel
  type: service
  hostname: workshop
  path: /
  port: 5000
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

# Money Transfer with Signals

Withdraw. Wait for a human. Deposit if they said yes, refund if they said no.

# The Code

Open the [button label="Code Editor" background="#444CE7"](tab-0). Three files
carry TODOs. `transfer_request.py` and `start_worker.py` are already done.

### `banking_activities.py`

Implement `withdraw`, `deposit` and `refund`. Each one logs what it did and
simulates a failure some of the time. The random failure is deliberate: it is
what makes Temporal's automatic Activity retries visible in the next step.

### `money_transfer_workflow.py`

- A `@workflow.signal` handler named `approve` that records the decision.
- Execute `withdraw`.
- Wait for the approval to arrive.
- Execute `deposit` on approval, `refund` on rejection.

### `start_workflow.py`

Send the `approve` Signal to the running Workflow handle.

# Start the Worker

Click the [button label="Worker" background="#444CE7"](tab-1):

```bash,run
uv run exercise2/start_worker.py
```

# Run It

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
uv run exercise2/start_workflow.py
```

The starter waits two seconds, then sends the approval. Watch the Worker tab.
If an Activity hit its simulated failure you will see the exception, then the
same Activity running again. You did not write that retry.

# Signal It Yourself

The Signal does not have to come from the starter. Any client that can reach
the server can move the Workflow along, including the CLI. Paste the Workflow
ID the starter printed and run this from the
[button label="Terminal" background="#444CE7"](tab-2):

```bash
WORKFLOW_ID=money-transfer-1788758722478

temporal workflow signal \
  --workflow-id "$WORKFLOW_ID" \
  --name approve \
  --input true
```

This particular run already got its approval from the starter two seconds in,
so the Signal lands on a Workflow that has finished. Exercise 7 uses this same
command against a Workflow that is genuinely waiting.

# Look at the Wait

Click the [button label="Temporal UI" background="#444CE7"](tab-3). Open your
Workflow, then the **Event History**. Find `WorkflowExecutionSignaled`. Above
it, the Workflow was doing nothing at all, and it was not consuming a Worker
while it did.

Click **Check** when the transfer completes.

# Key Takeaways

- `@workflow.signal` handlers mutate Workflow state from outside.
- `workflow.wait_condition` blocks on that state without burning a Worker.
- Failed Activities retry on their own. The default retry policy is already on.
- The Signal is recorded in history, so replay makes the same decision.
