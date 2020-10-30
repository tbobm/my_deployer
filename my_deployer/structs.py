"""Utility structures for My Deployer."""
from dataclasses import dataclass
import typing


@dataclass
class SSHInfos:
    """Centralize SSH informations."""
    hostname: str
    username: typing.Optional[str]
    password: typing.Optional[str]
    port: int = 22
    # TODO: Edit repr to avoid showing password (replace by '*' ?)
