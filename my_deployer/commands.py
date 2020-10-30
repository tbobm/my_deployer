"""My Deployer's subcommands definitions.

The program must implement the following:
    config: Configure Docker on the remote host
    build: Build the <service> Docker image on the remote host
    deploy: Run the <service> on the remote host
    healthcheck: Enquire about the remote container statuses
"""
import click

from my_deployer.operators import SSHOperator


@click.command()
@click.argument("hostname", type=str)
@click.option("--port", type=int, required=False, default=22)
@click.option("--username", type=str, required=False)
@click.option("--password", type=str, required=False)
def config(hostname: str, port: int, username: str, password: str):
    """Configure Docker on the remote host."""
    remote = SSHOperator(hostname, port, username, password)
    # ensure docker is installed
    docker_installed = remote.is_docker_installed()
    if not docker_installed:
        remote.install_docker()
    docker_up_to_date = remote.is_docker_up_to_date()
    if not docker_up_to_date:
        remote.install_docker()  # NOTE: Or remote.upgrade_docker


@click.command()
def build():
    """Build the Service on the remote host."""
