"""
Command discovery, collection, execution
"""

import os
import pathlib
from typing import List


APP_DIR = pathlib.Path(__file__).parent.resolve()
"""
The main application directory.
"""

USER_WITHFILES = f"{os.path.expanduser('~')}/.with"
"""
Path to user-defined withfiles.
"""

BUILTIN_WITHFILES = APP_DIR / "builtin"
"""
Path to builtin withfiles.
"""

WITH_PATH = [USER_WITHFILES, BUILTIN_WITHFILES]
"""
PATH for searching withfiles.
"""

WITH_SCRIPT = APP_DIR / "with.sh"
"""
The path to the main with script executable.
"""

SHELL_SUFFIX = ".sh"
"""
Shell suffix. All withfiles are shell commands
"""


def cmd_to_filename(command: str) -> str:
    """
    Returns the filename associated with the user command.
    Returns None if no filename corresponds to that command.

    Args:
        command: The command name.

    Returns: The fq path to the provided command, or None.
    """
    for dir in WITH_PATH:
        filename = os.path.join(dir, f"{command}{SHELL_SUFFIX}")
        if os.path.exists(filename) and os.path.isfile(filename):
            return filename
    return None


def filename_to_cmd(filename: str) -> str:
    """
    Returns a valid WITH command given a WITHFILE filename.

    Args:
        filename: The filename to parse.

    Returns: The sanitized command name.
    """
    return os.path.basename(filename).rstrip(SHELL_SUFFIX)


def discover() -> List[str]:
    """
    Discover all of the WITH commands that can be executed.

    Returns: A list of all valid commands.
    """
    commands = []
    for directory in WITH_PATH:
        if os.path.exists(directory) and os.path.isdir(directory):
            commands += [
                filename_to_cmd(filename)
                for filename in os.listdir(directory)
                if filename.endswith(SHELL_SUFFIX)
            ]
    return commands
