"""Utility structures for My Deployer."""
from dataclasses import dataclass, field
import typing


@dataclass
class SSHInfos:
    """Centralize SSH informations."""
    hostname: str
    username: typing.Optional[str]
    password: typing.Optional[str] = field(repr=False)
    port: int = 22
