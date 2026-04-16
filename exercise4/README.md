# Exercise 4: Money Transfer with Search Attributes

## Objective

Learn how to use Temporal search attributes to make workflows discoverable and filterable.

## Background

Search attributes allow you to add metadata to workflows that can be used for filtering and searching in the Temporal Web UI and programmatically via the client API. This is essential for production systems where you need to find workflows based on business criteria.

## Your Task

Implement search attribute functionality in the money transfer workflow:

1. **Add Search Attribute**: Set the `AccountId` search attribute to the source account ID when the workflow starts
2. **Test Filtering**: Verify that workflows can be filtered by account ID in the Temporal Web UI

## Prerequisites

Start Temporal Server with the custom search attribute:
```bash
temporal server start-dev --search-attribute AccountId=Text
```

## Implementation Steps

### Step 1: Set Search Attribute

In `money_transfer_workflow.py`, find the TODO comment and implement:
- Use `workflow.upsert_search_attributes()` to set the `AccountId` search attribute
- Set the value to `request.from_account`

### Step 2: Test the Implementation

1. Start the worker:
   ```bash
   uv run exercise4/start_worker.py
   ```

2. Run multiple workflows with different account IDs:
   ```bash
   uv run exercise4/start_workflow.py
   ```

3. Open Temporal Web UI at http://localhost:8233 and verify:
   - Workflows appear with the AccountId search attribute
   - You can filter workflows by AccountId

## Key Concepts

- **Search Attributes**: Metadata for workflow discoverability
- **Upsert Operations**: Adding/updating search attributes during execution
- **Workflow Filtering**: Finding workflows based on business criteria

## Expected Behavior

- Workflows should be tagged with the source account ID
- Multiple workflows can be filtered by account in the Web UI
- Search attributes appear in workflow details

## Verification

Check that your implementation works by:
1. Running workflows with different account IDs
2. Filtering by AccountId in the Temporal Web UI
3. Confirming the search attribute appears in workflow metadata

## Next Steps

After completing this exercise, you'll understand how to make workflows discoverable and filterable using search attributes, which is crucial for production workflow management.