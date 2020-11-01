"""Unit tests for my_deployer's entrypoint."""
import pytest

from my_deployer import structs
from my_deployer import utils


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


@pytest.mark.parametrize('reference,target,allow_eq,expected', [
    ('1.0.0', '2.0.0', True, True),
    ('v1.0.0', '1.1.0', True, True),
    ('1.0-rc', '0.9', True, False),
    ('1.0', '1.0', False, True),
    ])
def test_compare_version(reference: str, target: str, allow_eq: bool, expected: bool):
    """Ensure common version comparison is correct."""
    res = utils.should_deploy_based_on_version(reference, target, allow_eq)
    assert res is expected
