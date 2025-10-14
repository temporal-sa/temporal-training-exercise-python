from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def withdraw(account: str, amount: float) -> str:
    activity.logger.info(f"Withdrawing ${amount} from account {account}")
    
    if "invalid" in account:
        raise ApplicationError(
            f"Invalid fromAccount ID: {account}",
            type="InvalidAccount",
            non_retryable=True,
        )

    return f"Withdrew ${amount} from {account}"


@activity.defn
async def deposit(account: str, amount: float) -> str:    
    activity.logger.info(f"Depositing ${amount} to account {account}")
    
    if "invalid" in account:
        raise ApplicationError(
            f"Invalid toAccount ID: {account}",
            type="InvalidAccount",
            non_retryable=True,
        )
    
    return f"Deposited ${amount} to {account}"


@activity.defn
async def refund(account: str, amount: float) -> str:
    activity.logger.info(f"Refunding ${amount} to account {account}")
    return f"Refunded ${amount} to {account}"
