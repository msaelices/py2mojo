import ast
from functools import partial
from typing import Iterable

from tokenize_rt import Token

from ..exceptions import ParseException
from ..helpers import ast_to_offset, find_token
from ..rules import RuleSet


def _replace_class_keyword(tokens: list, i: int, rules: RuleSet) -> None:
    idx = find_token(tokens, i, 'class')
    tokens[idx] = Token(name='NAME', src='struct')


def convert_classdef(node: ast.FunctionDef, rules: RuleSet) -> Iterable:
    """Converts the annotation of the given function definition."""
    if rules.convert_class_to_struct:
        for child in node.body:
            if isinstance(child, ast.Assign):
                raise ParseException(node, 'Class contains non type annotated attributes.')

        offset = ast_to_offset(node)
        yield (
            offset,
            partial(
                _replace_class_keyword,
            ),
        )
