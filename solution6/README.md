# Solution 6: Unit Tests for Money Transfer Workflow

This solution demonstrates comprehensive unit testing for Temporal workflows and activities using pytest and Temporal's testing framework.

## Features

- **Activity Tests**: Unit tests for banking activities (withdraw, deposit, refund)
- **Workflow Tests**: Comprehensive workflow testing including:
  - Approved transfer flow
  - Rejected transfer flow
  - Query functionality
  - State transitions
- **Data Class Tests**: Tests for TransferRequest data class

## Test Structure

- `test_banking_activities.py` - Tests for banking activities with mocked failures
- `test_money_transfer_workflow.py` - Comprehensive workflow tests
- `test_transfer_request.py` - Data class tests

## Running Tests

1. Run all tests:
   ```bash
   uv run pytest
   ```

2. Run with the test runner:
   ```bash
   uv run python run_tests.py
   ```

3. Run specific test file:
   ```bash
   uv run pytest test_money_transfer_workflow.py
   ```

**Note:** Dependencies are managed via `pyproject.toml` and installed with `uv sync`.

## Key Testing Concepts

- **WorkflowEnvironment**: Provides isolated test environment for workflows
- **ActivityEnvironment**: Enables testing activities in isolation
- **Mocking**: Uses unittest.mock to control random failures in activities
- **Async Testing**: Proper async/await patterns with pytest-asyncio

## Test Coverage

The tests cover:
- Happy path scenarios (approved transfers)
- Error scenarios (rejected transfers)
- Activity failures and retries
- Query functionality at different workflow states
- Signal handling
- State transitions throughout workflow execution