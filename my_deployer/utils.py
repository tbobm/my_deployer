"""Utility functions for my_deployer program."""
from packaging.version import parse


def should_deploy_based_on_version(reference: str, target: str, allow_eq: bool = False) -> bool:
    """Return if the target is greater than the reference.

    Setting allow_eq=True will skip deployment if existing version is running.
    Otherwise, re-deploy on same image version.
    """
    ref_version = parse(reference)
    target_version = parse(target)
    if allow_eq:
        return target_version > ref_version
    return target_version >= ref_version
