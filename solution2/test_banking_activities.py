from unittest.mock import patch

import pytest
from temporalio.testing import ActivityEnvironment

from banking_activities import deposit, refund, withdraw


@pytest.mark.asyncio
async def test_withdraw_succeeds_when_the_dice_are_kind():
    # random.random() >= 0.1, so the simulated failure does not trigger.
    with patch("random.random", return_value=0.5):
        await ActivityEnvironment().run(withdraw, "account-123", 100.0)


@pytest.mark.asyncio
async def test_withdraw_raises_on_insufficient_funds():
    with patch("random.random", return_value=0.05):
        with pytest.raises(RuntimeError, match="insufficient funds"):
            await ActivityEnvironment().run(withdraw, "account-123", 100.0)


@pytest.mark.asyncio
async def test_deposit_succeeds_when_the_dice_are_kind():
    with patch("random.random", return_value=0.5):
        await ActivityEnvironment().run(deposit, "account-456", 100.0)


@pytest.mark.asyncio
async def test_deposit_raises_when_the_account_is_missing():
    with patch("random.random", return_value=0.01):
        with pytest.raises(RuntimeError, match="account not found"):
            await ActivityEnvironment().run(deposit, "account-456", 100.0)


@pytest.mark.asyncio
async def test_refund_never_fails():
    """The compensating activity has no simulated failure, by design."""
    with patch("random.random", return_value=0.0):
        await ActivityEnvironment().run(refund, "account-123", 100.0)
