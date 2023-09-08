import ast
from typing import List, Union

from tokenize_rt import UNIMPORTANT_WS, Offset, Token


def ast_to_offset(node: Union[ast.expr, ast.stmt]) -> Offset:
    return Offset(node.lineno, node.col_offset)


def find_token(tokens: List[Token], i: int, src: str) -> int:
    try:
        while tokens[i].src != src:
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
    if isinstance(node, ast.Attribute):
        return node.value
    elif isinstance(node, ast.Call):
        return node.func if isinstance(node.func, ast.Name) else node.func.value
    else:
        raise ValueError(f'Unexpected node type: {type(node)}')


def get_dot_path(node: ast.Attribute):
    attr_list = []
    while isinstance(node, ast.Attribute) or isinstance(node, ast.Call):
        attr = get_node_name(node)
        node = get_next_node(node)
        attr_list.append(attr)
    attr_list.append(get_node_name(node))
    return reversed(attr_list)


def replace_assignment(tokens: List[Token], i: int, curr_type: str, new_type: str) -> None:
    tokens.insert(0, Token(name='NAME', src='var '))
    j = find_token(tokens, i, curr_type)
    tokens[j] = tokens[j]._replace(src=new_type)