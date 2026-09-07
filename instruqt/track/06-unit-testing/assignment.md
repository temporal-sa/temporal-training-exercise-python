---
slug: unit-testing
id: tr6dbwxpsdqm
type: challenge
title: 'Exercise 6: Unit Testing Workflows'
teaser: Test a Workflow that waits for a human, with time skipping and mocked Activities.
  No dev server involved.
notes:
- type: text
  contents: |-
    # How do you unit test a Workflow that waits two days for approval?

    You do not wait two days. You do not mock out the wait either.

    The test environment skips the clock forward the instant nothing is
    left to run, so a two-day timer resolves in microseconds and the
    Workflow never knows.
- type: text
  contents: |-
    # No server needed

    `WorkflowEnvironment.start_time_skipping()` spins up an in-process
    test server. These tests run in CI with nothing installed, and they
    finish in under a second.
tabs:
- id: lgbfl4mocynf
  title: Code Editor
  type: code
  hostname: workshop
  path: /root/workshop/exercise6
- id: timu3mid8c2p
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: ieqaprsr07f5
  title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: ou8rylih8nx2
  title: Temporal UI
  type: service
  hostname: workshop
  path: /
  port: 8233
- id: dns00ryf9h3z
  title: Solution
  type: code
  hostname: workshop
  path: /root/workshop/solution6
- id: klxupxpuexp3
  title: Network Control Panel
  type: service
  hostname: workshop
  path: /
  port: 5000
difficulty: intermediate
timelimit: 1800
enhanced_loading: null
---

# Unit Testing Workflows

No Worker to start. No dev server to talk to. Two test files, fourteen TODOs.

> [!NOTE]
> This is the only exercise that does not need the Temporal dev server. Run
> everything from the [button label="Terminal" background="#444CE7"](tab-2).

# The Code

Open the [button label="Code Editor" background="#444CE7"](tab-0).

### `test_banking_activities.py`

Five TODOs. Test the Activities on their own: `withdraw` succeeds, `withdraw`
fails, `deposit` succeeds, `deposit` fails, `refund` succeeds.

The Activities fail randomly on purpose, so patch the randomness to make each
outcome deterministic:

```python
with patch("random.random", return_value=0.9):
    ...
```

### `test_money_transfer_workflow.py`

Nine TODOs across two scenarios.

**Approved transfer.** Start the Workflow, Query the state before approving,
Signal `approve` with `True`, then assert:

- initial `transfer_state` is `IN_PROGRESS`
- `current_step` moves through the withdraw and approval steps
- final `transfer_state` is `COMPLETED`
- the result is the success message

**Rejected transfer.** Same shape, Signal `approve` with `False`, then assert
`transfer_state` is `REJECTED`, `current_step` is `REFUNDED`, and the result is
the rejection message.

The `WorkflowEnvironment` and `Worker` scaffolding is already written. You are
filling in the assertions and the Signal and Query calls.

# Run the Tests

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
uv run pytest exercise6/ -v
```

Seven tests. All seven should pass.

```bash,nocopy
exercise6/test_banking_activities.py::TestBankingActivities::test_withdraw_success PASSED
...
exercise6/test_money_transfer_workflow.py::TestMoneyTransferWorkflow::test_approved_transfer PASSED
```

> [!WARNING]
> Run pytest from `/root/workshop`, not from inside `exercise6/`. The test
> files use package-relative imports, so pytest needs the repo root as its
> starting point.

Watch a single test while you work on it:

```bash
uv run pytest exercise6/test_money_transfer_workflow.py::TestMoneyTransferWorkflow::test_approved_transfer -v
```

Click **Check** when all seven pass.

# Key Takeaways

- `WorkflowEnvironment.start_time_skipping()` gives you a test server in-process.
- Time skipping fast-forwards timers, so testing a long wait costs nothing.
- Query a running Workflow inside a test to assert on intermediate state, not
  just the return value.
- Patch the source of randomness, not the Activity, when you want a specific
  outcome.
