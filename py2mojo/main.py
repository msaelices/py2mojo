from __future__ import annotations

import argparse
import ast
import os
import sys
import tokenize
from collections import defaultdict
from typing import Callable, List, Sequence

from tokenize_rt import Token, reversed_enumerate, src_to_tokens, tokens_to_src

from .converters import convert_assignment, convert_functiondef
from .helpers import fixup_dedent_tokens


TokenFunc = Callable[[List[Token], int], None]


def get_converters(klass: type) -> list[TokenFunc]:
    return {
        ast.AnnAssign: [
            convert_assignment,
        ],
        ast.FunctionDef: [
            convert_functiondef,
        ],
    }.get(klass, [])


def visit(tree: ast.Module, level: int) -> list[TokenFunc]:
    nodes = [tree]
    ret = defaultdict(list)
    while nodes:
        node = nodes.pop()

        for converter in get_converters(type(node)):
            for offset, token_func in converter(node, level):
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


def convert_to_mojo(source: str, level: int) -> str:
    tree = ast.parse(source)

    callbacks = visit(tree, level)

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
            callback(tokens, i, level)

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
        '--level',
        help='Level of how aggressive is the conversion, 0 means conservative, 1 means aggressive (so prone to errors)',
        choices=[0, 1],
        default=0,
        type=int,
    )
    args = parser.parse_args(argv)

    for filename in args.filenames:
        mojo_filename = filename if args.inplace else f'{os.path.splitext(filename)[0]}.{args.extension}'
        with open(filename) as source_file:
            source = source_file.read()

            annotated_source = convert_to_mojo(source, args.level)

            if source != annotated_source:
                print(f'Rewriting {filename}' if args.inplace else f'Rewriting {filename} into {mojo_filename}')
                with open(mojo_filename, 'w', encoding='UTF-8', newline='') as out:
                    out.write(annotated_source)
            else:
                print(f'File {filename} unchanged')

    return 0


if __name__ == '__main__':
    sys.exit(main())
