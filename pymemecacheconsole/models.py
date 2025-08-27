from dataclasses import dataclass
from typing import List


@dataclass
class StorageCommand:
    command: str
    key: str
    flags: int
    exptime: int
    bytes: int
    value: str
    noreply: bool = False


@dataclass
class RetrievalCommand:
    keys: List[str]


@dataclass
class ValueResponse:
    key: str
    flags: int
    bytes: int
    value: str


