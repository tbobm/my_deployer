"""Bash scripts to execute on remote host."""

INSTALL_DOCKER = [
    'apt-get update',
    'apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common',
    'curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -',
    'add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable"',
    'sudo apt-get update',
    'sudo apt-get install docker-ce docker-ce-cli containerd.io',
]
