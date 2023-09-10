import ast
from functools import partial
from typing import Iterable

from tokenize_rt import Token

from ..helpers import ast_to_offset, find_token


def _replace_class_keyword(tokens: list, i: int, level: int) -> None:
    idx = find_token(tokens, i, 'class')
    tokens[idx] = Token(name='NAME', src='struct')


def convert_classdef(node: ast.FunctionDef, level: int = 0) -> Iterable:
    """Converts the annotation of the given function definition."""
    if level > 0:
        offset = ast_to_offset(node)
        yield (
            offset,
            partial(
                _replace_class_keyword,
            ),
        )