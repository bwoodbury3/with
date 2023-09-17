# `with` - A Context Manager for Temporary Shell Sessions

`with` is a powerful command-line tool that allows you to create and manage temporary shell sessions in specific contexts. It provides an intuitive way to work within temporary environments or execute commands within those contexts.

```bash
$ with tmp
>> Starting context: /tmp/tmp-e7668361
$ curl https://raw.githubusercontent.com/bwoodbury3/with/main/with.sh > with.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   579  100   579    0     0   9512      0 --:--:-- --:--:-- --:--:-- 10924
$ exit
exit
>> Deleting context: /tmp/tmp-e7668361
/tmp/tmp-e7668361/with.sh
/tmp/tmp-e7668361
```

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Custom Context Managers](#custom-context-managers)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install `with`, follow these simple steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/bwoodbury3/with.git
   ```

2. Install `with` using `pip`:

   ```bash
   pip install -e with
   ```

Now, you should have the `with` command available in your shell.

## Usage

The `with` command is designed to create and manage temporary shell sessions. It accepts a context command and optionally, a command to run within that context. Here's the basic syntax:

```bash
with <context> [-a args...] [-e command]
```

- `<context>`: The type of context to enter (`--help` for a full list).
- `-a [args...]` (optional): Arguments to pass into the context.
- `-e [command]` (optional): A shell command to run within the specified context.

## Examples

### Starting a Temporary Shell Session

To start an ephemeral shell session in a temporary directory, try `with tmp`:

```bash
$ with tmp
>> Starting context: /tmp/tmp-e7668361
$ curl https://raw.githubusercontent.com/bwoodbury3/with/main/with.sh > with.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   579  100   579    0     0   9512      0 --:--:-- --:--:-- --:--:-- 10924
$ exit
exit
>> Deleting context: /tmp/tmp-e7668361
/tmp/tmp-e7668361/with.sh
/tmp/tmp-e7668361
```

This will open a new shell session pointing to a temporary directory. You can interact with the shell as usual.

### Exiting a Session

Simply type `exit` to exit an interactive context.

### Running a Command in a Temporary Context

You can also execute a single command within a temporary context:

```bash
$ with venv -e "python --version"
>> Initializing virtual environment /tmp/tmp-venv-ee9ac361
Python 3.9.6
>> Cleaning up virtual environment /tmp/tmp-venv-ee9ac361
```

In this example, `with` creates an ephemeral virtual environment and runs the `python --version` command within that context. The context is automatically cleaned up after the command completes.

## Custom Context Managers

One of the powerful features of the `with` tool is the ability for users to create custom context managers to suit their specific needs. These custom context managers are implemented as bash scripts placed in the `~/.with` directory. `with` will automatically discover new scripts added to this library and make them available for use.

### Creating a Custom Context Manager

To create a custom context manager, follow these steps:

1. **Create a Bash Script**: Create a Bash script with a meaningful name inside the `~/.with` directory. The script name will define your custom context manager.

2. **Define `enter()` and `cleanup()` Functions**: In your Bash script, define two essential functions:

   - `enter()`: This function is called when the context is entered. It should contain any setup or initialization code required for your context.

   - `cleanup()`: This function is called when the context is exited, either by ending the shell session or running a command. It should contain cleanup code to remove any resources or modifications made during the context.

Your script has access to the following environment variables:
* `$CONTEXT`: This variable has a unique value that can be used to identify the session for start and cleanup.
* `$ARGS`: This variable holds a space-separated list of args that can be passed into the `with` command with the `-a` flag.

Here's a trivial example example of a custom context manager that creates a temporary directory:

```bash
# Example: Custom Context Inside a Temporary Directory
# FILENAME: ~/.with/mycustomcontext.sh

tmpdir="/tmp/tmp-${CONTEXT}"

function enter() {
    echo ">> Starting context: $tmpdir"
    mkdir -p "$tmpdir"
    cd "$tmpdir"
}

function cleanup() {
    cd - > /dev/null
    echo ">> Deleting context: $tmpdir"
    rm -rfv "$tmpdir"
}
```

### Using Your Custom Context Manager

Once you've created your custom context manager script, you can use it with the `with` tool like any other context:

```bash
with mycustomcontext
```

The `with` tool will execute the `enter()` function when entering the context and the `cleanup()` function when exiting the context.

### Sharing Custom Context Managers

If you've created a particularly useful custom context manager, consider sharing it with the community by opening a pull request adding it to the `builtin` package.

## Contributing

We welcome contributions from the community. If you'd like to contribute to the development of `with`, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your fork to your local machine.
3. Create a new branch for your contribution.
4. Make your changes and commit them.
5. Push your changes to your fork on GitHub.
6. Submit a pull request to the main repository.

For more details, please read our [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License.
