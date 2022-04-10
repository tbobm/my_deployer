# My Deployer

[![Base CI](https://github.com/tbobm/my_deployer/actions/workflows/main.yml/badge.svg)](https://github.com/tbobm/my_deployer/actions/workflows/main.yml)

_A lightweight container deployment solution, written in Python._

## Goal

In order to support learning the basics of Containerization principles and starting to code in Python, the "My Deployer" aims to implement the following features:
- Ensure Docker is installed and at the expected version on a remote host
- Provide a simple way of building Docker images on a remote host
- Deploy these images on the remote host by taking in account image version
- Enable upgrading remote containers and reverting failing deployments
- Verify running container healthchecks and restart them if necessary

## Installation

- Clone this repository
- `pip install .`

## Example

```bash
my_deployer config localhost --port 2222 --username vagrant
my_deployer build ssh://vagrant@localhost:2222 examples/hello-world --tag 1.0
my_deployer deploy ssh://vagrant@localhost:2222 examples/hello-world --tag 1.0
```

## Usage

```
my_deployer --help
Usage: my_deployer [OPTIONS] COMMAND [ARGS]...

  Handy lightweight container deployment CLI program.

Options:
  --help  Show this message and exit.

Commands:
  build        Build the Service on the remote host.
  config       Configure Docker on the remote host.
  deploy       Deploy the Service on the remote host.
  healthcheck  Ensure the running containers are healthy.
```


### Config:

The `config` command will:
- SSH using the given arguments
- Install or update Docker on the remote host

```
my_deployer config --help
Usage: my_deployer config [OPTIONS] HOSTNAME

  Configure Docker on the remote host.

Options:
  --port INTEGER   SSH port to use.  [default: 22]
  --username TEXT  Remote user username if required.
  --password TEXT  Remote user password if required.
  --help           Show this message and exit.
```

### Build:

The `build` command will:
- Connect to the Docker socket through the `url` (i.e.: `ssh`-based URL)
- Build a Docker image on the remote host
- Tag this image using if the corresponding flag is set

```
my_deployer build --help
Usage: my_deployer build [OPTIONS] URL [SERVICES]...

  Build the Service on the remote host.

Options:
  --tag TEXT  Remote image tag for service(s) to build.
  --help      Show this message and exit.
```

### Deploy:

The `deploy` command will:
- Look for existing services
- Stop these services
- Try to run a container using the service image with the given tag if specified
- Restore or remove the previous containers if any

```
my_deployer deploy --help
Usage: my_deployer deploy [OPTIONS] URL [SERVICES]...

  Deploy the Service on the remote host.

Options:
  --tag TEXT  Remote image tag for service(s) to deploy.  [default: latest]
  --help      Show this message and exit.
```

### Healthcheck:

The `healthcheck` command will:
- List every container's healthcheck if any
- Restart every unhealthy container if asked

```
my_deployer healthcheck --help
Usage: my_deployer healthcheck [OPTIONS] URL [SERVICES]...

  Ensure the running containers are healthy.

Options:
  --restart  Restart unhealthy containers.  [default: False]
  --help     Show this message and exit.
```


## Tasks

### Communication

With the host:
- [x] Access a remote host using SSH
- [x] Connect to the remote Docker client

With the user:
- [x] Provide a friendly logging interface
- [ ] \(_optional): Enable a verbose mode (0 or 1) to display remote log_

### Config

> Ensure Docker is installed and at the expected version on a remote host.

- [x] Enquire about the currently installed Docker version, if any
- [x] Install or upgrade Docker to expected version if necessary
- [ ] \(_optional): Display informations about the Docker configuration_

### Build

> Provide a simple way of building Docker images on a remote host

- [x] Build the Docker image with the corresponding values
- [x] \(_optional): Generate some metadatas and display them_

### Deploy

> Deploy these images on the remote host by taking in account image version
- Enable upgrading remote containers and reverting failing deployments

- [x] Enquire if the specified image is already deployed and which version -if any- it is using
- [x] Deploy the newly built image (or a specified one) if necessary
- [x] If an already built container exists, stop it and restore it if the one getting deployed fails
- [x] Delete previous container if the new one is succesful and healthy

### Healthcheck

> Verify running container healthchecks and restart them if necessary

- [x] List every container's healthcheck status
- [x] If specified, restart the unhealthy containers
