import ast
from typing import List, Union

from tokenize_rt import UNIMPORTANT_WS, Offset, Token


def ast_to_offset(node: Union[ast.expr, ast.stmt]) -> Offset:
    return Offset(node.lineno, node.col_offset)


def find_token(tokens: List[Token], i: int, src: str) -> int:
    """Find the index of the token with the given src."""
    try:
        while tokens[i].src != src:
            i += 1
    except IndexError:
        return -1
    return i


def find_token_by_name(tokens: List[Token], i: int, name: str) -> int:
    """Find the index of the token with the given name."""
    try:
        while tokens[i].name != name:
            i += 1
    except IndexError:
        return -1
    return i


def find_token_after_offset(tokens: List[Token], i: int, offset: int) -> int:
    """Find the index of the token after the given offset."""
    try:
        while tokens[i].utf8_byte_offset < offset:
            i += 1
    except IndexError:
        return -1
    return i


def fixup_dedent_tokens(tokens: List[Token]) -> None:
    # copied from pyupgrade
    """For whatever reason the DEDENT / UNIMPORTANT_WS tokens are misordered
    | if True:
    |     if True:
    |         pass
    |     else:
    |^    ^- DEDENT
    |+----UNIMPORTANT_WS
    """
    for i, token in enumerate(tokens):
        if token.name == UNIMPORTANT_WS and tokens[i + 1].name == 'DEDENT':
            tokens[i], tokens[i + 1] = tokens[i + 1], tokens[i]


def get_node_name(node: ast.AST) -> str:
    """Returns the name of the given node."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Attribute):
        return node.attr
    elif isinstance(node, ast.Call):
        return node.func.id if isinstance(node.func, ast.Name) else node.func.attr
    else:
        return 'unknown'


def get_next_node(node: ast.AST) -> ast.AST:
    """Returns the next node of the given node."""
    if isinstance(node, ast.Attribute):
        return node.value
    elif isinstance(node, ast.Call):
        return node.func if isinstance(node.func, ast.Name) else node.func.value
    else:
        raise ValueError(f'Unexpected node type: {type(node)}')


def get_dot_path(node: ast.Attribute):
    """Returns the dot path of the given attribute node."""
    attr_list = []
    while isinstance(node, ast.Attribute) or isinstance(node, ast.Call):
        attr = get_node_name(node)
        node = get_next_node(node)
        attr_list.append(attr)
    attr_list.append(get_node_name(node))
    return reversed(attr_list)


def get_annotation_type(node: ast.AST) -> str:
    """Returns the type of the given annotation node."""
    
    match node.__class__.__name__:
        case 'Name':
            curr_type = node.id
        case 'Subscript':
            try:
                curr_type = f'{node.value.id}[{node.slice.id}]'
            except:
                breakpoint()
                return ''
        case _:
            curr_type = ''
    return curr_type


def get_mojo_type(curr_type: str) -> str:
    """Returns the corresponding Mojo type for the given Python type."""
    try:
        return {
            'int': 'Int',
            'float': 'Float64',
            'List[int]': 'List[Int]',
            'List[float]': 'List[Float64]',
            'list[int]': 'list[Int]',
            'list[float]': 'list[Float64]',
        }[curr_type]
    except KeyError:
        return ''