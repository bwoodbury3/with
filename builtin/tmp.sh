# Context inside a temporary directory

tmpdir="/tmp/tmp-${CONTEXT}"

function enter() {
    echo ">> Starting context: $tmpdir"
    mkdir -p $tmpdir
    cd $tmpdir
}

function cleanup() {
    cd - > /dev/null
    echo ">> Deleting context: $tmpdir"
    rm -rfv $tmpdir
}