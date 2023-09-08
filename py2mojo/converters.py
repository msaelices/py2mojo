import ast
from functools import partial
from typing import Iterable, List
from tokenize_rt import Token

from .helpers import ast_to_offset, replace_assignment


def convert_integers(node: ast.AnnAssign) -> Iterable:
    curr_type = node.annotation.id
    if curr_type != 'int':
        return

    yield (
        ast_to_offset(node),
        partial(
            replace_assignment,
            curr_type=curr_type,
            new_type='Int',
        ),
    )