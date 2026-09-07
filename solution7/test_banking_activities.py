import pytest
from temporalio.exceptions import ApplicationError
from temporalio.testing import ActivityEnvironment

from banking_activities import deposit, refund, withdraw


@pytest.mark.asyncio
async def test_withdraw_succeeds_for_a_valid_account():
    result = await ActivityEnvironment().run(withdraw, "account-123", 100.0)

    assert result == "Withdrew $100.0 from account-123"


@pytest.mark.asyncio
async def test_withdraw_rejects_an_invalid_account_without_retrying():
    with pytest.raises(ApplicationError) as caught:
        await ActivityEnvironment().run(withdraw, "invalid-account", 100.0)

    # Non-retryable, so Temporal hands the failure straight to the workflow
    # instead of burning through a retry policy on input that cannot succeed.
    assert caught.value.non_retryable
    assert caught.value.type == "InvalidAccount"


@pytest.mark.asyncio
async def test_deposit_succeeds_for_a_valid_account():
    result = await ActivityEnvironment().run(deposit, "account-456", 100.0)

    assert result == "Deposited $100.0 to account-456"


@pytest.mark.asyncio
async def test_deposit_rejects_an_invalid_account_without_retrying():
    with pytest.raises(ApplicationError) as caught:
        await ActivityEnvironment().run(deposit, "invalid-account", 100.0)

    assert caught.value.non_retryable
    assert caught.value.type == "InvalidAccount"


@pytest.mark.asyncio
async def test_refund_accepts_any_account():
    """The compensating activity has no validation, so it cannot strand funds."""
    result = await ActivityEnvironment().run(refund, "invalid-account", 100.0)

    assert result == "Refunded $100.0 to invalid-account"
