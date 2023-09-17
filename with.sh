#!/bin/bash
# Responsible for managing a shell context.

set -e

# These variables are intentionally exposed to WITH commands.
export COMMAND_PATH=$1
export CONTEXT=$2
export ARGS=$3
export EXECUTABLE=$4

if [ -z "$COMMAND_PATH" ] || [ -z "$CONTEXT" ]; then
    echo "with.sh <COMMAND_PATH> <CONTEXT>"
    exit -1
fi

source $COMMAND_PATH

# Trap cleanup in case the internal context fails.
trap "cleanup $ARGS" EXIT
enter $ARGS

# If the user specified a command to run, run that. Otherwise drop into a shell.
if [ -z "$EXECUTABLE" ]; then
    /bin/bash
else
    $EXECUTABLE
fi
