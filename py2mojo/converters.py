import ast
from functools import partial
from typing import Iterable

from tokenize_rt import Token

from .helpers import ast_to_offset, get_annotation_type, find_token, find_token_after_offset, find_token_by_name, replace_assignment

def convert_assignment(node: ast.AnnAssign) -> Iterable:
    curr_type = get_annotation_type(node.annotation)
    if curr_type not in ('int', 'float', 'List[int]', 'List[float]', 'list[int]', 'list[float]'):
        return
    
    new_type = {
        'int': 'Int',
        'float': 'Float64',
        'List[int]': 'List[Int]',
        'List[float]': 'List[Float64]',
        'list[int]': 'list[Int]',
        'list[float]': 'list[Float64]',
    }[curr_type]

    yield (
        ast_to_offset(node),
        partial(
            replace_assignment,
            curr_type=curr_type,
            new_type=new_type,
        ),
    )


def _replace_annotation(tokens: list, i: int, end_offset: int, curr_type: str, new_type: str) -> None:
    ann_idx = find_token(tokens, i, ':')
    type_idx = find_token_by_name(tokens, ann_idx, name='NAME')
    end_type_idx = find_token_after_offset(tokens, ann_idx, end_offset)
    del tokens[type_idx: end_type_idx]
    tokens.insert(type_idx, Token(name='NAME', src=new_type))


def convert_functiondef(node: ast.FunctionDef) -> Iterable:
    if not node.args.args:
        return

    for arg in node.args.args:
        curr_type = get_annotation_type(arg.annotation)
        if curr_type not in ('int', 'float', 'List[int]', 'List[float]', 'list[int]', 'list[float]'):
            continue

        new_type = {
            'int': 'Int',
            'float': 'Float64',
            'List[int]': 'List[Int]',
            'List[float]': 'List[Float64]',
            'list[int]': 'list[Int]',
            'list[float]': 'list[Float64]',
        }[curr_type]

        yield (
            ast_to_offset(arg),
            partial(
                _replace_annotation,
                end_offset=arg.end_col_offset,
                curr_type=curr_type,
                new_type=new_type,
            ),
        )
