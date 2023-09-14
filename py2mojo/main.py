from __future__ import annotations

import argparse
import ast
import os
import sys
import tokenize
from collections import defaultdict
from typing import Callable, Sequence

from tokenize_rt import Token, reversed_enumerate, src_to_tokens, tokens_to_src

from .converters import convert_assignment, convert_functiondef, convert_classdef
from .exceptions import ParseException
from .helpers import display_error, fixup_dedent_tokens
from .rules import get_rules, RuleSet


TokenFunc = Callable[[list[Token], int], None]


def get_converters(klass: type) -> list[TokenFunc]:
    return {
        ast.ClassDef: [
            convert_classdef,
        ],
        ast.AnnAssign: [
            convert_assignment,
        ],
        ast.FunctionDef: [
            convert_functiondef,
        ],
    }.get(klass, [])


def visit(tree: ast.Module, rules: RuleSet) -> list[TokenFunc]:
    nodes = [tree]
    ret = defaultdict(list)
    while nodes:
        node = nodes.pop()

        for converter in get_converters(type(node)):
            for offset, token_func in converter(node, rules):
                ret[offset].append(token_func)

        for name in reversed(node._fields):
            value = getattr(node, name)

            if isinstance(value, ast.AST):
                nodes.append(value)
            elif isinstance(value, list):
                for subvalue in reversed(value):
                    if isinstance(subvalue, ast.AST):
                        nodes.append(subvalue)
    return ret


def convert_to_mojo(source: str, rules: RuleSet) -> str:
    tree = ast.parse(source)

    callbacks = visit(tree, rules)

    if not callbacks:
        return source

    try:
        tokens = src_to_tokens(source)
    except tokenize.TokenError:
        return source

    fixup_dedent_tokens(tokens)

    for i, token in reversed_enumerate(tokens):
        if not token.src:
            continue

        for callback in callbacks.get(token.offset, ()):
            callback(tokens, i, rules)

    return tokens_to_src(tokens)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument(
        '--inplace',
        help='Rewrite the file inplace',
        action='store_true',
    )
    parser.add_argument(
        '--extension',
        help='File extension of the generated files',
        choices=['mojo', '🔥'],
        default='🔥',
        type=str,
    )
    parser.add_argument(
        '--convert-def-to-fn',
        default=True,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        '--convert-class-to-struct',
        default=True,
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args(argv)

    for filename in args.filenames:
        mojo_filename = filename if args.inplace else f'{os.path.splitext(filename)[0]}.{args.extension}'
        with open(filename) as source_file:
            source = source_file.read()

            rules = get_rules(args)

            try:
                annotated_source = convert_to_mojo(source, rules)
            except ParseException as exc:
                display_error(exc.node, exc.msg)
                sys.exit(1)

            if source != annotated_source:
                print(f'Rewriting {filename}' if args.inplace else f'Rewriting {filename} into {mojo_filename}')
                with open(mojo_filename, 'w', encoding='UTF-8', newline='') as out:
                    out.write(annotated_source)
            else:
                print(f'File {filename} unchanged')

    return 0


if __name__ == '__main__':
    sys.exit(main())
