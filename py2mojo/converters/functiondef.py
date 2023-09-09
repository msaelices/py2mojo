import ast
from functools import partial
from typing import Iterable, Optional

from tokenize_rt import Token

from ..helpers import ast_to_offset, get_annotation_type, find_token, find_token_after_offset, find_token_by_name, get_mojo_type


def _replace_annotation(tokens: list, i: int, end_offset: int, new_type: str, ann_offset: Optional[int] = None) -> None:
    if ann_offset:
        ann_idx = find_token_after_offset(tokens, i, ann_offset)
    else:
        ann_idx = find_token(tokens, i, ':')
    type_idx = find_token_by_name(tokens, ann_idx, name='NAME')
    end_type_idx = find_token_after_offset(tokens, ann_idx, end_offset)
    del tokens[type_idx: end_type_idx]
    tokens.insert(type_idx, Token(name='NAME', src=new_type))


def convert_functiondef(node: ast.FunctionDef) -> Iterable:
    """Converts the annotation of the given function definition."""
    if not node.args.args:
        return

    for arg in node.args.args:
        curr_type = get_annotation_type(arg.annotation)
        new_type = get_mojo_type(curr_type)
        if not new_type:
            return

        yield (
            ast_to_offset(arg),
            partial(
                _replace_annotation,
                end_offset=arg.end_col_offset,
                new_type=new_type,
            ),
        )
    
    if node.returns:
        curr_type = get_annotation_type(node.returns)
        new_type = get_mojo_type(curr_type)
        if not new_type:
            return

        offset = ast_to_offset(node.returns)
        yield (
            offset,
            partial(
                _replace_annotation,
                end_offset=node.returns.end_col_offset,
                new_type=new_type,
                ann_offset=offset.utf8_byte_offset,
            ),
        )
