# Temporal Training Exercises - Python

A series of hands-on exercises to learn Temporal workflow development using Python.

## Prerequisites

- Python 3.8+
- Temporal Server running locally (port 7233)
- UV package manager

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Start Temporal Server (in separate terminal):
   ```bash
   temporal server start-dev --search-attribute AccountId=Text
   ```

## Exercises

### [Exercise 1: Hello Temporal](exercise1/)
**Duration:** 30 minutes  
**Focus:** Basic workflow and activity concepts
- Implement your first Temporal workflow
- Create activities for external operations
- Set up workers and execute workflows

### [Exercise 2: Money Transfer with Signals](exercise2/)
**Duration:** 45 minutes  
**Focus:** Signals and human-in-the-loop processes
- Handle external signals in workflows
- Implement conditional logic based on signals
- Build approval-based business processes

### [Exercise 3: Money Transfer with Queries](exercise3/)
**Duration:** 30 minutes  
**Focus:** Workflow observability and state monitoring
- Add query methods to expose workflow state
- Track workflow progress in real-time
- Monitor workflow execution from external clients

### [Exercise 4: Money Transfer with Search Attributes](exercise4/)
**Duration:** 15 minutes  
**Focus:** Workflow discoverability and filtering
- Implement search attributes for workflow metadata
- Enable workflow filtering in Temporal Web UI
- Make workflows discoverable by business criteria

### [Exercise 5: User Metadata & Activity Summaries](exercise5/)
**Duration:** 30 minutes  
**Focus:** Workflow observability and metadata
- Add activity summaries for runtime context
- Improve workflow observability in Temporal Web UI
- Understand metadata best practices
- Enhance debugging capabilities

### [Exercise 6: Unit Testing](exercise6/)
**Duration:** 45 minutes  
**Focus:** Testing workflows, activities, signals, and queries
- Write comprehensive unit tests for Temporal workflows
- Test activity success and failure scenarios
- Verify signal handling and query responses
- Mock external dependencies for predictable tests

### [Exercise 7: Manual Activity Retry](exercise7/)
**Duration:** 45 minutes  
**Focus:** Manual retry patterns and signal-based error correction
- Implement manual retry patterns using signals
- Handle non-retryable activity failures
- Interactive error correction workflows
- Dynamic request updates during execution

### [Exercise 8: Workflow Versioning with Patched API](exercise8/)
**Duration:** 45 minutes  
**Focus:** Workflow versioning and backward compatibility
- Use `workflow.patched()` to safely evolve workflows
- Write replay tests to verify version compatibility
- Handle multiple workflow versions in production
- Generate and use workflow history for testing

## Running Exercises

Each exercise follows the same pattern:

1. **Start the worker:**
   ```bash
   uv run exercise{N}/start_worker.py
   ```

2. **Execute the workflow:**
   ```bash
   uv run exercise{N}/start_workflow.py
   ```

**For Exercise 6 (Unit Testing):**
```bash
uv run exercise6/run_tests.py
```

## Solutions

Complete solutions are available in the `solution{N}/` directories for reference.

### Running the Solution Tests

Every solution directory carries unit tests for the concept its exercise
teaches. Run them all:

```bash
uv run python run_tests.py
```

Or run one directory at a time:

```bash
cd solution3
uv run pytest -v
```

Each directory needs its own pytest process, and `run_tests.py` gives it one.
The exercises import their modules by flat name (`from banking_activities
import withdraw`) so that `start_worker.py` runs as a plain script, which means
`money_transfer_workflow` resolves to a different file in each directory. A
single pytest process over the whole repo would import whichever directory it
reached first and hand those modules to the rest.

The tests need no running server: `WorkflowEnvironment.start_local()` starts a
throwaway one, shared per directory by the `env` fixture in `conftest.py`.
Where an exercise's activities fail at random, the workflow tests register
stubs under the same activity names so the workflow code under test is
unchanged but the outcome is not a coin flip.

| Directory | What its tests cover |
|---|---|
| `solution1` | Activity in isolation with `ActivityEnvironment`; workflow delegating to it |
| `solution2` | Simulated activity failures; approve and reject paths; buffered signals |
| `solution3` | Query handlers at each stage, including mid-deposit and after close |
| `solution4` | `AccountId` search attribute set on a running workflow, and filtering by it |
| `solution5` | Activity summaries read back out of event history |
| `solution6` | Activities and workflow, as written for the testing exercise |
| `solution7` | Non-retryable `ApplicationError`, and correcting input with retry signals |
| `solution8` | Patched workflow, plus replay of pre-versioning history |

Solutions 3, 4, and 5 reuse `solution2`'s activities unchanged, so their tests
cover only the workflow behaviour each one adds.

### Solution 6: Unit Testing
Comprehensive unit tests for Temporal workflows and activities:
- Activity testing with mocked failures
- Workflow testing with different scenarios
- Query and signal testing
- State transition validation

**Running Tests:**
```bash
cd solution6
uv run python run_tests.py
```

### Solution 7: Manual Activity Retry
Manual retry patterns for handling invalid data scenarios:
- Non-retryable activity failures with `ApplicationError`
- Signal-based retry mechanisms
- Interactive error correction workflows
- Dynamic request updates during execution

### Solution 8: Workflow Versioning
Safe workflow evolution using the Patched API:
- `workflow.patched()` for conditional code branching
- Replay testing with `Replayer` and `WorkflowHistory`
- Pre-generated workflow history for backward compatibility testing
- Notification activity added via versioning

**Running Tests:**
```bash
cd solution8
uv run pytest -v
```

## Key Concepts Covered

- **Workflows:** Orchestration logic and state management
- **Activities:** External operations and side effects
- **Workers:** Task execution and polling
- **Signals:** External events and workflow modification
- **Queries:** Real-time workflow state inspection
- **Search Attributes:** Workflow metadata and discoverability
- **Error Handling:** Retries and failure management
- **Unit Testing:** Testing workflows and activities with mocked dependencies
- **Manual Activity Retry:** Signal-based retry patterns and error correction
- **Workflow Versioning:** Safe evolution with `workflow.patched()` and replay testing

---

## Instruqt Track: Temporal in Practice

These eight exercises are also packaged as an Instruqt hands-on lab called
**Temporal in Practice**. Attendees get a container sandbox with a Temporal dev
server already running, the native code editor pointed at the exercise
directory, and the finished solution one tab away.

```
instruqt/
├── README.md     How to push the track and the sandbox
├── track/        The track definition: track.yml + 8 challenge directories
└── sandbox/      An Instruqt sandbox preset, pushed separately from the track
                  (has its own README on provisioning and the proxy panel)
```

There is no image to build. The preset's `scripts/setup-workshop` installs the
toolchain on stock `ubuntu:24.04`, clones this repo, and starts the Temporal dev
server. Hot Start pre-provisions all of that ahead of the session, so attendees
do not wait on it.

The track and the sandbox are separate artifacts with separate commands, and
this repo's exercise code is part of neither push — it arrives through the git
clone that provisioning performs:

```bash
cd instruqt/track && instruqt track push      # assignments, track.yml
cd instruqt/sandbox && instruqt sandbox push  # then: instruqt sandbox publish
git push                                      # exercise code, proxy files
```

See [instruqt/README.md](instruqt/README.md) for which change needs which
command, the gotchas on each, and the pre-flight checklist before a live
session.
