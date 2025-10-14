import pytest
from unittest.mock import patch
from temporalio.testing import ActivityEnvironment

from .banking_activities import withdraw, deposit, refund


class TestBankingActivities:
    
    @pytest.mark.asyncio
    async def test_withdraw_success(self):
        """Test successful withdrawal"""
        with patch('random.random', return_value=1):  # No failure
            env = ActivityEnvironment()
            await env.run(withdraw, "account-001", 100.0)
    
    @pytest.mark.asyncio
    async def test_withdraw_failure(self):
        """Test withdrawal failure due to insufficient funds"""
        with patch('random.random', return_value=0.01):  # Trigger failure
            env = ActivityEnvironment()
            with pytest.raises(RuntimeError, match="Withdrawal failed - insufficient funds"):
                await env.run(withdraw, "account-001", 100.0)
    
    @pytest.mark.asyncio
    async def test_deposit_success(self):
        """Test successful deposit"""
        with patch('random.random', return_value=1):  # No failure
            env = ActivityEnvironment()
            await env.run(deposit, "account-002", 100.0)
    
    @pytest.mark.asyncio
    async def test_deposit_failure(self):
        """Test deposit failure due to account not found"""
        with patch('random.random', return_value=0.01):  # Trigger failure
            env = ActivityEnvironment()
            with pytest.raises(RuntimeError, match="Deposit failed - account not found"):
                await env.run(deposit, "account-002", 100.0)
    
    @pytest.mark.asyncio
    async def test_refund_success(self):
        """Test successful refund (never fails)"""
        env = ActivityEnvironment()
        await env.run(refund, "account-001", 100.0)
