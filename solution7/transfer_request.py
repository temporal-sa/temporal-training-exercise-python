from dataclasses import dataclass, replace


@dataclass
class TransferRequest:
    from_account: str
    to_account: str
    amount: float
    reference_id: str