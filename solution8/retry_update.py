from dataclasses import dataclass


@dataclass
class RetryUpdate:
    key: str
    value: str
