"""Unit tests for my_deployer's entrypoint."""
from my_deployer import structs


def test_integrity():
    """Ensure the tests are properly configured."""
    assert True


def test_ssh_struct():
    """Base SSHInfos test."""
    sshinfos = {
        'username': 'bob',
        'password': 'password',
        'hostname': '127.0.0.1',
    }
    infos = structs.SSHInfos(**sshinfos)
    assert infos is not None
    assert infos.port == 22
    assert infos.username == 'bob'
    assert infos.hostname == '127.0.0.1'
