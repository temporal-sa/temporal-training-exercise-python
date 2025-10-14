from dataclasses import dataclass


@dataclass
class TransferRequest:
    from_account: str
    to_account: str
    amount: float
    transfer_id: str