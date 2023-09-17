# Context with a virtual environment

venvdir="/tmp/tmp-venv-${CONTEXT}"

function enter() {
    echo ">> Initializing virtual environment $venvdir"
    /usr/bin/python3 -m venv $venvdir
    source "$venvdir/bin/activate"
}

function cleanup() {
    echo ">> Cleaning up virtual environment $venvdir"
    deactivate
    rm -rf $venvdir
}