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

## Solutions

Complete solutions are available in the `solution{N}/` directories for reference.

## Key Concepts Covered

- **Workflows:** Orchestration logic and state management
- **Activities:** External operations and side effects
- **Workers:** Task execution and polling
- **Signals:** External events and workflow modification
- **Queries:** Real-time workflow state inspection
- **Error Handling:** Retries and failure management
