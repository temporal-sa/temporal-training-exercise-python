# Exercise 6 Solution: Unit Testing Temporal Workflows

## test_money_transfer_workflow.py

```python
# In test_approved_transfer method:

# Test initial state using get_transfer_state query
state = await handle.query(MoneyTransferWorkflow.get_transfer_state)
assert state == "IN_PROGRESS"

# Test initial step using get_current_step query  
step = await handle.query(MoneyTransferWorkflow.get_current_step)
assert step in ["WITHDRAWING", "WAITING_FOR_APPROVAL"]

# Test final state using get_transfer_state query
final_state = await handle.query(MoneyTransferWorkflow.get_transfer_state)
assert final_state == "COMPLETED"

# Test final step using get_current_step query
final_step = await handle.query(MoneyTransferWorkflow.get_current_step)
assert final_step == "COMPLETED"

# Assert the result message
assert result == "Transfer completed successfully"
```

```python
# In test_rejected_transfer method:

# Check state before approval using get_transfer_state query
state = await handle.query(MoneyTransferWorkflow.get_transfer_state)
assert state == "IN_PROGRESS"

# Check final state after rejection using get_transfer_state query
final_state = await handle.query(MoneyTransferWorkflow.get_transfer_state)
assert final_state == "REJECTED"

# Check final step using get_current_step query
final_step = await handle.query(MoneyTransferWorkflow.get_current_step)
assert final_step == "REFUNDED"

# Assert the result message
assert result == "Transfer rejected and refunded"
```

## test_banking_activities.py

```python
# In test_withdraw_success method:
await env.run(withdraw, "account-001", 100.0)

# In test_withdraw_failure method:
with pytest.raises(RuntimeError, match="Withdrawal failed - insufficient funds"):
    await env.run(withdraw, "account-001", 100.0)

# In test_deposit_success method:
await env.run(deposit, "account-002", 100.0)

# In test_deposit_failure method:
with pytest.raises(RuntimeError, match="Deposit failed - account not found"):
    await env.run(deposit, "account-002", 100.0)

# In test_refund_success method:
await env.run(refund, "account-001", 100.0)
```

## Key Testing Concepts

- **ActivityEnvironment**: Isolated environment for testing individual activities
- **WorkflowEnvironment**: Full environment for testing workflows with activities
- **Mocking**: Control random behavior for predictable test outcomes
- **Query Testing**: Verify workflow state at different execution points
- **Exception Testing**: Use `pytest.raises()` to test error conditions
- **Signal Testing**: Test workflow interaction through external signals