"""Bash scripts to execute on remote host."""

# NOTE: hard-coding `sudo` is bad
INSTALL_DOCKER = [
    'sudo apt-get update',
    'sudo apt-get install -y apt-transport-https ca-certificates curl \
    gnupg-agent software-properties-common',
    'curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -',
    'sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable"',
    'sudo apt-get update',
    'sudo apt-get install -y docker-ce docker-ce-cli containerd.io',
]

ADD_USER_TO_DOCKER_GROUP = 'sudo usermod -aG docker {username}'
