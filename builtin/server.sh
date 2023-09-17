# Custom Context for a Temporary Web Server

web_server_pid=""

function enter() {
    web_dir=$1
    port=$2

    if [ -z "$web_dir" ]; then
        web_dir="$(pwd)"
    fi

    if [ -z "$port" ]; then
        port=8080
    fi

    echo ">> Serving $web_dir at 0.0.0.0:$port"

    # Start a simple HTTP server (Python's built-in HTTP server)
    python3 -m http.server "$port" > /dev/null 2>&1 &
    web_server_pid=$!
}

function cleanup() {
    # Stop the web server (if applicable)
    if [ -n "$web_server_pid" ]; then
        echo ">> Stopping web server (PID: $web_server_pid)"
        kill "$web_server_pid"
        wait "$web_server_pid" 2>/dev/null  # Suppress "Terminated" message
    fi
}