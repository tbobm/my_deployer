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
> `my_deployer config <REMOTE_IP>`

Build:
> `my_deployer build <REMOTE_IP> [<SERVICE>]...`

Deploy:
> `my_deployer deploy <REMOTE_IP> <SERVICE>...`

Healthcheck:
> `my_deployer healthcheck <REMOTE_IP> [<SERVICE>]...`


## Features

### Communication

With the host:
- [ ] Access a remote host using SSH

With the user:
- [ ] Provide a friendly logging interface
- [ ] \(_optional): Enable a verbose mode (0 or 1) to display remote log_

### Config

> Ensure Docker is installed and at the expected version on a remote host.

- [ ] Enquire about the currently installed Docker version, if any
- [ ] Install or upgrade Docker to expected version if necessary
- [ ] \(_optional): Display informations about the Docker configuration_

### Build

> Provide a simple way of building Docker images on a remote host

- [ ] Ensure the directory contains the necessary files (Dockerfile)
- [ ] \(_optional): Create a temporary working directory (`/tmp/my-deployer-{uid}`)_
- [ ] Copy the corresponding directory to the remote host
- [ ] \(_optional): Cleanup temporary working directory_
- [ ] Build the Docker image with the corresponding values
- [ ] \(_optional): Generate some metadatas and display them_

### Deploy

> Deploy these images on the remote host by taking in account image version
- Enable upgrading remote containers and reverting failing deployments

- [ ] Enquire if the specified image is already deployed and which version -if any- it is using
- [ ] Deploy the newly built image (or a specified one) if necessary
- [ ] If an already built container exists, stop it and restore it if the one getting deployed fails
- [ ] Delete previous container if the new one is succesful and healthy

### Healthcheck

> Verify running container healthchecks and restart them if necessary

- [ ] List every container's healthcheck status
- [ ] If specified, restart the unhealthy containers
