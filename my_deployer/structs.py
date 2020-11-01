"""Utility structures for My Deployer."""
from dataclasses import dataclass, field
from urllib import parse
import typing


@dataclass
class SSHInfos:
    """Centralize SSH informations."""
    hostname: str
    username: typing.Optional[str]
    password: typing.Optional[str] = field(repr=False)
    port: int = 22


@dataclass
class DockerInfos:
    """Manage Docker connection informations."""
    url: str = field(repr=False)
    hostname: str = field(init=False)
    scheme: str = field(init=False)

    def __post_init__(self):
        parsed = parse.urlparse(self.url)
        self.hostname = parsed.hostname
        self.scheme = parsed.scheme
