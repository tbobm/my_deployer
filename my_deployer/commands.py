"""My Deployer's subcommands definitions.

The program must implement the following:
    config: Configure Docker on the remote host
    build: Build the <service> Docker image on the remote host
    deploy: Run the <service> on the remote host
    healthcheck: Enquire about the remote container statuses
"""
from pathlib import Path

import click

from my_deployer.logs import build_logger
from my_deployer.operators import SSHOperator, DockerOperator
from my_deployer.structs import SSHInfos


@click.command()
@click.argument("hostname", type=str)
@click.option("--port", type=int, required=False, default=22)
@click.option("--username", type=str, required=False)
@click.option("--password", type=str, required=False)
def config(hostname: str, port: int, username: str, password: str):
    """Configure Docker on the remote host."""
    logger = build_logger('main')
    ssh_infos = SSHInfos(hostname, username, password, port=port)
    remote = SSHOperator(ssh_infos)
    logger.info('check if docker is installed')
    docker_installed = remote.is_docker_installed()
    logger.info(
        'docker is %sinstalled',
        "" if docker_installed else 'not ',
    )
    if not docker_installed:
        remote.install_docker()
        return

    logger.info('check if docker is up-to-date')
    docker_up_to_date = remote.is_docker_up_to_date()
    logger.info(
        'docker is %sup_to_date',
        "" if docker_up_to_date else 'not ',
    )
    if not docker_up_to_date:
        remote.install_docker()


@click.command()
@click.argument("url", type=str)
@click.argument("service", type=str)
@click.option("--name", type=str, required=False)
@click.option("--tag", type=str, required=False, default='latest')
def build(url: str, service: str, name: str = None, tag: str = 'latest'):
    """Build the Service on the remote host."""
    # TODO: Add progressbar
    logger = build_logger('main')
    # TODO: Add DockerInfos structure to display host
    docker_operator = DockerOperator(url)
    docker_operator.is_remote_reachable()
    # TODO: Build multiple services
    service_path = Path(service)
    if name is None:
        name = service_path.absolute().name
        logger.info("using default name=%s", name)
    docker_operator.build_service(service_path, name, tag=tag)


@click.command()
@click.argument("url", type=str)
@click.argument("service", type=str)
@click.option("--container-name", type=str, required=False)
@click.option("--tag", type=str, required=False, default='latest')
def deploy(url: str, service: str, container_name: str = None, tag: str = 'latest'):
    """Deploy the Service on the remote host."""
    # TODO: Add progressbar
    logger = build_logger('main')
    # TODO: Add DockerInfos structure to display host
    docker_operator = DockerOperator(url)
    docker_operator.is_remote_reachable()
    # TODO: Build multiple services
    docker_operator.run_container(
        service,
        image_tag=tag,
        container_name=container_name,
    )
