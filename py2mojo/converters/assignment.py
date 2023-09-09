import ast
from functools import partial
from typing import Iterable, List

from tokenize_rt import Token

from ..helpers import ast_to_offset, get_annotation_type, find_token, find_token_by_name, get_mojo_type


def _replace_assignment(tokens: List[Token], i: int, new_type: str) -> None:
    tokens.insert(0, Token(name='NAME', src='var '))
    ann_idx = find_token(tokens, i, ':')
    type_idx = find_token_by_name(tokens, ann_idx, name='NAME')
    end_type_idx = find_token(tokens, type_idx, '=')
    del tokens[type_idx: end_type_idx - 1]
    tokens.insert(type_idx, Token(name='NAME', src=new_type))


def convert_assignment(node: ast.AnnAssign) -> Iterable:
    """Convert an assignment to a mojo assignment."""
    curr_type = get_annotation_type(node.annotation)
    new_type = get_mojo_type(curr_type)
    if not new_type:
        return

    yield (
        ast_to_offset(node),
        partial(
            _replace_assignment,
            new_type=new_type,
        ),
    )
