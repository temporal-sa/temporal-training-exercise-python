# Exercise 4 Solution: Money Transfer with Search Attributes

## Overview

This exercise demonstrates how to use Temporal search attributes to make workflows discoverable and filterable.

## Key Implementation Points

### 1. Setting Search Attributes

Add search attribute in the workflow run method:

```python
@workflow.run
async def transfer(self, request: TransferRequest) -> str:
    workflow.logger.info(f"Starting transfer: {request}")
    
    # Set search attributes for filtering
    workflow.upsert_search_attributes({"AccountId": [request.from_account]})
    
    # ... rest of workflow logic
```

### 2. Search Attribute Configuration

The search attribute `AccountId` must be configured on the Temporal server:
- Type: Text
- Already configured in the server startup command in README.md

### 3. Using Search Attributes

Search attributes enable:
- **Web UI Filtering**: Filter workflows by AccountId in Temporal Web UI
- **Programmatic Search**: Query workflows using client API
- **Workflow Discovery**: Find workflows based on business criteria

## Key Concepts Learned

- **Search Attributes**: Metadata attached to workflows for discoverability
- **Upsert Operations**: Adding or updating search attributes during workflow execution
- **Workflow Filtering**: Finding workflows based on business criteria
- **Production Readiness**: Making workflows manageable at scale

## Testing the Implementation

1. Run multiple workflows with different account IDs
2. Open Temporal Web UI at http://localhost:8233
3. Use the filter feature to search by AccountId
4. Verify workflows are properly tagged and filterable

## Expected Output

```
Starting money transfer workflow...
Before approval - state: IN_PROGRESS, step: WAITING_FOR_APPROVAL
Sending approval signal...
Approval status: True
Final state: COMPLETED, step: COMPLETED
Transfer result: Transfer completed successfully
```

Plus the workflow should appear in the Web UI with AccountId search attribute set.

## Complete Solution

Check the `solution4/` directory for the complete implementation.

## Production Considerations

- Search attributes are indexed and queryable
- Use them for business-relevant metadata
- Consider performance impact of complex queries
- Plan search attribute schema for your use case