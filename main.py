"""
Main entrypoint.
"""

import argparse
import os
import random
import subprocess
import sys
from typing import List

import command


WITH_DEPTH = "WITH_DEPTH"
"""
The environment variable holding the with depth.
"""


def increment_depth() -> int:
    """
    Increment the depth environment variable. Do our best to clean up a bad
    state here, but there's only so much we can do.

    Returns: The context depth.
    """
    depth_var = os.environ.get(WITH_DEPTH, "0")
    if not depth_var.isdigit():
        depth_var = "0"

    new_depth = int(depth_var) + 1
    os.environ[WITH_DEPTH] = str(new_depth)
    return new_depth


def decrement_depth() -> int:
    """
    Decrement the depth environment variable. Do our best to clean up a bad
    state here, but there's only so much we can do.

    Returns: The context depth.
    """
    # Assume 1 if it's not present so that we can decrement.
    depth_var = os.environ.get(WITH_DEPTH, "1")
    if not depth_var.isdigit():
        depth_var = "1"

    new_depth = max(int(depth_var) - 1, 0)
    os.environ[WITH_DEPTH] = str(new_depth)
    return new_depth


def run(with_command: str, cmd_args: List[str], executable: str) -> int:
    """
    Run a WITH command.

    Args:
        with_command: The WITH command to execute.
        cmd_args: The args to pass to the WITH command.
        executable: The executable to run inside the WITH context.

    Return: exit code.
    """
    withfile = command.cmd_to_filename(with_command)
    context = hex(random.randint(0, 2**32)).lstrip("0x")
    if not cmd_args:
        cmd_args = []
    cmd_args_arg = f"{' '.join(cmd_args)}"

    depth = increment_depth()
    print(f">> Context depth: {depth}")

    # Run!
    out = subprocess.run(
        ["/bin/bash", command.WITH_SCRIPT, withfile, context, cmd_args_arg, executable]
    )

    depth = decrement_depth()
    print(f">> Context depth: {depth}")

    return out.returncode


def main():
    commands = command.discover()

    epilog = "Available contexts: " + ", ".join(commands)
    parser = argparse.ArgumentParser(prog="with", epilog=epilog)
    parser.add_argument(
        "command", type=str, choices=commands, help="The context to enter"
    )
    parser.add_argument(
        "--args", "-a", nargs="*", type=str, help="Args to pass to the subcommand"
    )
    parser.add_argument(
        "--executable",
        "-e",
        type=str,
        default="",
        help="Full executable to run in this context. If unspecified, will drop the user into an interactive shell",
    )
    args = parser.parse_args()
    sys.exit(run(args.command, args.args, args.executable))


if __name__ == "__main__":
    main()
