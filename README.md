# My Deployer

_A lightweight container deployment solution, written in Python._

## Goal

In order to support learning the basics of Containerization principles and starting to code in Python, the "My Deployer" aims to implement the following features:
- Ensure Docker is installed and at the expected version on a remote host
- Provide a simple way of building Docker images on a remote host
- Deploy these images on the remote host by taking in account image version
- Enable upgrading remote containers and reverting failing deployments
- Verify running container healthchecks and restart them if necessary

## Usage

**Write the code first!**

Config:
> `my_deployer config <SSH_REMOTE_URL>`

Build:
> `my_deployer build <SSH_REMOTE_URL> [<SERVICE>]...`

Deploy:
> `my_deployer deploy <SSH_REMOTE_URL> <SERVICE>...`

Healthcheck:
> `my_deployer healthcheck <REMOTE_IP> [<SERVICE>]...`


## Features

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
