"""Definition of my_deployer's CLI entrypoint.

.. code-block:: bash

   $ my_deployer config <REMOTE_IP>
   $ my_deployer build <REMOTE_IP> [<SERVICE>]...
   $ my_deployer deploy <REMOTE_IP> <SERVICE>...
   $ my_deployer healthcheck <REMOTE_IP> [<SERVICE>]...

"""
import click

from my_deployer.commands import config, build


@click.group()
def my_deployer():
    """Handy lightweight container deployment CLI program."""


def run_cli():
    """Execute the command using the CLI flags."""
    my_deployer.add_command(config)
    my_deployer.add_command(build)
    my_deployer()


if __name__ == '__main__':
    run_cli()
