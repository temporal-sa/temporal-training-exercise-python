---
slug: search-attributes
id: 83vq1kh41nbo
type: challenge
title: 'Exercise 4: Money Transfer with Search Attributes'
teaser: Tag a Workflow with a business identifier, then find it by that identifier
  instead of its Workflow ID.
notes:
- type: text
  contents: |-
    # Support asks about account-123. You have 40,000 Workflows. Now what?

    You do not have the Workflow ID. You have an account number.

    One line of code makes that account number queryable across every
    execution the cluster has ever seen.
- type: text
  contents: |-
    # One line. Fifteen minutes.

    The shortest exercise in the workshop. Custom search attributes have to
    be registered on the cluster before a Workflow can set one, so
    `AccountId=Text` is already registered on your dev server.

    Try it without that registration in production and the Workflow Task
    fails outright.
tabs:
- id: cryxhqhzs6wt
  title: Code Editor
  type: code
  hostname: workshop
  path: /root/workshop/exercise4
- id: dg0w7tqhyqvn
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: vpj6ixxv9est
  title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- id: ll6ya1re66lr
  title: Temporal UI
  type: service
  hostname: workshop
  path: /
  port: 8233
- id: xm7n0zznxak4
  title: Solution
  type: code
  hostname: workshop
  path: /root/workshop/solution4
- id: 6l7jehpdu4id
  title: Network Control Panel
  type: service
  hostname: workshop
  path: /
  port: 5000
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

# Money Transfer with Search Attributes

One TODO. One line. A Workflow you can find by account number.

# The Code

Open the [button label="Code Editor" background="#444CE7"](tab-0) and find the
single TODO in `money_transfer_workflow.py`, near the top of `transfer`.

Set the `AccountId` search attribute to `request.from_account` with
`workflow.upsert_search_attributes()`. Do it before the first Activity so the
tag is on the execution from the start.

> [!IMPORTANT]
> `AccountId=Text` is already registered on the dev server in this sandbox.
> Setting an unregistered attribute fails the Workflow Task, which shows up
> as a Workflow that starts and then goes nowhere.

# Run It

Click the [button label="Worker" background="#444CE7"](tab-1):

```bash,run
uv run exercise4/start_worker.py
```

Click the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
uv run exercise4/start_workflow.py
```

The starter uses `account-123` as the source account.

# Find It By Account

From the [button label="Terminal" background="#444CE7"](tab-2):

```bash,run
temporal workflow list --query 'AccountId="account-123"'
```

Now filter on an account that never sent anything:

```bash,run
temporal workflow list --query 'AccountId="account-999"'
```

Empty. The filter is doing real work.

# See It In the UI

Click the [button label="Temporal UI" background="#444CE7"](tab-3). Click your
Workflow, then look at the summary panel. `AccountId` is listed there with its
value.

Back on the Workflows list, put this in the search box:

```bash,nocopy
AccountId="account-123"
```

Click **Check** when the query returns your Workflow.

# Key Takeaways

- `workflow.upsert_search_attributes()` tags an execution with business data.
- Custom attributes must be registered on the cluster first. The dev server
  takes `--search-attribute Name=Type`.
- Search attributes are for finding Workflows, not for storing Workflow state.
  Keep the payload small.
- The same query syntax works in the CLI, the Web UI, and the client API.
