"""Unit tests for my_deployer's entrypoint."""
import pytest

from my_deployer import client


def test_base_answer():
    """Ensure the client does not do anything."""
    with pytest.raises(NotImplementedError):
        client.run_cli()
