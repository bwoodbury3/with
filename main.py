"""
Main entrypoint.
"""

import argparse
import random
import subprocess
import sys
from typing import List

import command


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
    cmd_args_arg = f"\"{' '.join(cmd_args)}\""

    # Run!
    out = subprocess.run(
        ["/bin/bash", command.WITH_SCRIPT, withfile, context, cmd_args_arg, executable]
    )
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
