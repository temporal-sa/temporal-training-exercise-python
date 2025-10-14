import random
from temporalio import activity


@activity.defn
async def withdraw(account: str, amount: float) -> None:
    activity.logger.info(f"Withdrawing ${amount} from account {account}")
    if random.random() < 0.1:
        raise RuntimeError("Withdrawal failed - insufficient funds")


@activity.defn
async def deposit(account: str, amount: float) -> None:
    activity.logger.info(f"Depositing ${amount} to account {account}")
    if random.random() < 0.05:
        raise RuntimeError("Deposit failed - account not found")


@activity.defn
async def refund(account: str, amount: float) -> None:
    activity.logger.info(f"Refunding ${amount} to account {account}")