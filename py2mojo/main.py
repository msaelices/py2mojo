from __future__ import annotations

import argparse
import ast
import os
import sys
import tokenize
from collections import defaultdict
from typing import Callable, List, Sequence

from tokenize_rt import Token, reversed_enumerate, src_to_tokens, tokens_to_src

from .converters import convert_assignments
from .helpers import fixup_dedent_tokens


TokenFunc = Callable[[List[Token], int], None]


def get_converters(klass: type) -> list[TokenFunc]:
    return {
        ast.AnnAssign: [
            convert_assignments,
        ],
    }.get(klass, [])


def visit(tree: ast.Module) -> list[TokenFunc]:
    nodes = [tree]
    ret = defaultdict(list)
    while nodes:
        node = nodes.pop()

        for annotator in get_converters(type(node)):
            for offset, token_func in annotator(node):
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


def convert_to_mojo(source: str) -> str:
    tree = ast.parse(source)

    callbacks = visit(tree)

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
            callback(tokens, i)

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
        help='File extension used for mojo file',
        choices=['mojo', '🔥'],
        default='🔥',
        type=str,
    )
    args = parser.parse_args(argv)

    for filename in args.filenames:
        mojo_filename = filename if args.inplace else f'{os.path.splitext(filename)[0]}.{args.extension}'
        with open(filename) as source_file:
            source = source_file.read()

            annotated_source = convert_to_mojo(source)

            if source != annotated_source:
                print(f'Rewriting {filename}' if args.inplace else f'Rewriting {filename} into {mojo_filename}')
                with open(mojo_filename, 'w', encoding='UTF-8', newline='') as out:
                    out.write(annotated_source)
            else:
                print(f'File {filename} unchanged')

    return 0


if __name__ == '__main__':
    sys.exit(main())
