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
from my_deployer.operators import DockerOperator, SSHOperator
from my_deployer.structs import DockerInfos, SSHInfos


@click.command()
@click.argument("hostname", type=str)
@click.option(
    "--port",
    type=int,
    help='SSH port to use.',
    show_default=True,
    required=False,
    default=22,
)
@click.option(
    "--username",
    help='Remote user username if required.',
    type=str,
    required=False,
)
@click.option(
    "--password",
    help='Remote user password if required.',
    type=str,
    required=False,
)
def config(hostname: str, port: int, username: str, password: str):
    """Configure Docker on the remote host."""
    logger = build_logger('main')
    ssh_infos = SSHInfos(hostname, username, password, port=port)
    logger.info('remote hostname=%s', ssh_infos.hostname)
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
@click.argument("services", type=str, nargs=-1)
@click.option(
    "--tag",
    type=str,
    help='Remote image tag for service(s) to build.',
    required=False,
    default='latest',
)
def build(url: str, services: str, tag: str = 'latest'):
    """Build the Service on the remote host."""
    # TODO: Add progressbar
    logger = build_logger('main')
    infos = DockerInfos(url)
    logger.info('remote hostname=%s', infos.hostname)
    docker_operator = DockerOperator(infos)
    docker_operator.is_remote_reachable()
    for service in services:
        service_path = Path(service)
        name = service_path.absolute().name
        docker_operator.build_service(service_path, name, tag=tag)


@click.command()
@click.argument("url", type=str)
@click.argument("services", type=str, nargs=-1)
@click.option(
    "--tag",
    type=str,
    help='Remote image tag for service(s) to deploy.',
    required=False,
    show_default=True,
    default='latest',
)
def deploy(url: str, services: str, tag: str = 'latest'):
    """Deploy the Service on the remote host."""
    # TODO: Add progressbar
    logger = build_logger('main')
    infos = DockerInfos(url)
    logger.info('remote hostname=%s', infos.hostname)
    docker_operator = DockerOperator(infos)
    docker_operator.is_remote_reachable()
    for service in services:
        service_path = Path(service).absolute()
        image_name = service_path.name
        docker_operator.run_container(
            image_name,
            image_tag=tag,
        )


@click.command()
@click.argument("url", type=str)
@click.argument("services", type=str, nargs=-1)
@click.option(
    "--restart",
    type=bool,
    help='Restart unhealthy containers.',
    default=False,
    is_flag=True,
    show_default=True,
)
def healthcheck(url: str, services: str, restart: bool = False):
    """Ensure the running containers are healthy."""
    logger = build_logger('main')
    infos = DockerInfos(url)
    logger.info('remote hostname=%s', infos.hostname)
    docker_operator = DockerOperator(infos)
    docker_operator.is_remote_reachable()
    docker_operator.list_healthy_containers(restart)
