import random
from temporalio import activity


@activity.defn
async def withdraw(account: str, amount: float) -> None:
    # TODO: Implement withdrawal activity
    # - Log the withdrawal operation
    # - Add 10% chance of failure with RuntimeError("Withdrawal failed - insufficient funds")
    pass


@activity.defn
async def deposit(account: str, amount: float) -> None:
    # TODO: Implement deposit activity
    # - Log the deposit operation
    # - Add 5% chance of failure with RuntimeError("Deposit failed - account not found")
    pass


@activity.defn
async def refund(account: str, amount: float) -> None:
    # TODO: Implement refund activity
    # - Log the refund operation
    # - This should not fail
    pass