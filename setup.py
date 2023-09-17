#!/usr/bin/env python3

from setuptools import setup

setup(
    name="with",
    version="1.0",
    entry_points={
        "console_scripts": ["with=main:main"],
    },
    description="Command line context manager",
    author="Brian Woodbury",
)
