# Fuzzum

Fuzzum is a lightweight, terminal-based fuzzy file finder written in Python. It recursively scans a directory tree, presents the results in an interactive `curses` interface, and prints the selected file to standard output when you exit.

Because the selected path is written to `stdout`, Fuzzum integrates well with shell pipelines and other command-line tools.

## Features

* Interactive terminal interface powered by `curses`
* Fast recursive file discovery
* Configurable search depth
* Outputs the selected file path to `stdout`
* Designed for use in shell scripts and pipelines

## Requirements

* Python 3.9 or newer
* A Unix-like operating system with `curses` support

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/fuzzum.git
cd fuzzum
```

Install the project (or its dependencies):

```bash
pip install .
```

Alternatively, install in editable mode while developing:

```bash
pip install -e .
```

## Usage

Search the current directory:

```bash
fuzz
```

Search a specific directory:

```bash
fuzz ~/Projects
```

Limit the search depth:

```bash
fuzz ~/Projects --depth 2
```

After selecting a file, Fuzzum exits and prints the selected path:

```bash
$ fuzz
/home/user/Projects/example/main.py
```

This makes it easy to compose with other commands:

```bash
vim "$(fuzz)"
```

or

```bash
cat "$(fuzz)"
```

## Command-Line Options

| Option      | Description                                                                           |
| ----------- | ------------------------------------------------------------------------------------- |
| `path`      | Root directory to search. Defaults to the current working directory.                  |
| `--depth N` | Maximum directory depth to traverse. A value of `0` searches only the root directory. |

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
