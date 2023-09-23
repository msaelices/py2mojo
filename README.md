# py2mojo

Automated Python to Mojo code translation

A tool to automatically convert Python code to the new [Mojo programming language](https://www.modular.com/mojo).

## Installation

```bash
pip install py2mojo
```

## Usage

You can read the usage by running `py2mojo --help`:

```bash
❯ py2mojo --help
usage: py2mojo [-h] [--inplace] [--extension {mojo,🔥}] [--convert-def-to-fn | --no-convert-def-to-fn] [--convert-class-to-struct | --no-convert-class-to-struct] [--float-precision {32,64}]
               filenames [filenames ...]

positional arguments:
  filenames

options:
  -h, --help            show this help message and exit
  --inplace             Rewrite the file inplace
  --extension {mojo,🔥}  File extension of the generated files
  --convert-def-to-fn, --no-convert-def-to-fn
  --convert-class-to-struct, --no-convert-class-to-struct
  --float-precision {32,64}
```

Examples:

```bash
❯ py2mojo myfile.py
```

```bash
❯ py2mojo mypackage/*.py
```

## ⚠ Disclaimer

Please be aware that the Mojo programming language is still in its nascent stages of development. As with any young language, there might be frequent updates, changes, and unforeseen quirks in its syntax and behavior. There will probably be instances where the conversion might not work and may require manual adjustments.

So, consider this tool as experimental. Please do not trust the generated code and double-check it.

## Implementation details

This uses a similar approach to the [pyupgrade](https://github.com/asottile/pyupgrade) tool, using the AST parser to analyze the Python code and replace some parts of it with the equivalent Mojo code.

As Mojo is a superset of Python, non-replaced logic should be also a valid Mojo code.

## Contributing

### How to install it locally

1. Fork the repository

2. Clone your fork:

```bash
git clone git@github.com:youraccount/py2mojo.git
```

3. Install it locally:
```
cd py2mojo
pip install -e .
```
