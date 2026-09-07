---
slug: hello-temporal
id: ax828yzz8boi
type: challenge
title: 'Exercise 1: Hello Temporal'
teaser: Write your first Workflow, Activity and Worker. Run it and read the event
  history.
notes:
- type: text
  contents: |-
    # What does a Workflow actually run on?

    You write a function. You never call it. Something else picks it up,
    runs it, and records every step.

    That something is a Worker, and it is polling a task queue right now
    waiting for code you have not written yet.
- type: text
  contents: |-
    # Already running in your sandbox

    A Temporal dev server on 127.0.0.1:7233, with the Web UI on port 8233.
    The AccountId search attribute is already registered, so exercise 4
    works when you get there.

    The Solution tab has finished code for every exercise. Use it when you
    are stuck, not before.
tabs:
- id: 8toghhepyhj7
  title: Code Editor
  type: code
  hostname: workshop
  path: /root/workshop/exercise1
- id: 9rz09kf4mtog
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: 9blcua0ccnut
  title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: lsmbia2ssctf
  title: Temporal UI
  type: service
  hostname: workshop
  path: /
  port: 8233
- id: wxndbkhjvvri
  title: Solution
  type: code
  hostname: workshop
  path: /root/workshop/solution1
- id: 5evr37djgtoy
  title: Network Control Panel
  type: service
  hostname: workshop
  path: /
  port: 5000
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

# Hello Temporal

Four files. Nine TODOs. A greeting that survives anything.

> [!NOTE]
> **Sandbox Notes:**
> - [button label="Code Editor" background="#444CE7"](tab-0) edits the files in `exercise1/`
> - [button label="Worker" background="#444CE7"](tab-1) runs the Worker
> - [button label="Terminal" background="#444CE7"](tab-2) starts Workflows
> - [button label="Temporal UI" background="#444CE7"](tab-3) is the Temporal Web UI
> - [button label="Solution" background="#444CE7"](tab-4) has the finished code
> - [button label="Network Control Panel" background="#444CE7"](tab-5) toggles outbound HTTP
>
> The blue buttons above are clickable. Click any to jump to that tab.
> Instruqt saves editor changes for you. There is no save step.

# The Code

Open the [button label="Code Editor" background="#444CE7"](tab-0). Four files
carry the TODOs:

| File | What goes in it |
|------|-----------------|
| `greeting_activity.py` | The `create_greeting` Activity body |
| `greeting_workflow.py` | Call the Activity with a 5 second `start_to_close_timeout` |
| `start_worker.py` | Register the Workflow and the Activity on `hello-task-queue` |
| `start_workflow.py` | Connect a Client and execute the Workflow |

The Activity is where side effects live. The Workflow only orchestrates. The
Worker is the process that runs both.

# Start the Worker

Click the [button label="Worker" background="#444CE7"](tab-1) terminal:

```bash,run
uv run exercise1/start_worker.py
```

It stays in the foreground and polls. Leave it running.

# Run It

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
uv run exercise1/start_workflow.py
```

```bash,nocopy
Hello, Temporal!
```

# Read the History

Click the [button label="Temporal UI" background="#444CE7"](tab-3). Click your
Workflow at the top of the list. Hit refresh if it is not there yet.

Open the **Event History**. Look for `ActivityTaskScheduled`,
`ActivityTaskStarted` and `ActivityTaskCompleted`. Those three events are the
whole point. Temporal wrote down that the Activity ran and what it returned.
Replay reads that back instead of calling the Activity again.

Click **Check** when the greeting prints.

# Key Takeaways

- `@workflow.defn` marks the class, `@workflow.run` marks the entry point.
- Activities do the side effects. Workflows orchestrate and stay deterministic.
- A Worker only runs what you register with it, on the task queue you name.
- Every Activity result lands in the event history, which is what makes replay work.
