# Custom Context for an SSH Tunnel (remote)

ssh_tunnel_pid=""

function _help() {
    echo "Usage:"
    echo "$ with remote-port-forward -a remote_port:local_host:local_port user@remote_host"
    echo
    echo "Note that this requires passwordless authentication"
}

function enter() {
    port_forward_args=$1 # Of the form <remote_port>:<local_host>:<local_port>
    remote_host_arg=$2   # Of the form <user>@<remote_host>

    if [ -z "$port_forward_args" ] || [ -z "$remote_host_arg" ]; then
        _help
        return -1
    fi

    echo ">> Starting SSH tunnel context"

    # Start the SSH tunnel in the background
    ssh -N -R "$port_forward_args" "$remote_host_arg" &
    ssh_tunnel_pid=$!

    # Sanity check the process is still running
    sleep 0.5
    if ! kill -0 "$ssh_tunnel_pid" 2>/dev/null; then
        echo "ERROR: SSH tunnel exited."
        ssh_tunnel_pid=""
        return -1
    fi

    echo ">> SSH tunnel is running (PID: $ssh_tunnel_pid)"
}

function cleanup() {
    if [ -n "$ssh_tunnel_pid" ]; then
        echo ">> Stopping SSH tunnel (PID: $ssh_tunnel_pid)"
        kill "$ssh_tunnel_pid"
        wait "$ssh_tunnel_pid" 2>/dev/null  # Suppress "Terminated" message
        ssh_tunnel_pid=""

        echo ">> SSH tunnel context cleanup complete"
    fi

}
