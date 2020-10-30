"""Different connectors used to interact with the remote host."""
import paramiko

from my_deployer.remote_commands import INSTALL_DOCKER


GET_DOCKER_VERSION_CMD = 'docker -v'


class SSHOperator:
    """Allow to execute command on a remote host."""

    def __init__(self, hostname: str, port: int, username: str, password: str):
        self.client = paramiko.client.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(hostname, port=port, username=username, password=password)
        print(self.client)


    def execute_remote_command(self, commands: str):
        """Execute `commands` using SSHClient's exec_command."""
        _, stdout, stderr = self.client.exec_command(commands)
        return (stdout.read().decode('utf-8'), stderr.read().decode('utf-8'))

    def is_docker_installed(self) -> bool:
        """Execute `docker -v` on the remote host and analyze output."""
        _, stderr = self.execute_remote_command(GET_DOCKER_VERSION_CMD)
        docker_is_missing = not stderr
        return docker_is_missing

    def is_docker_up_to_date(self, version: str = '19.03') -> bool:
        """Execute `docker -v` on the remote host and analyze output."""
        _, stdout, _ = self.client.exec_command(GET_DOCKER_VERSION_CMD)
        return version in stdout

    def install_docker(self) -> bool:
        """Execute `docker -v` on the remote host and analyze output."""
        _, stdout, stderr = self.client.exec_command(";".join(INSTALL_DOCKER))
        print(stdout)
        print('err:', stderr)
        # TODO: Install docker in blockking mode
        # TODO: Allow to add a user to Docker group
        return True
