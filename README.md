# py2mojo

Automated Python to Mojo code translation

A tool to automatically convert Python code to the new [Mojo programming language](https://www.modular.com/mojo).

## Installation

```bash
pip install py2mojo
```

## Approach

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
