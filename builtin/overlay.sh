#!/bin/bash

# Ensure you have the necessary privileges for OverlayFS operations.
# This script assumes you have superuser privileges.

# Define variables
original_dir="$(pwd)"
mount_dir="/tmp/overlay-${CONTEXT}-mount"
upper_dir="/tmp/overlay-${CONTEXT}-upper"
work_dir="/tmp/overlay-${CONTEXT}-work"

# Function to create the OverlayFS and enter the context
enter() {
    mkdir $mount_dir $upper_dir $work_dir

    # Set up OverlayFS
    # mount -t overlay overlay -o lowerdir=/lower1:/lower2:/lower3,upperdir=/upper,workdir=/work /merged
    # Note MacOS requires the -t flag to be after -o
    sudo mount -t overlay overlay -o lowerdir=$original_dir,upperdir=$upper_dir,workdir=$work_dir $mount_dir || return 1

    # Change to the OverlayFS directory. Return here if we can't get to that
    # directory, as it indicates a problem with the mount command above.
    cd "$mount_dir" || return 1

    # Display a message to indicate the overlay is active
    echo ">> OverlayFS is active. Experiment with this directory."
}

# Function to clean up OverlayFS and exit the context
cleanup() {
    echo ">> Cleaning temporary filesystem"

    cd "$original_dir"

    # Unmount OverlayFS
    sudo umount "$mount_dir" || echo "ERROR: Unable to unmount overlay!!"

    # Remove temporary directories
    rm -rf "$mount_dir" "$upper_dir" "$work_dir"
}
