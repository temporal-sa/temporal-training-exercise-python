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

### Exercise 1: Hello Temporal
**Duration:** 30 minutes  
**Focus:** Basic workflow and activity concepts
- Implement your first Temporal workflow
- Create activities for external operations
- Set up workers and execute workflows

### Exercise 2: Money Transfer with Signals
**Duration:** 45 minutes  
**Focus:** Signals and human-in-the-loop processes
- Handle external signals in workflows
- Implement conditional logic based on signals
- Build approval-based business processes

### Exercise 3: Money Transfer with Queries
**Duration:** 30 minutes  
**Focus:** Workflow observability and state monitoring
- Add query methods to expose workflow state
- Track workflow progress in real-time
- Monitor workflow execution from external clients

### Exercise 4: Money Transfer with Search Attributes
**Duration:** 15 minutes  
**Focus:** Workflow discoverability and filtering
- Implement search attributes for workflow metadata
- Enable workflow filtering in Temporal Web UI
- Make workflows discoverable by business criteria

### Exercise 5: User Metadata & Activity Summaries
**Duration:** 30 minutes  
**Focus:** Workflow observability and metadata
- Add activity summaries for runtime context
- Improve workflow observability in Temporal Web UI
- Understand metadata best practices
- Enhance debugging capabilities

### Exercise 6: Unit Testing
**Duration:** 45 minutes  
**Focus:** Testing workflows, activities, signals, and queries
- Write comprehensive unit tests for Temporal workflows
- Test activity success and failure scenarios
- Verify signal handling and query responses
- Mock external dependencies for predictable tests

### Exercise 7: Manual Activity Retry
**Duration:** 45 minutes  
**Focus:** Manual retry patterns and signal-based error correction
- Implement manual retry patterns using signals
- Handle non-retryable activity failures
- Interactive error correction workflows
- Dynamic request updates during execution

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
