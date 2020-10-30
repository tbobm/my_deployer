"""Packaging file for my_deployer."""
from distutils.core import setup

from setuptools import find_packages


__version__ = "0.0.0"
URL = "https://github.com/tbobm/my_deployer/archive/{}.tar.gz".format(__version__)

setup(
    name="my_deployer",
    packages=["my_deployer"],
    install_requires=['click'],
    version=__version__,
    description="A lightweight container deployment solution, written in Python",
    author="Theo 'Bob' Massard",
    author_email="tbobm@protonmail.com",
    url="https://github.com/tbobm/my_deployer",
    download_url=URL,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
    ],
    entry_points={
        "console_scripts": [
            "my_deployer=my_deployer.client:run_cli",
        ],
    },
)
