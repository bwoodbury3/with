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
    cmd_args = " ".join(cmd_args)

    # Run!
    out = subprocess.run(
        ["/bin/bash", command.WITH_SCRIPT, withfile, context, cmd_args, executable]
    )
    return out.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", type=str, choices=command.discover(), help="The context to enter"
    )
    parser.add_argument(
        "args", nargs="*", type=str, help="Args to pass to the subcommand"
    )
    parser.add_argument(
        "--executable",
        "-e",
        nargs="?",
        type=str,
        default="",
        help="Full executable to run in this context. If unspecified, will drop the user into an interactive shell",
    )
    args = parser.parse_args()
    sys.exit(run(args.command, args.args, args.executable))


if __name__ == "__main__":
    main()
