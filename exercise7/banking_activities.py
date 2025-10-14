from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def withdraw(account: str, amount: float) -> str:
    """TODO: Implement withdrawal with error handling for invalid accounts"""
    activity.logger.info(f"Withdrawing ${amount} from account {account}")
    
    # TODO: Add error handling for accounts containing "invalid"
    # Raise ApplicationError with type="InvalidAccount" and non_retryable=True
    
    return f"Withdrew ${amount} from {account}"


@activity.defn
async def deposit(account: str, amount: float) -> str:
    """TODO: Implement deposit with error handling for invalid accounts"""
    activity.logger.info(f"Depositing ${amount} to account {account}")
    
    # TODO: Add error handling for accounts containing "invalid"
    # Raise ApplicationError with type="InvalidAccount" and non_retryable=True
    
    return f"Deposited ${amount} to {account}"


@activity.defn
async def refund(account: str, amount: float) -> str:
    """TODO: Implement refund activity"""
    activity.logger.info(f"Refunding ${amount} to account {account}")
    return f"Refunded ${amount} to {account}"