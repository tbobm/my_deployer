"""My Deployer custom Exceptions.

Allow to catch internal runtime errors scoped to the My Deployer API.
"""


class MyDeployerError(Exception):
    """Internal Error used when running commands."""
