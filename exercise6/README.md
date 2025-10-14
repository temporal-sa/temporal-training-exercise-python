# Exercise 6: Unit Testing Temporal Workflows

**Duration:** 45 minutes  
**Focus:** Testing workflows, activities, signals, and queries

## Objective

Learn how to write comprehensive unit tests for Temporal workflows using the testing framework. You'll test workflow execution, signals, queries, and different scenarios.

## What You'll Learn

- Setting up test environments with `WorkflowEnvironment`
- Testing workflow execution with different outcomes
- Verifying signal handling behavior
- Testing query methods for state inspection
- Mocking activities to control test scenarios

## Your Task

Complete the unit tests in `test_money_transfer_workflow.py` by implementing the TODO items:

1. **Test approved transfer scenario:**
   - Verify initial transfer state is "IN_PROGRESS"
   - Check that current step progresses correctly
   - Confirm final state is "COMPLETED" after approval
   - Assert the success message

2. **Test rejected transfer scenario:**
   - Check state before approval
   - Verify final state is "REJECTED" after rejection
   - Confirm final step is "REFUNDED"
   - Assert the rejection message

## Key Testing Concepts

- **WorkflowEnvironment**: Provides isolated test environment
- **Worker**: Handles workflow and activity execution in tests
- **Mocking**: Control random behavior for predictable tests
- **Queries**: Test workflow state inspection
- **Signals**: Test external workflow interaction

## Running the Tests

```bash
uv run exercise6/run_tests.py
```

## Expected Test Coverage

Your tests should verify:
- Workflow state transitions
- Query method responses
- Signal handling
- Different execution paths (approved vs rejected)
- Proper result messages