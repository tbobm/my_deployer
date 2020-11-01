"""Different connectors used to interact with the remote host."""
import logging
import time
from typing import Optional, Tuple, List
from pathlib import Path

import docker
from docker.models.containers import Container
import paramiko

from my_deployer.errors import MyDeployerError
from my_deployer.utils import should_deploy_based_on_version
from my_deployer.logs import build_logger
from my_deployer.remote_commands import INSTALL_DOCKER, ADD_USER_TO_DOCKER_GROUP
from my_deployer.structs import DockerInfos, SSHInfos


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
            self.logger.info('adding user=%s to docker group', user)
            _, _ = self.execute_remote_command(
                ADD_USER_TO_DOCKER_GROUP.format(username=user),
            )
            self.logger.info('added %s to docker group', user)
        return True


class DockerOperator:
    """Execute Docker-related commands on the remote host."""
    DEFAULT_LABELS = {
        'management.tool': 'my_deployer',
    }
    CONTAINER_LABELS = {
        'image': 'my_deployer.app.image',
        'tag': 'my_deployer.app.tag',
    }

    def __init__(self, infos: DockerInfos, logger: Optional[logging.Logger] = None):
        self.client = docker.DockerClient(infos.url)
        if logger is not None:
            self.logger = logger
        else:
            self.logger = build_logger(self.__class__.__name__)
        self.logger.info('setup DockerClient')

    def is_remote_reachable(self) -> bool:
        """Ping the remote Docker daemon."""
        self.logger.info('ping remote target')
        self.client.ping()
        self.logger.info('remote target answered ping')
        return True

    def build_service(self, path: Path, name: str, tag: str = 'latest'):
        """Build the Docker image using self.client."""
        self.logger.info('building from %s with %s:%s', path, name, tag)
        image, _ = self.client.images.build(
            path=path.absolute().as_posix(),
            tag=f"{name}:{tag}",
            labels=self.DEFAULT_LABELS,
        )
        self.logger.info('successfully built service %s:%s (%s)', name, tag, image.id)
        self.logger.info('image=%s size=%d bytes', image.short_id, image.attrs.get('Size'))

    def handle_running_containers(self, image_name: str, image_tag: str) -> List[Container]:
        """Look for and stop the container running using the fully qualified_image."""
        target_labels = {
            'label': [
                f"{self.CONTAINER_LABELS['image']}={image_name}",
            ]
        }
        containers = self.client.containers.list(
            filters=target_labels,
        )
        self.logger.info('looking for existing containers using image=%s', image_name)
        if len(containers) == 0:
            self.logger.info('no previous container')
            return []

        self.logger.info(
            'checking wether or not we should deploy image=%s:%s',
            image_name,
            image_tag,
        )
        older_containers = [
            cont for cont in containers
            if should_deploy_based_on_version(cont.image.tags[0], image_tag)
        ]
        self.logger.info('found %d containers', len(older_containers))
        for container in older_containers:
            self.logger.info(
                'stopping %s (image=%s)',
                container.name,
                container.image.tags[0],
            )
            container.stop()
        return containers

    def _remove_containers(self, containers: List[Container]):
        """Attempt to remove the previous containers."""
        self.logger.info('deleting %d previous containers', len(containers))
        for container in containers:
            container.remove()
            self.logger.debug('deleted container %s', container.id)
        self.logger.info('deleted previous containers')

    def _restore_containers(self, containers: List[Container]):
        """Attempt to restore previous containers."""
        self.logger.info('restoring %d previous containers', len(containers))
        for container in containers:
            container.start()
            self.logger.debug('restored container %s', container.id)
        self.logger.info('restored previous containers')

    def handle_old_containers(self, containers: List[Container], success: bool):
        """Delete or restart previous containers based on success if any."""
        if len(containers) == 0:
            self.logger.info('no previous containers to handle')
            return
        if success:
            self._remove_containers(containers)
        else:
            self._restore_containers(containers)

    def run_container(self,
                      image_name: str,
                      image_tag: str = 'latest',) -> Optional[Container]:
        """Run the container on the remote host.

        - Look for existing containers (looking for similar `image_name`)
        - Try to start the target container
        - Restore or Delete the previous containers if any

        If anything goes wrong while trying to run the target container
        my_deployer tries to restore the previous containers.
        If the deployment goes as expected we delete the old containers.
        """
        # TODO: assert targeted image exists

        # Look for existing containers
        containers = self.handle_running_containers(image_name, image_tag)
        target_image = f"{image_name}:{image_tag}"
        container_labels = {
            **self.DEFAULT_LABELS,
            self.CONTAINER_LABELS['image']: image_name,
            self.CONTAINER_LABELS['tag']: image_tag,
        }
        # Deploy the target container
        self.logger.info('deploying %s:%s', image_name, image_tag)
        try:
            container = self.client.containers.run(
                target_image,
                detach=True,
                labels=container_labels,
            )  # type: Container
            self.logger.info(
                'started container id=%s name=%s',
                container.id,
                container.name,
            )

            # TODO: if healtcheck, wait for "healthy" or set success as False
            success = True
        except docker.errors.DockerException as exc:
            self.logger.error('failed to start container %s', exc)
            success = False
            container = None

        self.handle_old_containers(containers, success)

        return container
