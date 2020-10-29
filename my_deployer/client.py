"""Definition of my_deployer's CLI entrypoint.

.. code-block:: bash

   $ my_deployer config <REMOTE_IP>
   $ my_deployer build <REMOTE_IP> [<SERVICE>]...
   $ my_deployer deploy <REMOTE_IP> <SERVICE>...
   $ my_deployer healthcheck <REMOTE_IP> [<SERVICE>]...

"""


def run_cli():
    """Execute the command using the CLI flags."""
    raise NotImplementedError()


if __name__ == '__main__':
    run_cli()
