import ast
from functools import partial
from typing import Iterable, List
from tokenize_rt import Token

from .helpers import ast_to_offset, get_annotation_type, replace_assignment


def convert_assignments(node: ast.AnnAssign) -> Iterable:
    curr_type = get_annotation_type(node.annotation)
    if curr_type not in ('int', 'float', 'List[int]', 'List[float]'):
        return
    
    new_type = {
        'int': 'Int',
        'float': 'Float64',
        'List[int]': 'List[Int]',
        'List[float]': 'List[Float64]',
    }[curr_type]

    yield (
        ast_to_offset(node),
        partial(
            replace_assignment,
            curr_type=curr_type,
            new_type=new_type,
        ),
    )