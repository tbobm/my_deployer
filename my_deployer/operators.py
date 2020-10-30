"""Different connectors used to interact with the remote host."""
import logging
import time
from typing import Optional, Tuple
from pathlib import Path

import docker
import paramiko

from my_deployer.errors import MyDeployerError
from my_deployer.logs import build_logger
from my_deployer.remote_commands import INSTALL_DOCKER, ADD_USER_TO_DOCKER_GROUP
from my_deployer.structs import SSHInfos


GET_DOCKER_VERSION_CMD = 'docker -v'


class SSHOperator:
    """Allow to execute command on a remote host."""

    def __init__(self, infos: SSHInfos, logger: Optional[logging.Logger] = None):
        self.client = paramiko.client.SSHClient()
        self.infos = infos
        self.client.load_system_host_keys()
        self.client.connect(
            infos.hostname,
            port=infos.port,
            username=infos.username,
            password=infos.password,
        )
        if logger is not None:
            self.logger = logger
        else:
            self.logger = build_logger(self.__class__.__name__)
        self.logger.info('setup SSHClient targeting %s', infos.hostname)

    def execute_remote_command(self, commands: str, allow_fail=False) -> Tuple[str, str]:
        """Execute `commands` using SSHClient's exec_command."""
        self.logger.debug(commands)
        _, stdout, stderr = self.client.exec_command(commands)
        while not stdout.channel.exit_status_ready():
            time.sleep(0.1)
        # NOTE: might be a great idea to manager result code here
        result = stdout.channel.recv_exit_status()
        self.logger.debug('command result=%d', result)
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        if result != 0 and not allow_fail:
            self.logger.error('could not fetch docker version:\n%s', err)
            raise MyDeployerError()
        return (out, err)

    def is_docker_installed(self) -> bool:
        """Execute `docker -v` on the remote host and analyze output."""
        # TODO: Cache output in order to prevent from querying version twice
        _, stderr = self.execute_remote_command(
            GET_DOCKER_VERSION_CMD,
            allow_fail=True,
        )
        docker_is_missing = not stderr
        return docker_is_missing

    def is_docker_up_to_date(self, version: str = '19.03') -> bool:
        """Execute `docker -v` on the remote host and analyze output."""
        self.logger.debug('Ensure remote has matching version=%s', version)
        stdout, _ = self.execute_remote_command(GET_DOCKER_VERSION_CMD)
        up_to_date = version in stdout
        return up_to_date

    def install_docker(self, add_current_user_to_docker_group: bool = True) -> bool:
        """Install latest docker version using SSH and add user to docker group."""
        self.logger.info('installing docker on remote')
        _, _ = self.execute_remote_command(";".join(INSTALL_DOCKER))
        self.logger.info('docker successfully installed')
        if add_current_user_to_docker_group:
            user = self.infos.username
            self.logger.info('adding user=%s to docker group')
            _, _ = self.execute_remote_command(
                ADD_USER_TO_DOCKER_GROUP.format(username=user),
            )
            self.logger.info('added %s to docker group', user)
        return True


class DockerOperator:
    """Execute Docker-related commands on the remote host."""

    def __init__(self, url: str, logger: Optional[logging.Logger] = None):
        self.client = docker.DockerClient(url)
        if logger is not None:
            self.logger = logger
        else:
            self.logger = build_logger(self.__class__.__name__)
        self.logger.info('setup DockerClient')

    def build_service(self, path: Path, name: str, tag: str = 'latest'):
        """Build the Docker image using self.client."""
        self.logger.info('building from %s with %s:%s', path, name, tag)
        image, _ = self.client.images.build(path=path, tag=f"{name}:{tag}")
        self.logger.info('successfully built service %s:%s (%s)', name, tag, image.id)
        self.logger.info('image=%s size=%d bytes', image.short_id, image.attrs.get('Size'))

    def run_container(self, image_name: str, image_tag: str = 'latest'):
        """Run the container on the remote host."""
