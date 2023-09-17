"""
Main entrypoint.
"""

import argparse
import os
import random
import shutil
import stat
import subprocess
import sys
from typing import List

import command


TAB_COMPLETE_DIRS = [
    "/etc/bash_completion.d/",  # Linux
    "/usr/local/etc/bash_completion.d/",  # MacOS
]
"""
Possible locations for tab complete.
"""


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

    # Run!
    out = subprocess.run(
        ["/bin/bash", command.WITH_SCRIPT, withfile, context, cmd_args_arg, executable]
    )
    return out.returncode


def commands() -> int:
    """
    Print the full list of available commands.

    Return: exit code.
    """
    commands = command.discover()
    print(" ".join(commands))
    return 0


def install_tab_complete() -> int:
    """
    Install tab completion.

    Return: exit code.
    """
    # Check if the user is running as root (sudo)
    if os.geteuid() != 0:
        print("You need root privileges to install tab completion.")
        return 1

    completion_script = command.APP_DIR / "with-completion.sh"

    # Check if the completion script exists
    if not os.path.exists(completion_script):
        print(f"Completion script '{completion_script}' not found.")
        return 1

    # Copy the completion script to the tab completion directory
    for directory in TAB_COMPLETE_DIRS:
        if os.path.exists(directory) and os.path.isdir(directory):
            dest_path = os.path.join(directory, os.path.basename(completion_script))
            shutil.copy(completion_script, dest_path)
            os.chmod(
                dest_path,
                stat.S_IRUSR
                | stat.S_IWUSR
                | stat.S_IRGRP
                | stat.S_IROTH
                | stat.S_IXUSR
                | stat.S_IXGRP
                | stat.S_IXOTH,
            )
            print(f"Tab completion installed successfully to {dest_path}")
            break

    return 0


OTHER_COMMANDS = {"commands": commands, "install-tab-complete": install_tab_complete}


def main():
    commands = command.discover() + list(OTHER_COMMANDS.keys())

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
    parser.add_argument(
        "--all-commands", action="store_true", help="Print all available commands"
    )
    args = parser.parse_args()

    if args.command in OTHER_COMMANDS:
        func = OTHER_COMMANDS[args.command]
        sys.exit(func())

    sys.exit(run(args.command, args.args, args.executable))


if __name__ == "__main__":
    main()
